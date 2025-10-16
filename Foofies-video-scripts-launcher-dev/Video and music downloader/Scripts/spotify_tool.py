import sys
import requests
import subprocess
import json
import os
import re
import shutil

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)

def get_spotify_track_info(spotify_url):
    r = requests.get(f"https://open.spotify.com/oembed?url={spotify_url}")
    r.raise_for_status()
    data = r.json()
    title = data.get("title", "").strip()
    thumbnail = data.get("thumbnail_url", "")
    if not title:
        raise Exception("Could not get track title from Spotify")
    return title, thumbnail

def search_youtube(track_name, artist_override=""):
    query = f"{track_name} {artist_override}" if artist_override.strip() else track_name
    result = subprocess.run(
        ["yt-dlp", f"ytsearch1:{query}", "--dump-json"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise Exception("Error searching YouTube")
    info = json.loads(result.stdout)
    return info.get("webpage_url", ""), info.get("uploader", "Unknown Artist")

def get_direct_url(yt_url):
    result = subprocess.run(
        ["yt-dlp", "-f", "mp4", "--get-url", yt_url],
        capture_output=True,
        text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise Exception("Failed to get direct URL")
    return result.stdout.strip()

def copy_to_clipboard(text):
    import subprocess
    subprocess.run('powershell -Command "Set-Clipboard -Value \\"{}\\" "'.format(text), shell=True)

def download_track(yt_url, track_name, folder_artist, video_mode, thumbnail_url):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if video_mode:
        download_path = os.path.join(root_dir, "Downloads", "Music", "Music Videos", folder_artist)
    else:
        download_path = os.path.join(root_dir, "Downloads", "Music", "Songs", folder_artist)
    os.makedirs(download_path, exist_ok=True)
    output_template = os.path.join(download_path, f"{track_name}.%(ext)s")
    
    cmd = ["yt-dlp"]
    if video_mode:
        cmd += ["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4", "--recode-video", "mp4"]
    else:
        cmd += ["-x", "--audio-format", "mp3"]
    cmd += [yt_url, "-o", output_template]
    if thumbnail_url:
        cmd += ["--add-metadata", "--embed-thumbnail"]

    # cookies or user agent
    cookie_file = os.path.join(root_dir, "www.youtube.com_cookies.txt")
    if os.path.exists(cookie_file):
        cmd += ["--cookies", cookie_file]
    else:
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        cmd += ["--add-header", f"User-Agent: {ua}"]

    subprocess.run(cmd)
    print("[SUCCESS] Download complete!")

# ------------------- Main -------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python spotify_tool.py [link|direct|download] <spotify_url> [artist/direct/video]")
        sys.exit(1)

    mode = sys.argv[1]
    spotify_url = sys.argv[2]

    if mode == "link":
        artist_override = sys.argv[3] if len(sys.argv) > 3 else ""
        track_name, _ = get_spotify_track_info(spotify_url)
        yt_url, _ = search_youtube(track_name, artist_override)
        copy_to_clipboard(yt_url)
        print(yt_url)

    elif mode == "direct":
        # Get YouTube link first via search
        track_name, _ = get_spotify_track_info(spotify_url)
        yt_url, _ = search_youtube(track_name)
        direct_url = get_direct_url(yt_url)
        copy_to_clipboard(direct_url)
        print(direct_url)

    elif mode == "download":
        artist_override = sys.argv[3] if len(sys.argv) > 3 else ""
        video_choice = sys.argv[4].lower() if len(sys.argv) > 4 else "n"
        video_mode = video_choice == "y"

        track_name, thumbnail_url = get_spotify_track_info(spotify_url)
        yt_url, uploader = search_youtube(track_name, artist_override)
        folder_artist = sanitize_filename(artist_override) if artist_override.strip() else sanitize_filename(uploader)
        download_track(yt_url, sanitize_filename(track_name), folder_artist, video_mode, thumbnail_url)
