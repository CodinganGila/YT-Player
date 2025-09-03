import os
import subprocess
import re
import random
import glob
import shutil    
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Warna ANSI
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def clear():
    os.system("clear")
    
def get_direct_url(url, fmt="bestaudio"):
    try:
        return subprocess.check_output(
            ["yt-dlp", "-f", fmt, "--get-url", url],
            text=True
        ).strip()
    except subprocess.CalledProcessError:
        return None


def tampil_kontrol():
    print(f"""{CYAN}
═════════════════════════════════════════════════════════
{BOLD}{GREEN} Kontrol Pemutaran MPV {RESET}{CYAN}
═════════════════════════════════════════════════════════
{YELLOW}► [←]  Seek -5 detik        [→]  Seek +5 detik
► [↑]  Seek +1 menit        [↓]  Seek -1 menit

► [0]  Volume +2%           [9]  Volume -2%

► [<] Previous              [>]  Next
► [SPACE] Play / Pause      [q]  Berhenti & Keluar{RESET}
{CYAN}═════════════════════════════════════════════════════════{RESET}
""")

def menu():
    clear()
    print(f"""{BOLD}{CYAN}
╔══════════════════════════════════════╗
║      🎵  {MAGENTA}Pemutar Musik YouTube{CYAN}       ║
╠══════════════════════════════════════╣
║ {YELLOW}1. {CYAN} Play Music Youtube               ║
║ {YELLOW}2. {CYAN} Play Mix Youtube                 ║
║ {YELLOW}3. {CYAN} Play Playlist Youtube            ║
║ {YELLOW}4. {CYAN} Play Music Spotify               ║
║ {YELLOW}5. {CYAN} Download Audio Youtube           ║
║ {YELLOW}6. {CYAN} Download Video Youtube           ║
║ {YELLOW}7. {CYAN} Download Video (All Sites)       ║
║ {YELLOW}8. {CYAN} Download Audio (All Sites)       ║
║ {YELLOW}9. {CYAN} Download Photo (All Sites)       ║
║ {YELLOW}10.{CYAN} Download Music Spotify           ║
║ {YELLOW}11.{CYAN} Update Dependencies              ║
║ {RED}0. {CYAN} Keluar                           ║
╚══════════════════════════════════════╝{RESET}
""")
    return input(f"{BOLD}{GREEN}Pilih opsi: {RESET}")

def tampilkan_hasil(hasil):
    print()
    for i, line in enumerate(hasil, 1):
        print(f"{YELLOW}{i}.{RESET} {line}")
    pilih = input(f"\n{CYAN}Pilih nomor [1-{len(hasil)}] atau Enter untuk batal: {RESET}")
    if pilih.isdigit():
        index = int(pilih)
        if 1 <= index <= len(hasil):
            return hasil[index - 1].split(" | ")[-1]
    return None

def search_youtube(query):
    print(f"\n{CYAN}🔍 Mencari di YouTube...{RESET}")
    try:
        hasil = subprocess.check_output(
            f"yt-dlp 'ytsearch5:{query}' --print '%(title)s | %(webpage_url)s'",
            shell=True
        ).decode().strip().split('\n')
    except subprocess.CalledProcessError:
        print(f"{RED}❌ Gagal mencari.{RESET}")
        return None

    if not hasil:
        print(f"{RED}❌ Tidak ada hasil.{RESET}")
        return None

    return tampilkan_hasil(hasil)

def play_music():
    inp = input(f"\n{GREEN}🎧 Masukkan judul atau link: {RESET}").strip()
    if "youtube.com" in inp or "youtu.be" in inp:
        url = inp
    else:
        url = search_youtube(inp)
        if not url:
            return
    tampil_kontrol()
    print(f"\n{YELLOW}▶️ Memutar musik...{RESET}")
    direct_url = get_direct_url(url)
    if direct_url:
        os.system(f"mpv --no-video '{direct_url}'")
    else:
        print(f"{RED}❌ Gagal memutar musik.{RESET}")

