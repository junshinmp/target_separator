import yt_dlp
import os
from pathlib import Path

better_training = Path("better_training")

print(f"Youtube videos will be put into the {better_training} directory")
os.makedirs(better_training, exist_ok=True)

url = 'https://www.youtube.com/watch?v=mjxGYCzzcSM'
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'outtmpl': str(better_training / '%(title)s.%(ext)s'),
    }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])