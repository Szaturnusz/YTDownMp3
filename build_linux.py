import os
import subprocess
import shutil
import customtkinter
import sys

APP_NAME = "YTDownMP3"
BINARY_NAME = "ytdownmp3"
VERSION = "2.0.0"
DESCRIPTION = "YouTube to MP3 Converter Pro"
MAINTAINER = "Szaturnusz"
ICON_PATH = "ytdown.png"

def get_customtkinter_path():
    return os.path.dirname(customtkinter.__file__)

def build_binary():
    print("Building binary with PyInstaller...")
    ctk_path = get_customtkinter_path()
    
    # PyInstaller arguments
    args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", BINARY_NAME,
        "--icon", ICON_PATH,
        "--add-data", f"{ctk_path}:customtkinter",
        "--add-data", "localization.py:.",
        "--add-data", "ytdown.png:.",
        "--hidden-import", "PIL._tkinter_finder",
        "main.py"
    ]
    
    subprocess.check_call(args)

def create_deb_structure():
    print("Creating Debian package structure...")
    base_dir = "deb_dist"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    
    # Directories
    os.makedirs(f"{base_dir}/DEBIAN")
    os.makedirs(f"{base_dir}/usr/local/bin")
    os.makedirs(f"{base_dir}/usr/share/applications")
    os.makedirs(f"{base_dir}/usr/share/icons/hicolor/256x256/apps")
    
    # Copy Binary
    shutil.copy(f"dist/{BINARY_NAME}", f"{base_dir}/usr/local/bin/{BINARY_NAME}")
    os.chmod(f"{base_dir}/usr/local/bin/{BINARY_NAME}", 0o755)
    
    # Copy Icon
    shutil.copy(ICON_PATH, f"{base_dir}/usr/share/icons/hicolor/256x256/apps/{BINARY_NAME}.png")
    
    # Create Control File
    control_content = f"""Package: {BINARY_NAME}
Version: {VERSION}
Section: utils
Priority: optional
Architecture: amd64
Depends: ffmpeg, python3
Maintainer: {MAINTAINER}
Description: {DESCRIPTION}
 A professional YouTube to MP3 converter with GUI.
"""
    with open(f"{base_dir}/DEBIAN/control", "w") as f:
        f.write(control_content)
        
    # Create Desktop Entry
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={APP_NAME}
Comment={DESCRIPTION}
Exec=/usr/local/bin/{BINARY_NAME}
Icon={BINARY_NAME}
Terminal=false
Categories=AudioVideo;Audio;
"""
    with open(f"{base_dir}/usr/share/applications/{BINARY_NAME}.desktop", "w") as f:
        f.write(desktop_content)
        
    return base_dir

def build_deb(dist_dir):
    print("Building .deb package...")
    subprocess.check_call(["dpkg-deb", "--build", dist_dir, f"{BINARY_NAME}_{VERSION}_amd64.deb"])
    print(f"Package created: {BINARY_NAME}_{VERSION}_amd64.deb")

if __name__ == "__main__":
    # Ensure we are in the right directory
    if not os.path.exists("main.py"):
        print("Error: main.py not found. Run this script from the project root.")
        sys.exit(1)
        
    try:
        build_binary()
        dist_dir = create_deb_structure()
        build_deb(dist_dir)
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")
