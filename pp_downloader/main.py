import signal
import threading

from yt_dlp import YoutubeDL
from dotenv import load_dotenv
import json
import os

# Load environment variables
load_dotenv()


# Load configuration from a JSON file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Set the parent directory, FFmpeg path, and JSON path
parent_dir = os.getenv('MUSIC_PARENT_DIR')
ffmpeg_path = os.getenv('FFMPEG_PATH')
json_path = os.getenv('JSON_PATH')

# Load configuration
config = load_config(json_path)
playlists = config['playlists']
sleep_time = int(config['sleep_time'])

# Global archive file for tracking all downloads
global_archive_file = os.path.join(parent_dir, 'global_archive.txt')


# Function to process and download each video with metadata
def process_video(video_info, target_dir, base_ydl_opts):
    video_outtmpl = os.path.join(target_dir, f"{video_info['title']}.%(ext)s")
    metadata_args = [
        "-metadata", f"title={video_info['title']}",
        "-metadata", f"album={video_info['title']}",
        "-metadata", f"artist={video_info['uploader']}",
    ]

    ydl_opts = base_ydl_opts.copy()
    ydl_opts.update({"outtmpl": video_outtmpl, "postprocessor_args": metadata_args})

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_info["webpage_url"]])
        print(f"Downloaded video: {video_info['title']}")
    except Exception as e:
        print(f"Error downloading video '{video_info['title']}': {e}")


# Download a playlist with metadata for each video
def download_playlist(playlist_url, target_dir, base_ydl_opts):
    try:
        with YoutubeDL(base_ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            for video_info in playlist_info.get("entries", []):
                if video_info:
                    process_video(video_info, target_dir, base_ydl_opts)
    except Exception as e:
        print(f"Error processing playlist: {e}")


# Event for managing sleep/wait
sleep_event = threading.Event()

# Base download options with a global archive file
base_download_options = {
    "format": "bestaudio/best",
    "postprocessors": [
        {"key": "FFmpegExtractAudio", "preferredcodec": "best", "preferredquality": "best"},
        {"key": "FFmpegMetadata", "add_metadata": True},
        {"key": "EmbedThumbnail"},
    ],
    "ffmpeg_location": ffmpeg_path,
    "writethumbnail": True,
    "noplaylist": False,
    "noplaylist_metafiles": True,
    "ignoreerrors": True,
    "download_archive": global_archive_file
}


def handle_sigint(signum, frame):
    print("SIGINT signal received.")
    exit(0)


def handle_sigterm(signum, frame):
    print("SIGTERM signal received.")
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    while True:
        print("Starting download process.")
        for playlist_name, playlist_url in playlists.items():
            target_dir = os.path.join(parent_dir, playlist_name.replace('/', '_'))
            os.makedirs(target_dir, exist_ok=True)
            download_playlist(playlist_url, target_dir, base_download_options)
        print(f"Download process completed. Sleeping for {sleep_time} seconds.")

        # Wait for sleep_time or until the event is set
        sleep_event.wait(sleep_time)
        if sleep_event.is_set():
            break
        sleep_event.clear()
