import sys
import subprocess
import json
import os
import re
import requests

def sanitize_filename(name):
    # Remove invalid Windows filename characters: \ / : * ? " < > |
    return re.sub(r'[\\/:*?"<>|]', '', name)

# 1️⃣ Get Spotify URL from command-line argument
if len(sys.argv) < 2:
    print("Usage: python spotify_to_ytm_download_yt_artist.py <spotify_url>")
    sys.exit(1)

spotify_url = sys.argv[1]
print(f"[DEBUG] Spotify URL: {spotify_url}")

# 2️⃣ Get track info from Spotify oEmbed
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

# 3️⃣ Search YouTube
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

# 4️⃣ Get artist from YouTube uploader
artist_name = info.get("uploader", "Unknown Artist")
artist_name = sanitize_filename(artist_name)
print(f"[DEBUG] Artist (from YouTube channel): {artist_name}")

print(f"[DEBUG] Found YouTube URL: {yt_url}")

# 5️⃣ Prepare download folder
download_path = os.path.join("Downloads", "Music", artist_name)
os.makedirs(download_path, exist_ok=True)
print(f"[DEBUG] Download folder: {download_path}")

# 6️⃣ Get Spotify cover thumbnail URL
thumbnail_url = data.get("thumbnail_url", "")
if thumbnail_url:
    print(f"[DEBUG] Cover thumbnail URL: {thumbnail_url}")

# 7️⃣ Download YouTube video/audio as mp4 with embedded thumbnail
output_template = os.path.join(download_path, f"{song_name}.%(ext)s")
print(f"[DEBUG] Downloading to: {output_template} ...")

yt_dlp_cmd = [
    "yt-dlp",
    "-f", "bestvideo+bestaudio/best",
    "--merge-output-format", "mp4",
    yt_url,
    "-o", output_template
]

# Embed cover image if available
if thumbnail_url:
    yt_dlp_cmd += ["--add-metadata", "--embed-thumbnail"]  # only this, no --thumbnail

subprocess.run(yt_dlp_cmd)

print("[SUCCESS] Download complete!")