def play_mix_manual():
    judul_awal = input(f"{YELLOW}🎵 Masukkan judul lagu awal: {RESET}").strip()
    try:
        print(f"{CYAN}🔍 Mencari video pertama dari: {judul_awal}{RESET}")
        result = subprocess.check_output(
            f"yt-dlp 'ytsearch1:{judul_awal}' --print '%(title)s|||%(webpage_url)s' -q",
            shell=True
        ).decode().strip()

        judul, url = result.split("|||")
        tampil_kontrol()
        print(f"{GREEN}▶️ Memutar awal (dipercepat): {judul}{RESET}")
        direct_url = get_direct_url(url)
        if direct_url:
            os.system(f"mpv --no-video '{direct_url}'")

        # Loop untuk lagu berikutnya
        while True:
            hasil = subprocess.check_output(
                f"yt-dlp 'ytsearch10:{judul}' --print '%(title)s|||%(webpage_url)s' -q",
                shell=True
            ).decode().strip().split('\n')

            if not hasil:
                print(f"{RED}❌ Tidak ada hasil yang ditemukan.{RESET}")
                break

            acak = random.choice(hasil)  # ambil lagu acak dari hasil pencarian
            judul, url = acak.split("|||")  # update judul & url
            direct_url = get_direct_url(url)

            if direct_url:
                tampil_kontrol()
                print(f"{YELLOW}▶️ Memutar lagu mirip (dipercepat): {judul}{RESET}")
                os.system(f"mpv --no-video '{direct_url}'")

    except KeyboardInterrupt:
        print(f"\n{MAGENTA}⏹️ Dihentikan oleh user.{RESET}")
    except Exception as e:
        print(f"{RED}❌ Terjadi kesalahan: {str(e)}{RESET}")

def play_playlist():
    url = input(f"{YELLOW}📜 Masukkan link playlist YouTube: {RESET}").strip()
    if "playlist" in url or "list=" in url:
        tampil_kontrol()
        print(f"{GREEN}▶️ Memutar playlist...{RESET}")
        try:
            playlist_urls = subprocess.check_output(
                ["yt-dlp", "-f", "bestaudio", "--get-url", url],
                text=True
            ).strip().splitlines()
        
            for direct_url in playlist_urls:
                os.system(f"mpv --no-video '{direct_url}'")
        
        except subprocess.CalledProcessError:
            print(f"{RED}❌ Gagal memutar playlist.{RESET}")
    else:
        print(f"{RED}⚠️  Bukan link playlist yang valid.{RESET}")

def download_audio():
    inp = input(f"\n{GREEN}⬇️ Masukkan judul atau link: {RESET}").strip()
    if "youtube.com" in inp or "youtu.be" in inp:
        url = inp
    else:
        url = search_youtube(inp)
        if not url:
            return

    # Ambil daftar file sebelum download
    before = set(glob.glob("*.mp3"))

    print(f"\n{YELLOW}🎵 Mengunduh audio...{RESET}")
    os.system(f"yt-dlp -x --audio-format mp3 -o '%(title)s.%(ext)s' '{url}'")

    # Ambil daftar file setelah download
    after = set(glob.glob("*.mp3"))
    new_files = after - before

    if new_files:
        os.makedirs("/sdcard/Download/Music", exist_ok=True)
        for file in new_files:
            try:
                shutil.move(file, f"/sdcard/Download/Music/{file}")
                print(f"{GREEN}✅ Dipindahkan: {file}{RESET}")
            except Exception as e:
                print(f"{RED}❌ Gagal pindah {file}: {e}{RESET}")
    else:
        print(f"{RED}❌ Tidak ada file baru untuk dipindahkan.{RESET}")

 
