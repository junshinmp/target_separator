import yt_dlp
import os
from pathlib import Path

def download_video(url, output_folder="better_training"):
    output_folder = Path(output_folder)

    print(f"Youtube videos will be put into the {output_folder} directory")
    os.makedirs(output_folder, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/best[vcodec^=avc1]',
        'outtmpl': str(output_folder / '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=d-RGJPvFuNE'
    download_video(url)