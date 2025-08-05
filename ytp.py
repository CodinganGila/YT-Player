import os
import subprocess
import re
import random
import glob
import shutil    

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
║ {YELLOW}1.{CYAN} Play Music (judul/link)           ║
║ {YELLOW}2.{CYAN} Play Mix (lagu mirip otomatis)    ║
║ {YELLOW}3.{CYAN} Play Playlist                     ║
║ {YELLOW}4.{CYAN} Download Audio                    ║
║ {YELLOW}5.{CYAN} Download Video                    ║
║ {YELLOW}0.{CYAN} Keluar                            ║
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
    os.system(f"mpv --no-video --ytdl-format=bestaudio '{url}'")

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
        os.system(f"mpv --no-video --ytdl-format=bestaudio '{url}'")

        while True:
            hasil = subprocess.check_output(
                f"yt-dlp 'ytsearch10:{judul}' --print '%(webpage_url)s' -q",
                shell=True
            ).decode().strip().split('\n')

            if not hasil:
                print(f"{RED}❌ Tidak ada hasil yang ditemukan.{RESET}")
                break

            acak = random.choice(hasil)
            tampil_kontrol()
            print(f"{YELLOW}▶️ Memutar lagu mirip (dipercepat): {acak}{RESET}")
            os.system(f"mpv --no-video --ytdl-format=bestaudio '{acak}'")

    except KeyboardInterrupt:
        print(f"\n{MAGENTA}⏹️ Dihentikan oleh user.{RESET}")
    except Exception as e:
        print(f"{RED}❌ Terjadi kesalahan: {str(e)}{RESET}")

def play_playlist():
    url = input(f"{YELLOW}📜 Masukkan link playlist YouTube: {RESET}").strip()
    if "playlist" in url or "list=" in url:
        tampil_kontrol()
        print(f"{GREEN}▶️ Memutar playlist...{RESET}")
        os.system(f"mpv --no-video --ytdl-format=bestaudio '{url}'")
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
        os.makedirs("/sdcard/Music", exist_ok=True)
        for file in new_files:
            try:
                shutil.move(file, f"/sdcard/Music/{file}")
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
        os.makedirs("/sdcard/Movies", exist_ok=True)
        for file in new_files:
            try:
                shutil.move(file, f"/sdcard/Movies/{file}")
                print(f"{GREEN}✅ Dipindahkan: {file}{RESET}")
            except Exception as e:
                print(f"{RED}❌ Gagal pindah {file}: {e}{RESET}")
    else:
        print(f"{RED}❌ Tidak ada file baru untuk dipindahkan.{RESET}")


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
            download_audio()
        elif pilihan == "5":
            download_video()            
        elif pilihan == "0":
            print(f"\n{MAGENTA}👋 Keluar...{RESET}")
            break
        else:
            print(f"\n{RED}❌ Pilihan tidak valid.{RESET}")
        input(f"\n{BOLD}{BLUE}Tekan Enter untuk kembali ke menu...{RESET}")

if __name__ == "__main__":
    main()

