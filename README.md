# YT-Player
Play and download Audio, Video from Youtube

pkg update && pkg update -y
termux-setup-storage
pkg install python mpv git -y
pip install yt-dlp
pip install ffmpeg
git clone https://github.com/CodinganGila/YT-Player

cd YT-Player

python ytp.py
