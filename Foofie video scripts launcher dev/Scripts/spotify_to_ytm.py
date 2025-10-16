import sys
import requests
import subprocess
import json

spotify_url = sys.argv[1]
artist_override = sys.argv[2] if len(sys.argv) > 2 else ""

# 1️⃣ Get track info from Spotify oEmbed
r = requests.get(f"https://open.spotify.com/oembed?url={spotify_url}")
if r.status_code != 200:
    print("Error fetching track info")
    sys.exit(1)

data = r.json()
track_name = data['title']  # e.g. "Song Name by Artist"

# If user provided artist, append it to the search
if artist_override.strip():
    search_query = f"{track_name} {artist_override}"
else:
    search_query = track_name

# 2️⃣ Search YouTube for the track
result = subprocess.run(
    ["yt-dlp", f"ytsearch1:{search_query}", "--dump-json"],
    capture_output=True,
    text=True
)

if result.returncode != 0 or not result.stdout.strip():
    print("Error searching YouTube")
    sys.exit(1)

info = json.loads(result.stdout)
yt_url = info.get("webpage_url", "")
print(yt_url)
