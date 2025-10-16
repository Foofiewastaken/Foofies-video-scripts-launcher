import subprocess
import sys
import os
import shutil
import traceback

try:
    # Name of your script
    script_name = "Scripts Launcher.py"
    exe_name = os.path.splitext(script_name)[0] + ".exe"

    # Ensure we are in the script folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Absolute paths for script and icon
    script_path = os.path.abspath(script_name)
    icon_file = "downico.ico"
    icon_path = os.path.abspath(icon_file) if os.path.exists(icon_file) else None

    if icon_path is None:
        print(f"Warning: Icon file '{icon_file}' not found. Default icon will be used.")

    # Ensure PyInstaller is installed
    try:
        import PyInstaller  # noqa
    except ImportError:
        print("PyInstaller not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Remove old builds/spec/dist first
    for item in ["build", "dist", os.path.splitext(script_name)[0] + ".spec"]:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
            except Exception as e:
                print(f"Warning: could not remove {item}: {e}")

    # Build the exe
    print(f"Building '{script_name}' into a onefile exe (terminal-less)...")

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",      # single exe
        "--noconsole",    # hide console
    ]

    if icon_path:
        cmd.append(f'--icon="{icon_path}"')

    cmd.append(f'"{script_path}"')

    # Use shell=True to correctly handle quotes and spaces
    subprocess.run(" ".join(cmd), shell=True, check=True)

    # Move the exe from dist to root
    dist_path = os.path.join("dist", exe_name)
    root_path = os.path.join(os.getcwd(), exe_name)
    if os.path.exists(dist_path):
        shutil.move(dist_path, root_path)
        print(f"Moved '{exe_name}' to root folder.")

    # Post-build cleanup
    for folder in ["build", "dist"]:
        if os.path.exists(folder) and os.path.isdir(folder):
            try:
                shutil.rmtree(folder)
            except Exception:
                pass
    spec_file = os.path.splitext(script_name)[0] + ".spec"
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
        except Exception:
            pass

    print("\n✅ Build complete! EXE is in the root folder.")

except Exception:
    print("\n❌ An error occurred:\n")
    traceback.print_exc()

finally:
    os.system("pause")