def download_video():
    def resolusi_to_label(res):
        match = re.search(r'(\d+)x(\d+)', res)
        if match:
            height = match.group(2)
            return f"{res} ({height}p)"
        return res

    inp = input(f"\n{GREEN}⬇️ Masukkan judul atau link video: {RESET}").strip()
    if "youtube.com" in inp or "youtu.be" in inp:
        url = inp
    else:
        url = search_youtube(inp)
        if not url:
            return

    print(f"\n{CYAN}📥 Mengambil daftar resolusi video...{RESET}")
    try:
        output = subprocess.check_output(
            f"yt-dlp -F '{url}'",
            shell=True
        ).decode().splitlines()
    except subprocess.CalledProcessError:
        print(f"{RED}❌ Gagal mengambil format.{RESET}")
        return

    format_dict = {}
    seen_resolutions = set()

    for line in output:
        if re.search(r'\bvideo only\b', line) and 'https' in line:
            parts = line.split()
            if len(parts) >= 3:
                fid = parts[0]
                res = parts[2]
                size_match = re.search(r'~?\d+(\.\d+)?[MGK]iB', line)
                size = size_match.group(0) if size_match else "?"
                label_match = re.search(r'(\d+)x(\d+)', res)
                if not label_match:
                    continue
                _, h = label_match.groups()
                quality = f"{h}p"
                if quality in seen_resolutions:
                    continue
                seen_resolutions.add(quality)
                label = f"{res} ({quality}) {size}"
                format_dict[fid] = label

    print(f"\n{BOLD}{CYAN}📺 Resolusi Tersedia:{RESET}\n")
    print(f"{BOLD}  No  Resolusi      Kualitas     ▸   Ukuran File{RESET}")
    print(f"{CYAN}╔═════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {YELLOW} 0.{RESET} Kembali ke menu utama{' ' * 22}{CYAN}║{RESET}")
    for i, (fid, label) in enumerate(format_dict.items(), 1):
        parts = re.match(r"(.+?)\s\((\d+p)\)\s(.+)", label)
        if parts:
            res_raw, res_p, size = parts.groups()
            size = size.replace("~", "").strip()
            print(f"{CYAN}║{RESET}  {YELLOW}{i:>2}.{RESET} {res_raw:<13} ({res_p:<6})    ▸  {size:<10}   {CYAN} ║{RESET}")
        else:
            print(f"{CYAN}║{RESET}  {YELLOW}{i:>2}.{RESET} {label:<43} {CYAN}║{RESET}")
    print(f"{CYAN}╚═════════════════════════════════════════════════╝{RESET}")

    pilihan = input(f"\n{GREEN}🎯 Pilih nomor resolusi yang diinginkan (0 untuk kembali): {RESET}").strip()
    if pilihan == "0":
        return

    if not pilihan.isdigit():
        print(f"{RED}❌ Input tidak valid.{RESET}")
        return

    index = int(pilihan)
    if index < 1 or index > len(format_dict):
        print(f"{RED}❌ Nomor tidak tersedia.{RESET}")
        return

    format_id = list(format_dict.keys())[index - 1]
    label = list(format_dict.values())[index - 1]

    # Simpan file sebelum download
    before = set(glob.glob("*.mp4"))

    print(f"\n{YELLOW}📽️ Mengunduh video resolusi {label}...{RESET}")
    os.system(f"yt-dlp -f {format_id}+bestaudio --merge-output-format mp4 -o '%(title)s.%(ext)s' '{url}'")

    # Ambil file setelah download
    after = set(glob.glob("*.mp4"))
    new_files = after - before

    if new_files:
        os.makedirs("/sdcard/Download/Movies", exist_ok=True)
        for file in new_files:
            try:
                shutil.move(file, f"/sdcard/Download/Movies/{file}")
                print(f"{GREEN}✅ Dipindahkan: {file}{RESET}")
            except Exception as e:
                print(f"{RED}❌ Gagal pindah {file}: {e}{RESET}")
    else:
        print(f"{RED}❌ Tidak ada file baru untuk dipindahkan.{RESET}")

def download_video_any():
    inp = input(f"\n{GREEN}⬇️ Masukkan link video : {RESET}").strip()
    if not inp:
        print(f"{RED}❌ Link tidak boleh kosong.{RESET}")
        return

    # Simpan file sebelum download
    before = set(glob.glob("*.mp4"))

    print(f"\n{YELLOW}📽️ Mengunduh video...{RESET}")
    
    # Coba format bestvideo+bestaudio dulu
    result = os.system(f"yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o '%(title)s.%(ext)s' '{inp}'")
    
    # Jika gagal, coba format best (gabung otomatis jika hanya 1 stream)
    if result != 0:
        print(f"{YELLOW}⚠️ Format terpisah tidak tersedia, mencoba format tunggal...{RESET}")
        os.system(f"yt-dlp -f best --merge-output-format mp4 -o '%(title)s.%(ext)s' '{inp}'")

    # Ambil file setelah download
    after = set(glob.glob("*.mp4"))
    new_files = after - before

    if new_files:
        os.makedirs("/sdcard/Download/Movies", exist_ok=True)
        for file in new_files:
            try:
                shutil.move(file, f"/sdcard/Download/Movies/{file}")
                print(f"{GREEN}✅ Dipindahkan: {file}{RESET}")
            except Exception as e:
                print(f"{RED}❌ Gagal pindah {file}: {e}{RESET}")
    else:
        print(f"{RED}❌ Tidak ada file baru untuk dipindahkan.{RESET}")

