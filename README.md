# 🎵 YT Audio Converter Pro - Ultimate YouTube to MP3 Downloader

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-Open%20Source-green.svg)

**YT Audio Converter Pro** is a powerful, open-source desktop application designed to download and convert YouTube videos into high-fidelity audio files. Unlike simple downloaders, this tool acts as a complete audio processing suite: it downloads playlists in parallel, normalizes volume to professional radio standards, removes non-music segments (SponsorBlock), and embeds high-quality metadata.

Built with **Python** and **CustomTkinter**, it offers a modern, dark-mode GUI that looks great on both Linux and Windows.

![Logo](ytdown.png)

---

## 🌟 Why Choose YT Audio Converter Pro?

This isn't just another downloader. It's built for audiophiles and power users who want a clean, organized, and high-quality music library.

### 🚀 Ultra-Fast Performance
*   **Parallel Playlist Downloading:** Downloads up to **5 videos simultaneously**, drastically reducing wait times for large playlists.
*   **Multi-threaded Acceleration:** Uses concurrent fragment downloading for individual videos to maximize your bandwidth.

### 💿 Studio-Grade Audio Quality
*   **Enforced High Fidelity:** Automatically converts all downloads to **320kbps MP3/AAC/OGG** and **44.1kHz** sample rate.
*   **Crystal Clear Sound:** No upscaling, just the best possible audio stream extracted and processed.

### 🔊 Professional Audio Normalization
*   **EBU R128 Standard:** Normalizes all tracks to **-13 LUFS**, ensuring consistent volume across your entire library.
*   **Dynamic Range Compression:** Intelligently balances quiet and loud parts (Loudness Range Target: 7.0).
*   **True Peak Limiting:** Prevents clipping and distortion (-1.0 dBTP), so your music sounds perfect on any sound system.

### ✂️ Smart Mode (SponsorBlock)
*   **Automatic Editing:** Detects and removes intros, outros, self-promotions, interaction reminders, and non-music sections.
*   **Pure Music:** You get the song, and nothing else.

### 🖼️ Complete Metadata Management
*   **Auto-Tagging:** Automatically fetches and embeds **Artist**, **Title**, and **Album Art**.
*   **Cover Art:** High-resolution thumbnails are embedded directly into the audio file.

### 🌍 Global Language Support
Automatically detects your system language. Supported localizations:
🇬🇧 English | 🇭🇺 Hungarian | 🇩🇪 German | 🇷🇺 Russian | 🇸🇪 Swedish | 🇳🇴 Norwegian | 🇮🇹 Italian | 🇪🇸 Spanish | 🇫🇷 French | 🇸🇰 Slovak | 🇷🇴 Romanian | 🇭🇷 Croatian | 🇹🇷 Turkish | 🇬🇷 Greek

---

## 📥 Installation Guide

### 🐧 Linux (Debian / Ubuntu / Linux Mint)

We provide a native `.deb` package for easy installation.

1.  **Download** the latest release: `ytdownmp3_2.0.0_amd64.deb`
2.  **Install** via terminal:
    ```bash
    sudo dpkg -i ytdownmp3_2.0.0_amd64.deb
    sudo apt-get install -f  # Fixes any missing dependencies (ffmpeg, python3)
    ```
3.  **Run:** Search for "YT Audio Converter Pro" in your application menu.

### 🪟 Windows

1.  **Prerequisites:**
    *   Install [Python 3.10+](https://www.python.org/downloads/).
    *   Install [FFmpeg](https://ffmpeg.org/download.html) and add it to your System PATH.
2.  **Run:**
    *   Double-click `run.bat` to automatically install dependencies and start the app.
    *   *Or build your own executable (see below).*

---

## 🛠️ Developer & Build Instructions

Want to contribute or build from source? Follow these steps.

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Szaturnusz/YTDownMP3.git
cd YTDownMP3

# Create a virtual environment
python3 -m venv .venv

# Activate the environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Building the Packages

#### 📦 Linux (.deb Package)
This script uses PyInstaller to create a single-file binary and then wraps it into a Debian package structure.

```bash
python3 build_linux.py
```
*   **Output:** `ytdownmp3_2.0.0_amd64.deb` (in the project root)

#### 📦 Windows (.exe Executable)
This script creates a standalone `.exe` file.

```cmd
build_windows.bat
```
*   **Output:** `dist/ytdownmp3.exe`

---

## 🔧 Tech Stack

*   **Language:** Python 3.12
*   **GUI:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern UI)
*   **Core Engine:** [yt-dlp](https://github.com/yt-dlp/yt-dlp) (YouTube downloading)
*   **Audio Processing:** [ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) & [FFmpeg](https://ffmpeg.org/)
*   **Packaging:** PyInstaller, dpkg-deb

---

## 📝 License

This project is open-source software. Feel free to fork, modify, and distribute.

**Created by:** Szaturnusz
**Current Version:** 2.0.0


