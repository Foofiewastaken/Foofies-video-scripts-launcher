import subprocess
import sys
import os
import shutil
import traceback

try:
    # Name of your script
    script_name = "YTDLP GUI.py"  # <-- change if needed
    exe_name = os.path.splitext(script_name)[0] + ".exe"  # "YTDLP GUI.exe"

    # Ensure we are in the script folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 1. Ensure PyInstaller is installed
    try:
        import PyInstaller  # noqa
    except ImportError:
        print("PyInstaller not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Build the exe
    print(f"Building {script_name} into an exe (app will be terminal-less)...")

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--noconsole",  # hide console for app
        script_name
    ]

    subprocess.run(cmd, check=True)

    # 3. Optional cleanup of build folders
    for folder in ["build", f"{os.path.splitext(script_name)[0]}.spec"]:
        if os.path.exists(folder):
            try:
                if os.path.isdir(folder):
                    shutil.rmtree(folder)
                else:
                    os.remove(folder)
            except Exception as e:
                print(f"Warning: could not remove {folder}: {e}")

    # 4. Move the exe from dist to root, replacing old one
    dist_path = os.path.join("dist", exe_name)
    root_path = os.path.join(os.getcwd(), exe_name)
    if os.path.exists(dist_path):
        print(f"Moving {exe_name} from 'dist' to root folder...")
        shutil.move(dist_path, root_path)
        # Optional: remove dist folder if empty
        try:
            os.rmdir("dist")
        except OSError:
            pass
    else:
        print(f"❌ Could not find {exe_name} in 'dist' folder!")

    print("\n✅ Build complete! Your EXE is now in the root folder.")

except Exception:
    print("\n❌ An error occurred:\n")
    traceback.print_exc()

finally:
    # Keep the builder window open
    os.system("pause")