def download_audio_any():
    inp = input(f"\n{GREEN}⬇️ Masukkan link audio/video : {RESET}").strip()
    if not inp:
        print(f"{RED}❌ Link tidak boleh kosong.{RESET}")
        return

    # Ambil daftar file sebelum download
    before = set(glob.glob("*.mp3"))

    print(f"\n{YELLOW}🎵 Mengunduh audio...{RESET}")
    os.system(f"yt-dlp -x --audio-format mp3 -o '%(title)s.%(ext)s' '{inp}'")

    # Ambil daftar file setelah download
    after = set(glob.glob("*.mp3"))
    new_files = after - before

    if new_files:
        os.makedirs("/sdcard/Download/Music", exist_ok=True)
        for file in new_files:
            try:
                shutil.move(file, f"/sdcard/Download/Music/{file}")
                print(f"{GREEN}✅ Dipindahkan: {file}{RESET}")
            except Exception as e:
                print(f"{RED}❌ Gagal pindah {file}: {e}{RESET}")
    else:
        print(f"{RED}❌ Tidak ada file baru untuk dipindahkan.{RESET}")

def download_spotify_music():

    # ===== KONFIGURASI =====
    CLIENT_ID = "48fb05aa18f74092abe88882b281eebf"
    CLIENT_SECRET = "083099b34cbf48679078faa17c9a2740"
    DOWNLOAD_DIR = "/sdcard/Download/Music"  # folder untuk menyimpan file
    # =======================

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    spotify_url = input(f"\n{GREEN}Masukkan link Spotify: {RESET}").strip()

    # Setup Spotify API
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
    )

    # ===== REGEX UNIVERSAL =====
    match = re.search(
        r"spotify\.com/(?:[a-zA-Z\-]+/)?(playlist|album|track|artist|show|episode)/([a-zA-Z0-9]+)",
        spotify_url
    )
    if not match:
        print("URL Spotify tidak valid atau tipe belum didukung.")
        return

    link_type = match.group(1)
    spotify_id = match.group(2)
    tracks = []

    # ===== PLAYLIST =====
    if link_type == "playlist":
        results = sp.playlist_tracks(spotify_id)
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    title = f"{track['name']} {track['artists'][0]['name']}"
                    tracks.append(title)
            if results['next']:
                results = sp.next(results)
            else:
                break

    # ===== ALBUM =====
    elif link_type == "album":
        results = sp.album_tracks(spotify_id)
        for item in results['items']:
            title = f"{item['name']} {item['artists'][0]['name']}"
            tracks.append(title)

    # ===== TRACK =====
    elif link_type == "track":
        track = sp.track(spotify_id)
        title = f"{track['name']} {track['artists'][0]['name']}"
        tracks.append(title)

    # ===== ARTIST =====
    elif link_type == "artist":
        seen_tracks = set()
        albums = sp.artist_albums(spotify_id, album_type='album,single', country='ID', limit=50)
        album_ids = []
        while True:
            for album in albums['items']:
                if album['id'] not in album_ids:
                    album_ids.append(album['id'])
            if albums['next']:
                albums = sp.next(albums)
            else:
                break
        for album_id in album_ids:
            album_tracks = sp.album_tracks(album_id)
            for item in album_tracks['items']:
                track_name = f"{item['name']} {item['artists'][0]['name']}"
                if track_name not in seen_tracks:
                    tracks.append(track_name)
                    seen_tracks.add(track_name)

    # ===== SHOW (podcast) =====
    elif link_type == "show":
        episodes = sp.show_episodes(spotify_id, limit=50)
        while True:
            for ep in episodes['items']:
                tracks.append(ep['name'])
            if episodes['next']:
                episodes = sp.next(episodes)
            else:
                break

    # ===== EPISODE =====
    elif link_type == "episode":
        episode = sp.episode(spotify_id)
        tracks.append(episode['name'])

    if not tracks:
        print("Gagal mengambil daftar lagu/episode.")
        return

    # ===== DOWNLOAD =====
    for title in tracks:
        print(f"⬇ Mengunduh: {title}")
        try:
            url = subprocess.check_output(
                ["yt-dlp", f"ytsearch1:{title}", "--get-url", "-f", "bestaudio"],
                text=True
            ).strip()
            os.system(f"mpv --no-video '{url}'")
        except subprocess.CalledProcessError:
            print(f"{RED}❌ Gagal memutar: {title}{RESET}")

        except KeyboardInterrupt:
            print("\n⏹ Dihentikan.")
            break

    print(f"\n✅ Semua file tersimpan di folder '{DOWNLOAD_DIR}'")

