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
import threading

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

# ---------- Open Downloads ----------
def open_downloads():
    downloads_folder = os.path.join(APP_DIR, "Downloads")
    if os.path.exists(downloads_folder) and os.listdir(downloads_folder):
        if platform.system() == "Windows":
            os.startfile(downloads_folder)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", downloads_folder])
        else:  # Linux
            subprocess.Popen(["xdg-open", downloads_folder])
    else:
        messagebox.showinfo("No Downloads", "You haven't downloaded anything yet")

# ---------- Tips ----------
def show_tips():
    top = tk.Toplevel(app)
    top.title("Tips")
    top.resizable(False, False)
    top.configure(bg="black")

    txt = tk.Text(top, wrap="word", width=72, height=13, padx=10, pady=10, borderwidth=0,
                   bg="black", fg="white", insertbackground="white")
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

    tk.Button(top, text="OK", command=top.destroy, fg="white", bg="#333").pack(pady=(6, 10))
    top.transient(app)
    top.grab_set()
    app.wait_window(top)

# ---------- Credits ----------
def show_credits():
    top = tk.Toplevel(app)
    top.title("Credits")
    top.geometry("400x215")
    top.resizable(False, False)
    top.configure(bg="black")

    tk.Label(top, text="Scripts and GUI made by Foofie.\nIf obtained elsewhere, might be a virus.\n\n"
                        "Discord: .foofie\nTelegram: @Foofie_UwU\nGitHub: Click Docs button",
             font=("Segoe UI", 12), justify="center", fg="white", bg="black").pack(pady=20)
    tk.Button(top, text="OK", command=top.destroy, fg="white", bg="#333").pack(pady=10)
    top.transient(app)
    top.grab_set()
    app.wait_window(top)

# ---------- FFMPEG Functions ----------
FFMPEG_PATH = os.path.join(APP_DIR, "ffmpeg.exe")

def check_ffmpeg():
    if os.path.exists(FFMPEG_PATH):
        return True
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ffmpeg():
    system = platform.system()
    if system != "Windows":
        raise RuntimeError("Auto-install only implemented for Windows.")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(APP_DIR, "ffmpeg.zip")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(APP_DIR)
    os.remove(zip_path)
    for root_dir, dirs, files in os.walk(APP_DIR):
        if "ffmpeg.exe" in files:
            shutil.copy(os.path.join(root_dir, "ffmpeg.exe"), FFMPEG_PATH)
            break
    for folder in os.listdir(APP_DIR):
        if folder.startswith("ffmpeg-") and os.path.isdir(os.path.join(APP_DIR, folder)):
            shutil.rmtree(os.path.join(APP_DIR, folder))

def download_ffmpeg_thread(top):
    try:
        install_ffmpeg()
        top.destroy()
        messagebox.showinfo("FFMPEG Installed", "FFMPEG has been successfully installed!")
    except Exception as e:
        top.destroy()
        messagebox.showerror("FFMPEG Install Error", f"Installation failed:\n{e}")
        app.destroy()

def check_ffmpeg_startup():
    if check_ffmpeg():
        return
    top = tk.Toplevel(app)
    top.title("FFMPEG not found")
    top.resizable(False, False)
    top.configure(bg="black")
    label = tk.Label(top, text="FFMPEG was not detected.\nDo you want to download and install it now?",
                     fg="white", bg="black", font=("Segoe UI", 10), justify="center")
    label.pack(padx=20, pady=20)
    top.protocol("WM_DELETE_WINDOW", lambda: None)
    top.transient(app)
    top.grab_set()
    app.update()

    def start_download():
        label.config(text="Downloading and installing FFMPEG, please wait...")
        for widget in btn_frame.winfo_children():
            widget.pack_forget()
        threading.Thread(target=download_ffmpeg_thread, args=(top,), daemon=True).start()

    def exit_app():
        app.destroy()

    btn_frame = tk.Frame(top, bg="black")
    btn_frame.pack(pady=(0,20))
    tk.Button(btn_frame, text="Download", command=start_download, fg="white", bg="#333", width=10).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Exit", command=exit_app, fg="white", bg="#333", width=10).pack(side="left", padx=10)

# ---------- GUI ----------
app = tk.Tk()
app.title("Foofie's video Script Launcher")
app.geometry("360x280")
app.resizable(False, False)
app.configure(bg="black")

header_frame = tk.Frame(app, bg="black")
header_frame.pack(pady=(10, 4))
tk.Label(header_frame, text="Foofie's video scripts launcher",
         font=("Segoe UI", 14, "bold"), fg="white", bg="black").pack(side="left")

tk.Label(app, text="Click a button below to run the desired script.",
         font=font.Font(family="Segoe UI", size=9), fg="white", bg="black").pack(pady=(0, 10))

# ---------- List scripts ----------
if os.path.exists(SCRIPTS_FOLDER):
    scripts = [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".bat")]
    if scripts:
        for script in scripts:
            tk.Button(app, text=script.replace(".bat",""), width=46,
                      command=lambda s=script: run_script(s),
                      fg="white", bg="#333").pack(pady=4)
    else:
        tk.Label(app, text="No .bat files found.", fg="white", bg="black").pack(pady=20)
else:
    tk.Label(app, text="Scripts folder not found.", fg="white", bg="black").pack(pady=20)

# ---------- Downloads button below scripts ----------
tk.Button(app, text="Open Downloads", width=46, command=open_downloads, fg="white", bg="#242424").pack(pady=6)

# ---------- Footer ----------
footer_frame = tk.Frame(app, bg="black")
footer_frame.pack(side="bottom", pady=10)

tk.Button(footer_frame, text="Tips", command=show_tips, width=10, fg="white", bg="#333").pack(side="left", padx=5)
tk.Button(footer_frame, text="Credits", command=show_credits, width=10, fg="white", bg="#333").pack(side="left", padx=5)
tk.Button(footer_frame, text="Docs", command=lambda: webbrowser.open_new(
    "https://github.com/Foofiewastaken/yt-dlp-gui"), width=10, fg="white", bg="#333").pack(side="left", padx=5)

app.after(100, check_ffmpeg_startup)
app.mainloop()
