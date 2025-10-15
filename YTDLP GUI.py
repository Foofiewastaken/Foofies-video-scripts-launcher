import os
import subprocess
import tkinter as tk
from tkinter import messagebox, font
import webbrowser
import sys
import urllib.request
import zipfile
import shutil
import platform

# ---------- App folders ----------
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS_FOLDER = os.path.join(APP_DIR, "Scripts")

# ---------- Run batch script ----------
def run_script(script_name):
    path = os.path.join(SCRIPTS_FOLDER, script_name)
    if os.path.exists(path):
        subprocess.Popen(['cmd', '/c', path])
    else:
        messagebox.showerror("Error", f"Script not found:\n{path}")

# ---------- Tips ----------
def show_tips():
    top = tk.Toplevel(app)
    top.title("Tips")
    top.resizable(False, False)

    txt = tk.Text(top, wrap="word", width=72, height=18, padx=10, pady=10, borderwidth=0)
    txt.insert("end",
        "If a video is restricted or you get a cookies error:\n\n"
        "1. Export your browser cookies file (www.youtube.com_cookies.txt or music.youtube.com_cookies.txt). "
        "Best way to do this, is by "
    )
    start_index = txt.index("end-1c")
    txt.insert("end", "downloading this extension")
    end_index = txt.index("end-1c")
    txt.insert("end",
        ". \n2. Open the extension in Youtube, and click export. \n"
        "3. Move the cookies from Downloads to the root folder.\n"
        "4. Rerun the script.\n\n"
        "Cookies must be named www.youtube.com_cookies.txt or music.youtube.com_cookies.txt.\n\n"
        "Add more scripts in the root folder."
    )
    txt.tag_add("link", start_index, end_index)
    txt.tag_config("link", foreground="blue", underline=1)
    txt.tag_bind("link", "<Button-1>", lambda e: webbrowser.open_new(
        "https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
    ))

    txt.config(state="disabled")
    txt.pack(fill="both", expand=True)
    tk.Button(top, text="OK", command=top.destroy).pack(pady=(6, 10))
    top.transient(app)
    top.grab_set()
    app.wait_window(top)

# ---------- Credits ----------
def show_credits():
    top = tk.Toplevel(app)
    top.title("Credits")
    top.geometry("400x200")
    top.resizable(False, False)

    tk.Label(top, text="Scripts and GUI made by Foofie.\nIf obtained elsewhere, might be a virus.\n\n"
                        "Discord: .foofie\nTelegram: @Foofie_UwU\nGitHub: Click Docs button",
             font=("Segoe UI", 12), justify="center").pack(pady=20)
    tk.Button(top, text="OK", command=top.destroy).pack(pady=10)
    top.transient(app)
    top.grab_set()
    app.wait_window(top)

# ---------- FFMPEG Functions ----------
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
        messagebox.showerror("Error", "Auto-install only implemented for Windows.")
        return

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(APP_DIR, "ffmpeg.zip")

    try:
        urllib.request.urlretrieve(url, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(APP_DIR)
        os.remove(zip_path)

        # Find ffmpeg.exe
        for root_dir, dirs, files in os.walk(APP_DIR):
            if "ffmpeg.exe" in files:
                shutil.copy(os.path.join(root_dir, "ffmpeg.exe"), FFMPEG_PATH)
                break

        # Cleanup
        for folder in os.listdir(APP_DIR):
            if folder.startswith("ffmpeg-") and os.path.isdir(os.path.join(APP_DIR, folder)):
                shutil.rmtree(os.path.join(APP_DIR, folder))

        messagebox.showinfo("FFMPEG", "FFMPEG has been installed in the app root!")

    except Exception as e:
        messagebox.showerror("FFMPEG Install Error", str(e))

def check_ffmpeg_button():
    try:
        if check_ffmpeg():
            messagebox.showinfo("FFMPEG", "FFMPEG is already installed!")
        else:
            if messagebox.askyesno("FFMPEG", "FFMPEG not found. Install it now?"):
                install_ffmpeg()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check/install FFMPEG:\n{e}")

# ---------- GUI ----------
app = tk.Tk()
app.title("yt-dlp Script Launcher")
app.geometry("420x500")
app.resizable(False, False)

header_frame = tk.Frame(app)
header_frame.pack(pady=(10, 4))
tk.Label(header_frame, text="Foofie's yt-dlp scripts launcher", font=("Segoe UI", 14, "bold")).pack(side="left", padx=(0,10))
tk.Button(header_frame, text="Tips", command=show_tips, width=6).pack(side="left")

tk.Label(app, text="Click a button below to run the desired script.\nThe EXIT command is case sensitive!",
         font=font.Font(family="Segoe UI", size=9), fg="#555").pack(pady=(0, 10))

# Script buttons
if os.path.exists(SCRIPTS_FOLDER):
    scripts = [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".bat")]
    if scripts:
        for script in scripts:
            tk.Button(app, text=script.replace(".bat",""), width=46,
                      command=lambda s=script: run_script(s)).pack(pady=4)
    else:
        tk.Label(app, text="No .bat files found.").pack(pady=20)
else:
    tk.Label(app, text="Scripts folder not found.").pack(pady=20)

# Footer
footer_frame = tk.Frame(app)
footer_frame.pack(side="bottom", pady=10)

tk.Button(footer_frame, text="Credits", command=show_credits, width=10).pack(side="left", padx=5)
tk.Button(footer_frame, text="Docs", command=lambda: webbrowser.open_new(
    "https://github.com/Foofiewastaken/yt-dlp-gui"), width=10).pack(side="left", padx=5)
tk.Button(footer_frame, text="Check for FFMPEG", command=check_ffmpeg_button, width=15).pack(side="left", padx=5)

app.mainloop()