def download_photo():
    inp = input(f"\n{GREEN}⬇️ Masukkan link foto/album: {RESET}").strip()
    if not inp:
        print(f"{RED}❌ Link tidak boleh kosong.{RESET}")
        return

    # Cek apakah gallery-dl terpasang
    try:
        subprocess.run(["gallery-dl", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{RED}❌ gallery-dl belum terpasang.{RESET}")
        print(f"{YELLOW}💡 Install dengan: {CYAN}pip install gallery-dl{RESET}")
        return

    # Buat folder tujuan
    save_dir = "/sdcard/Download/Photo"
    os.makedirs(save_dir, exist_ok=True)

    print(f"\n{YELLOW}🖼️ Mengunduh foto...{RESET}")
    result = os.system(f"gallery-dl -d '{save_dir}' '{inp}'")

    if result == 0:
        print(f"{GREEN}✅ Foto berhasil diunduh ke: {save_dir}{RESET}")
    else:
        print(f"{RED}❌ Gagal mengunduh foto.{RESET}")

def play_music_spotify():
    # ===== KONFIGURASI =====
    CLIENT_ID = "2fc2c537fbef4a49ae788bc57e7ba7fc"
    CLIENT_SECRET = "26ec19cc9ea74235ab0f3094ccf57f11"
    # =======================

    spotify_url = input(f"\n{GREEN}🎧Masukkan link Spotify: {RESET}").strip()

    # Setup Spotify API
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
    )

    # ===== REGEX UNIVERSAL =====
    match = re.search(
        r"spotify\.com/(?:[a-zA-Z\-]+/)?(playlist|album|track|artist|show|episode)/([a-zA-Z0-9]+)",
        spotify_url
    )
    if not match:
        print("URL Spotify tidak valid atau tipe belum didukung.")
        return

    link_type = match.group(1)
    spotify_id = match.group(2)
    tracks = []

    # ===== PLAYLIST =====
    if link_type == "playlist":
        results = sp.playlist_tracks(spotify_id)
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    title = f"{track['name']} {track['artists'][0]['name']}"
                    tracks.append(title)
            if results['next']:
                results = sp.next(results)
            else:
                break

    # ===== ALBUM =====
    elif link_type == "album":
        results = sp.album_tracks(spotify_id)
        for item in results['items']:
            title = f"{item['name']} {item['artists'][0]['name']}"
            tracks.append(title)

    # ===== TRACK =====
    elif link_type == "track":
        track = sp.track(spotify_id)
        title = f"{track['name']} {track['artists'][0]['name']}"
        tracks.append(title)

    # ===== ARTIST =====
    elif link_type == "artist":
        seen_tracks = set()
        albums = sp.artist_albums(spotify_id, album_type='album,single', country='ID', limit=50)
        album_ids = []
        while True:
            for album in albums['items']:
                if album['id'] not in album_ids:
                    album_ids.append(album['id'])
            if albums['next']:
                albums = sp.next(albums)
            else:
                break
        for album_id in album_ids:
            album_tracks = sp.album_tracks(album_id)
            for item in album_tracks['items']:
                track_name = f"{item['name']} {item['artists'][0]['name']}"
                if track_name not in seen_tracks:
                    tracks.append(track_name)
                    seen_tracks.add(track_name)

    # ===== SHOW =====
    elif link_type == "show":
        episodes = sp.show_episodes(spotify_id, limit=50)
        while True:
            for ep in episodes['items']:
                tracks.append(ep['name'])
            if episodes['next']:
                episodes = sp.next(episodes)
            else:
                break

    # ===== EPISODE =====
    elif link_type == "episode":
        episode = sp.episode(spotify_id)
        tracks.append(episode['name'])

    if not tracks:
        print("Gagal mengambil daftar lagu/episode.")
        return

    tampil_kontrol()  # kalau mau menampilkan kontrol MPV di terminal

    # ===== STREAM TANPA DOWNLOAD =====
    for title in tracks:
        print(f"▶ Memutar: {title}")
        try:
            url = subprocess.check_output(
                ["yt-dlp", f"ytsearch1:{title}", "--get-url", "-f", "bestaudio"],
                text=True
            ).strip()
            os.system(f"mpv --no-video '{url}'")
        except KeyboardInterrupt:
            print("\n⏹ Dihentikan.")
            break

def update_dependencies():
    print(f"\n{CYAN}🔄 Mengecek koneksi internet...{RESET}")
    try:
        # Tes koneksi dengan ping google
        status = os.system("ping -c 1 google.com > /dev/null 2>&1")
        if status != 0:
            print(f"{RED}❌ Tidak ada koneksi internet. Periksa jaringan kamu dulu.{RESET}")
            return
    except Exception:
        print(f"{RED}❌ Gagal melakukan pengecekan internet.{RESET}")
        return

    print(f"\n{CYAN}🔄 Mengupdate & Menginstall semua dependensi...{RESET}")
    try:
        # Update python + pip bawaan
        os.system("pkg install -y python")
        os.system("pkg upgrade -y python")

        # Update yt-dlp (via pip dan pkg agar aman di Termux)
        os.system("pip install -U yt-dlp")
        os.system("pkg install -y yt-dlp")

        # Install Spotify API wrapper (spotipy)
        os.system("pip install spotipy")

        # Install dependensi tambahan
        os.system("pip install requests termcolor pyfiglet")

        # Install mpv untuk pemutar musik
        os.system("pkg install -y mpv")

        # Install ffmpeg untuk konversi audio/video
        os.system("pkg install -y ffmpeg")

        print(f"\n{GREEN}✅ Semua dependensi sudah diupdate!{RESET}\n")

        # =========================================================
        # 🔍 Langsung cek semua versi setelah update
        # =========================================================
        print(f"\n{CYAN}📌 Versi dependensi setelah update:{RESET}\n")

        print(f"{CYAN}▶ Python:{RESET}")
        os.system("python --version")

        print(f"{CYAN}▶ pip:{RESET}")
        os.system("pip --version")

        print(f"{CYAN}▶ yt-dlp:{RESET}")
        os.system("yt-dlp --version")

        print(f"{CYAN}▶ mpv:{RESET}")
        os.system("mpv --version | head -n 1")

        print(f"{CYAN}▶ ffmpeg:{RESET}")
        os.system("ffmpeg -version | head -n 1")

        print(f"{CYAN}▶ spotipy:{RESET}")
        os.system("pip show spotipy | grep Version || echo '❌ Belum terpasang'")

        print(f"{CYAN}▶ requests:{RESET}")
        os.system("pip show requests | grep Version || echo '❌ Belum terpasang'")

        print(f"{CYAN}▶ termcolor:{RESET}")
        os.system("pip show termcolor | grep Version || echo '❌ Belum terpasang'")

        print(f"{CYAN}▶ pyfiglet:{RESET}")
        os.system("pip show pyfiglet | grep Version || echo '❌ Belum terpasang'")

    except Exception as e:
        print(f"{RED}❌ Gagal update dependensi: {str(e)}{RESET}")

def main():
    while True:
        pilihan = menu()
        if pilihan == "1":
            play_music()
        elif pilihan == "2":
            play_mix_manual()
        elif pilihan == "3":
            play_playlist()
        elif pilihan == "4":
            play_music_spotify()
        elif pilihan == "5":
            download_audio()
        elif pilihan == "6":
            download_video()
        elif pilihan == "7":
            download_video_any()
        elif pilihan == "8":
            download_audio_any()
        elif pilihan == "9":
            download_photo()            
        elif pilihan == "10":
            download_spotify_music()
        elif pilihan == "11":
            update_dependencies()
        elif pilihan == "0":
            print(f"\n{MAGENTA}👋 Keluar...{RESET}")
            break
        else:
            print(f"\n{RED}❌ Pilihan tidak valid.{RESET}")
        input(f"\n{BOLD}{BLUE}Tekan Enter untuk kembali ke menu...{RESET}")

if __name__ == "__main__":
    main()

