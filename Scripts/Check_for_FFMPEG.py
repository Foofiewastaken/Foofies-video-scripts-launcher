import os
import subprocess
import urllib.request
import zipfile
import shutil
import platform
from tkinter import messagebox

APP_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG_PATH = os.path.join(APP_DIR, "ffmpeg.exe")

def check_ffmpeg():
    """Return True if ffmpeg is available either in PATH or in app root."""
    if os.path.exists(FFMPEG_PATH):
        return True
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ffmpeg():
    """Download and place ffmpeg.exe into the app root folder."""
    system = platform.system()
    if system != "Windows":
        raise NotImplementedError("Auto-install only implemented for Windows.")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(APP_DIR, "ffmpeg.zip")

    # Download FFmpeg
    urllib.request.urlretrieve(url, zip_path)

    # Extract FFmpeg
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(APP_DIR)

    os.remove(zip_path)

    # Find ffmpeg.exe in extracted folder
    for root_dir, dirs, files in os.walk(APP_DIR):
        if "ffmpeg.exe" in files:
            shutil.copy(os.path.join(root_dir, "ffmpeg.exe"), FFMPEG_PATH)
            break

    # Clean up extracted folders
    for folder in os.listdir(APP_DIR):
        if folder.startswith("ffmpeg-") and os.path.isdir(os.path.join(APP_DIR, folder)):
            shutil.rmtree(os.path.join(APP_DIR, folder))

    messagebox.showinfo("FFMPEG", "FFMPEG has been installed in the app root!")
