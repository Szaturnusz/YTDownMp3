#!/usr/bin/env python3
import os
import sys
import threading
import subprocess
import platform
import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
from ffmpeg_normalize import FFmpegNormalize
from localization import TRANSLATIONS, get_system_language

# Megjelenés beállítása
ctk.set_appearance_mode("Dark")  # Sötét mód a pro hatásért
ctk.set_default_color_theme("dark-blue")

class YouTubeConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Nyelv beállítása
        self.lang_code = get_system_language()
        # Ha nincs a listában, angol az alapértelmezett
        self.t = TRANSLATIONS.get(self.lang_code, TRANSLATIONS["en"])

        # Ablak beállításai
        self.title(self.t["title"])
        self.geometry("700x550")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Fő keret (Kártya stílus)
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(6, weight=1) # A log mező nyúljon meg (most már a 6. sorban van)

        # Fejléc
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Bal oldali szövegdoboz (Cím + Alcím egymás alatt)
        self.title_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.title_container.pack(side="left")

        self.label_title = ctk.CTkLabel(self.title_container, text=self.t["title"], font=ctk.CTkFont(family="Roboto", size=28, weight="bold"))
        self.label_title.pack(anchor="w")
        
        self.label_subtitle = ctk.CTkLabel(self.title_container, text=self.t["subtitle"], font=ctk.CTkFont(family="Roboto", size=14), text_color="gray")
        self.label_subtitle.pack(anchor="w")

        # Jobb oldali gomb
        self.btn_update = ctk.CTkButton(self.header_frame, text=self.t["update_btn"], width=100, height=25, fg_color="gray30", command=self.update_engine)
        self.btn_update.pack(side="right", pady=5)

        # Input Szekció (Külön keretben)
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color=("gray90", "gray16"), corner_radius=10)
        self.input_frame.grid(row=1, column=0, padx=30, pady=15, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry_url = ctk.CTkEntry(self.input_frame, placeholder_text=self.t["url_placeholder"], height=40, border_width=0, fg_color="transparent")
        self.entry_url.grid(row=0, column=0, padx=15, pady=10, sticky="ew")

        self.btn_paste = ctk.CTkButton(self.input_frame, text=self.t["paste_btn"], width=80, height=30, fg_color="gray25", hover_color="gray30", command=self.paste_from_clipboard)
        self.btn_paste.grid(row=0, column=1, padx=10, pady=10)

        # Beállítások Szekció (Formátum + Mappa)
        self.settings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.settings_frame.grid(row=2, column=0, padx=30, pady=5, sticky="ew")
        
        # Bal oldal: Formátum
        self.label_format = ctk.CTkLabel(self.settings_frame, text=self.t["format_label"], font=ctk.CTkFont(weight="bold"))
        self.label_format.pack(side="left", padx=(0, 10))
        
        self.option_format = ctk.CTkSegmentedButton(self.settings_frame, values=["MP3", "OGG", "AAC"])
        self.option_format.pack(side="left")
        self.option_format.set("MP3")

        # Jobb oldal: Mappa
        self.btn_browse = ctk.CTkButton(self.settings_frame, text=self.t["save_to_btn"], width=100, height=30, fg_color="gray30", command=self.browse_folder)
        self.btn_browse.pack(side="right", padx=(10, 0))

        self.label_folder = ctk.CTkLabel(self.settings_frame, text="downloads/", text_color="gray")
        self.label_folder.pack(side="right")

        # Minőség választó (ÚJ)
        self.quality_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.quality_frame.grid(row=3, column=0, padx=30, pady=5, sticky="ew")

        self.label_quality = ctk.CTkLabel(self.quality_frame, text=self.t["quality_label"], font=ctk.CTkFont(weight="bold"))
        self.label_quality.pack(side="left", padx=(0, 10))

        self.option_quality = ctk.CTkOptionMenu(self.quality_frame, values=["320 kbps (Studio)", "192 kbps (High)", "128 kbps (Normal)"], width=150)
        self.option_quality.pack(side="left")
        self.option_quality.set("320 kbps (Studio)")

        # Smart Mode (ÚJ)
        self.switch_smart = ctk.CTkSwitch(self.quality_frame, text=self.t["smart_mode"], onvalue=True, offvalue=False)
        self.switch_smart.pack(side="right", padx=(10, 0))
        self.switch_smart.select() # Alapból bekapcsolva

        # Akció Gomb
        self.btn_download = ctk.CTkButton(self.main_frame, text=self.t["download_btn"], height=50, font=ctk.CTkFont(size=16, weight="bold"), corner_radius=25, command=self.start_download_thread)
        self.btn_download.grid(row=4, column=0, padx=30, pady=20, sticky="ew")

        # Progress Bar (ÚJ)
        self.progressbar = ctk.CTkProgressBar(self.main_frame, height=15)
        self.progressbar.grid(row=5, column=0, padx=30, pady=(0, 10), sticky="ew")
        self.progressbar.set(0)

        # Log / Státusz Szekció
        self.log_frame = ctk.CTkFrame(self.main_frame, fg_color=("gray95", "black"), corner_radius=10)
        self.log_frame.grid(row=6, column=0, padx=30, pady=(0, 30), sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(0, weight=1)

        self.textbox_log = ctk.CTkTextbox(self.log_frame, font=ctk.CTkFont(family="Consolas", size=12), fg_color="transparent", text_color="green")
        self.textbox_log.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox_log.configure(state="disabled")

        # Mappa megnyitása gomb (Log kereten belül jobb alulra vagy mellé)
        self.btn_open_folder = ctk.CTkButton(self.log_frame, text=self.t["open_folder_btn"], width=100, height=25, fg_color="gray20", command=self.open_download_folder)
        self.btn_open_folder.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")

        self.download_folder = self.get_default_download_folder()
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            
        # Frissítjük a címkét az alapértelmezett mappával
        display_name = os.path.basename(self.download_folder)
        self.label_folder.configure(text=f".../{display_name}")

    def get_default_download_folder(self):
        home = os.path.expanduser("~")
        # Próbáljuk meg a magyar "Letöltések" mappát
        hungarian_downloads = os.path.join(home, "Letöltések")
        if os.path.exists(hungarian_downloads):
            return os.path.join(hungarian_downloads, "YT_Music")
        
        # Ha nincs, akkor a szabványos "Downloads"
        standard_downloads = os.path.join(home, "Downloads")
        return os.path.join(standard_downloads, "YT_Music")

    def open_download_folder(self):
        path = self.download_folder
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                self.log(self.t["folder_create_error"])
                return

        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                # Linux: xdg-open csendes módban, hogy ne spammelje a terminált
                subprocess.Popen(["xdg-open", path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except Exception as e:
            self.log(self.t["folder_open_error"].format(e))

    def update_engine(self):
        self.log(self.t["update_start"])
        def run_update():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
                self.log(self.t["update_success"])
            except Exception as e:
                self.log(self.t["update_error"].format(e))
        
        threading.Thread(target=run_update).start()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_folder = folder
            # Rövidített megjelenítés
            display_name = os.path.basename(folder)
            if not display_name: display_name = folder 
            self.label_folder.configure(text=f".../{display_name}")
            self.log(self.t["save_location"].format(folder))

    def paste_from_clipboard(self):
        try:
            # Próbáljuk meg a vágólap tartalmát beilleszteni
            content = self.clipboard_get()
            self.entry_url.delete(0, "end")
            self.entry_url.insert(0, content)
        except Exception as e:
            self.log(self.t["paste_error"].format(e))


    def log(self, message):
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", message + "\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                self.progressbar.set(float(p) / 100)
            except:
                pass
        elif d['status'] == 'finished':
            self.progressbar.set(1)
            self.log(self.t["download_ready"])

    def start_download_thread(self):
        url = self.entry_url.get().strip()
        fmt = self.option_format.get().lower()
        quality = self.option_quality.get().split()[0] # "320", "192", "128"
        smart_mode = self.switch_smart.get()
        
        if not url:
            self.log(self.t["error_no_link"])
            return

        self.btn_download.configure(state="disabled")
        self.progressbar.set(0)
        self.log(self.t["start_log"].format(url, fmt.upper(), quality))
        if smart_mode: self.log(self.t["smart_mode_log"])
        
        # Külön szálon futtatjuk, hogy ne fagyjon le az ablak
        thread = threading.Thread(target=self.process_video, args=(url, fmt, quality, smart_mode))
        thread.start()

    def process_video(self, url, fmt, quality, smart_mode):
        try:
            # 1. Letöltés
            self.log(self.t["download_meta_log"])
            files = self.download_audio(url, fmt, quality, smart_mode)
            
            if not files:
                self.log(self.t["download_fail_log"])
                return

            # 2. Normalizálás minden fájlra
            count = len(files)
            self.log(self.t["norm_start_log"].format(count))
            
            for i, filename in enumerate(files):
                self.log(self.t["norm_item_log"].format(i+1, count, os.path.basename(filename)))
                self.normalize_audio(filename, fmt)
            
            self.log("-" * 30)
            self.log(self.t["success_log"])
            self.progressbar.set(0)
            
            # Opcionális: Mappa megnyitása automatikusan?
            # self.open_download_folder()

        except Exception as e:
            self.log(self.t["critical_error"].format(str(e)))
        finally:
            self.btn_download.configure(state="normal")

    def download_audio(self, url, fmt, quality, smart_mode):
        # Formátum leképezése yt-dlp codec-re
        codec_map = {
            "mp3": "mp3",
            "ogg": "vorbis",
            "aac": "aac"
        }
        preferred_codec = codec_map.get(fmt, "mp3")

        postprocessors = [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': preferred_codec,
                'preferredquality': quality,
            },
            {'key': 'EmbedThumbnail'}, # Borítókép beágyazása
            {'key': 'FFmpegMetadata'}, # Metadata (cím, előadó) beágyazása
        ]

        if smart_mode:
            # Smart Mode: SponsorBlock integráció a felesleg kivágására
            categories = ['intro', 'outro', 'selfpromo', 'interaction', 'music_offtopic']
            postprocessors.append({
                'key': 'SponsorBlock',
                'categories': categories,
            })
            postprocessors.append({
                'key': 'ModifyChapters',
                'remove_sponsor_segments': categories,
            })

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.download_folder}/%(title)s.%(ext)s',
            'writethumbnail': True, # Borítókép letöltése
            'postprocessors': postprocessors,
            'progress_hooks': [self.progress_hook], # Progress bar frissítése
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True, # Playlistnél ne álljon meg egy hiba miatt
        }

        downloaded_files = []

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Először lekérjük az infót, hogy tudjuk, playlist-e
            try:
                info = ydl.extract_info(url, download=True)
            except Exception as e:
                self.log(self.t["download_error"].format(e))
                return []

            if 'entries' in info:
                # Ez egy Playlist
                self.log(self.t["playlist_detected"].format(info.get('title')))
                for entry in info['entries']:
                    if entry:
                        filename = ydl.prepare_filename(entry)
                        final_filename = self._get_final_filename(filename, fmt)
                        downloaded_files.append(final_filename)
            else:
                # Ez egy sima videó
                filename = ydl.prepare_filename(info)
                final_filename = self._get_final_filename(filename, fmt)
                downloaded_files.append(final_filename)
            
        return downloaded_files

    def _get_final_filename(self, filename, fmt):
        base, _ = os.path.splitext(filename)
        if fmt == "mp3":
            return base + ".mp3"
        elif fmt == "ogg":
            return base + ".ogg"
        elif fmt == "aac":
            # Az aac codec gyakran m4a konténerbe kerül
            m4a = base + ".m4a"
            if os.path.exists(m4a): return m4a
            return base + ".aac"
        return base + ".mp3"

    def normalize_audio(self, input_file, fmt):
        output_file = os.path.splitext(input_file)[0] + "_temp" + os.path.splitext(input_file)[1]
        
        # Codec kiválasztása a normalizáláshoz
        ffmpeg_codec = 'libmp3lame' # alapértelmezett
        if fmt == 'ogg':
            ffmpeg_codec = 'libvorbis'
        elif fmt == 'aac':
            ffmpeg_codec = 'aac'
        
        normalizer = FFmpegNormalize(
            target_level=-14,
            print_stats=False,
            debug=False,
            progress=False,
            audio_codec=ffmpeg_codec
        )
        
        try:
            normalizer.add_media_file(input_file, output_file)
            normalizer.run_normalization()
            
            os.replace(output_file, input_file)
            return input_file
        except Exception as e:
            self.log(self.t["norm_error"].format(e))
            if os.path.exists(output_file):
                os.remove(output_file)
            return None

if __name__ == "__main__":
    app = YouTubeConverterApp()
    app.mainloop()
