import sys
import subprocess
import json
import os
import re
import requests

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)

# ------------------- Get Spotify URL -------------------
if len(sys.argv) < 2:
    print("Usage: python spotify_to_ytm_video.py <spotify_url>")
    sys.exit(1)

spotify_url = sys.argv[1]
print(f"[DEBUG] Spotify URL: {spotify_url}")

# ------------------- Get track info from Spotify -------------------
try:
    r = requests.get(f"https://open.spotify.com/oembed?url={spotify_url}")
    r.raise_for_status()
except Exception as e:
    print(f"[ERROR] Failed to fetch Spotify oEmbed: {e}")
    sys.exit(1)

data = r.json()
song_name = data.get('title', '').strip()
if not song_name:
    print("[ERROR] Could not get song title from Spotify")
    sys.exit(1)

song_name = sanitize_filename(song_name)
print(f"[DEBUG] Track: {song_name}")

# ------------------- Search YouTube -------------------
search_query = f"ytsearch1:{song_name}"
print(f"[DEBUG] Searching YouTube: {search_query}")

try:
    result = subprocess.run(
        ["yt-dlp", search_query, "--dump-json"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        print(f"[ERROR] yt-dlp search failed:\n{result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] yt-dlp execution failed: {e}")
    sys.exit(1)

info = json.loads(result.stdout)
yt_url = info.get("webpage_url", "")
if not yt_url:
    print("[ERROR] No YouTube URL found")
    sys.exit(1)

# ------------------- Get artist from YouTube -------------------
artist_name = info.get("uploader") or "Unknown Artist"
artist_name = sanitize_filename(artist_name)
print(f"[DEBUG] Artist (from YouTube channel): {artist_name}")
print(f"[DEBUG] Found YouTube URL: {yt_url}")

# ------------------- MP4 output folder -------------------
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
download_path = os.path.join(root_dir, "Downloads", "Music", "Music Videos", artist_name)
os.makedirs(download_path, exist_ok=True)
print(f"[DEBUG] Download folder: {download_path}")

thumbnail_url = data.get("thumbnail_url", "")
if thumbnail_url:
    print(f"[DEBUG] Cover thumbnail URL: {thumbnail_url}")

output_template = os.path.join(download_path, f"{song_name}.%(ext)s")
print(f"[DEBUG] Downloading to: {output_template} ...")

# ------------------- Cookies/User-Agent handling -------------------
cookie_files = [
    os.path.join(root_dir, "www.youtube.com_cookies.txt"),
    os.path.join(root_dir, "Scripts", "www.youtube.com_cookies.txt")
]

# yt-dlp command with audio conversion to AAC
yt_dlp_cmd = [
    "yt-dlp",
    "-f", "bestvideo+bestaudio/best",  # pick best video + best audio
    "--merge-output-format", "mp4",    # merge into MP4
    "--recode-video", "mp4",           # re-encode audio/video to MP4-compatible AAC
    yt_url,
    "-o", output_template
]

# Embed cover if available
if thumbnail_url:
    yt_dlp_cmd += ["--add-metadata", "--embed-thumbnail"]

# Check for cookies
cookies_used = False
for cfile in cookie_files:
    if os.path.exists(cfile):
        yt_dlp_cmd += ["--cookies", cfile]
        cookies_used = True
        print(f"[DEBUG] Using cookies file: {cfile}")
        break

# If no cookies, add User-Agent
if not cookies_used:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    yt_dlp_cmd += ["--add-header", f"User-Agent: {ua}"]
    print("[DEBUG] Using custom User-Agent header")

# ------------------- Run yt-dlp -------------------
print(f"[DEBUG] Running yt-dlp: {' '.join(yt_dlp_cmd)}")
subprocess.run(yt_dlp_cmd)
print("[SUCCESS] Download complete!")
