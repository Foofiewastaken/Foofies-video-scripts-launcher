import sys
import requests
import subprocess
import os
import re
import json

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)

# ------------------- Parse arguments -------------------
spotify_url = sys.argv[1]
artist_override = ""
video_mode = False

for arg in sys.argv[2:]:
    if arg.lower() == "-v":
        video_mode = True
    else:
        artist_override = arg

print(f"[DEBUG] Spotify URL: {spotify_url}")
print(f"[DEBUG] Artist override: {artist_override}")
print(f"[DEBUG] Video mode: {video_mode}")

# ------------------- Get track info from Spotify -------------------
try:
    r = requests.get(f"https://open.spotify.com/oembed?url={spotify_url}")
    r.raise_for_status()
except Exception as e:
    print(f"[ERROR] Failed to fetch Spotify oEmbed: {e}")
    sys.exit(1)

data = r.json()
track_title = data.get('title', '').strip()
if not track_title:
    print("[ERROR] Could not get song title from Spotify")
    sys.exit(1)

print(f"[DEBUG] Track title from Spotify: {track_title}")

# ------------------- Build search query -------------------
search_query = f"{track_title} {artist_override}" if artist_override.strip() else track_title
yt_search = f"ytsearch1:{search_query}"
print(f"[DEBUG] YouTube search query: {yt_search}")

# ------------------- Search YouTube -------------------
try:
    result = subprocess.run(
        ["yt-dlp", yt_search, "--dump-json"],
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

print(f"[DEBUG] Found YouTube URL: {yt_url}")

# ------------------- Determine artist for folder -------------------
if artist_override.strip():
    folder_artist = sanitize_filename(artist_override)
    print(f"[DEBUG] Using user-supplied artist for folder: {folder_artist}")
else:
    folder_artist = sanitize_filename(info.get("uploader") or "Unknown Artist")
    print(f"[DEBUG] Using YouTube uploader for folder: {folder_artist}")

song_name = sanitize_filename(track_title)

# ------------------- Determine download folder -------------------
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if video_mode:
    download_path = os.path.join(root_dir, "Downloads", "Music", "Music Videos", folder_artist)
else:
    download_path = os.path.join(root_dir, "Downloads", "Music", "Songs", folder_artist)
os.makedirs(download_path, exist_ok=True)
print(f"[DEBUG] Download folder: {download_path}")

# ------------------- Prepare yt-dlp command -------------------
output_template = os.path.join(download_path, f"{song_name}.%(ext)s")
thumbnail_url = data.get("thumbnail_url", "")

yt_dlp_cmd = ["yt-dlp"]

if video_mode:
    yt_dlp_cmd += ["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4", "--recode-video", "mp4"]
else:
    yt_dlp_cmd += ["-x", "--audio-format", "mp3"]

yt_dlp_cmd += [yt_url, "-o", output_template]

if thumbnail_url:
    yt_dlp_cmd += ["--add-metadata", "--embed-thumbnail"]

# ------------------- Cookies/User-Agent -------------------
cookie_files = [
    os.path.join(root_dir, "www.youtube.com_cookies.txt"),
    os.path.join(root_dir, "Scripts", "www.youtube.com_cookies.txt")
]

cookies_used = False
for cfile in cookie_files:
    if os.path.exists(cfile):
        yt_dlp_cmd += ["--cookies", cfile]
        cookies_used = True
        print(f"[DEBUG] Using cookies file: {cfile}")
        break

if not cookies_used:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    yt_dlp_cmd += ["--add-header", f"User-Agent: {ua}"]
    print("[DEBUG] Using custom User-Agent header")

# ------------------- Run yt-dlp -------------------
print(f"[DEBUG] Running yt-dlp command: {' '.join(yt_dlp_cmd)}")
subprocess.run(yt_dlp_cmd)
print("[SUCCESS] Download complete!")
