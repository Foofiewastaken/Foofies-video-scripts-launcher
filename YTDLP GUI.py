import os
import subprocess
import tkinter as tk
from tkinter import messagebox, font
import webbrowser

# ---------- App setup ----------
SCRIPTS_FOLDER = os.path.join(os.getcwd(), "ScriptsNDownloads")

def run_script(script_name):
    path = os.path.join(SCRIPTS_FOLDER, script_name)
    if os.path.exists(path):
        subprocess.Popen(['cmd', '/c', 'start', '', path], shell=True)
    else:
        messagebox.showerror("Error", f"Script not found:\n{path}")

# ---------- Tips function with hyperlink ----------
def show_tips():
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()

    top = tk.Toplevel(root)
    top.title("Tips")
    top.resizable(False, False)

    txt = tk.Text(top, wrap="word", width=72, height=18, padx=10, pady=10, borderwidth=0)
    txt.insert("end",
        "If a video is restricted or you get a cookies error:\n\n"
        "1. Export your browser cookies file (www.youtube.com_cookies.txt or music.youtube.com_cookies.txt). "
        "Best way to do this, is by "
    )

    # Add hyperlink
    start_index = txt.index("end-1c")
    txt.insert("end", "downloading this extension")
    end_index = txt.index("end-1c")
    txt.insert("end",
        ". \n" 
        "2. Open the extension in Youtube, and click export. \n"
        "3. Move the cookies from Downloads to the 'ScriptsNDownloads' folder.\n"
        "4. Rerun the script.\n\n"
        "Cookies have to be named www.youtube.com_cookies.txt or music.youtube.com_cookies.txt, "
        "because the scripts expect such names! \n\n\n"
        "If you want to add more scripts, put them in the 'ScriptsNDownloads' folder. All your downloads will also be there!"
    )

    txt.tag_add("link", start_index, end_index)
    txt.tag_config("link", foreground="blue", underline=1)
    txt.tag_bind("link", "<Button-1>", lambda e: webbrowser.open_new(
        "https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
    ))

    txt.config(state="disabled")
    txt.pack(fill="both", expand=True)

    btn = tk.Button(top, text="OK", command=top.destroy)
    btn.pack(pady=(6, 10))

    top.transient(root)
    top.grab_set()
    root.wait_window(top)

# ---------- Credits function (empty window for now) ----------
def show_credits():
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()

    top = tk.Toplevel(root)
    top.title("Credits")
    top.geometry("400x200")
    tk.Label(top, text="The scripts and this GUI is all made by Foofie. \n If you got this app from anywhere aside from me directly, \n or my github, it might be a virus! \n\n My socials are: \n Discord: .foofie \n Telegram @Foofie_UwU \n Git-Hub: not yet made", font=("Segoe UI", 12)).pack(pady=20)

    btn = tk.Button(top, text="OK", command=top.destroy)
    btn.pack(pady=10)

    top.transient(root)
    top.grab_set()
    root.wait_window(top)

# ---------- GUI ----------
app = tk.Tk()
app.title("yt-dlp Script Launcher")
app.geometry("420x500")

# Title + Tips button on same line
header_frame = tk.Frame(app)
header_frame.pack(pady=(10, 4))

title = tk.Label(header_frame, text="Foofie's yt-dlp scripts launcher", font=("Segoe UI", 14, "bold"))
title.pack(side="left", padx=(0, 10))

tips_button = tk.Button(header_frame, text="Tips", command=show_tips, width=6)
tips_button.pack(side="left")

# Small subtext below
sub_font = font.Font(family="Segoe UI", size=9)
tk.Label(
    app,
    text="Click a button below to run the desired script.",
    font=sub_font, fg="#555"
).pack(pady=(0, 10))

# Script buttons
if os.path.exists(SCRIPTS_FOLDER):
    scripts = [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".bat")]
    if scripts:
        for script in scripts:
            tk.Button(
                app, text=script.replace(".bat", ""), width=46,
                command=lambda s=script: run_script(s)
            ).pack(pady=4)
    else:
        tk.Label(app, text="No .bat files found.").pack(pady=20)
else:
    tk.Label(app, text="ScriptsNDownloads folder not found.").pack(pady=20)

# Footer frame with Credits and Docs buttons
footer_frame = tk.Frame(app)
footer_frame.pack(side="bottom", pady=10)

credits_button = tk.Button(footer_frame, text="Credits", command=show_credits, width=10)
credits_button.pack(side="left", padx=5)

def open_docs():
    webbrowser.open_new("https://github.com/Foofiewastaken/yt-dlp-gui")  # docs link

docs_button = tk.Button(footer_frame, text="Docs", command=open_docs, width=10)
docs_button.pack(side="left", padx=5)

app.mainloop()

