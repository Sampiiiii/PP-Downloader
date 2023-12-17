from yt_dlp import YoutubeDL
from dotenv import load_dotenv
import json
import os

load_dotenv()


def load_playlists(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Set the parent directory and FFmpeg path directly
parent_dir = os.getenv('PARENT_DIR')
ffmpeg_path = os.getenv('FFMPEG_PATH')
json_path = os.getenv('JSON_PATH')

# Map directories to playlist URLs
playlists = load_playlists(json_path)


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
    except Exception as e:
        print(f"Error downloading video '{video_info['title']}': {e}")


# Download a playlist with metadata for each video
def download_playlist(playlist_url, target_dir, playlist_name, base_ydl_opts):
    archive_file = os.path.join(parent_dir, f"{playlist_name}_archive.txt")

    try:
        with YoutubeDL(base_ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            for video_info in playlist_info.get("entries", []):
                if video_info:
                    process_video(video_info, target_dir, base_ydl_opts)
    except Exception as e:
        print(f"Error processing playlist '{playlist_name}': {e}")


# Base download options
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
    "ignoreerrors": True,
}

# Ensure target directories exist and download each playlist
for playlist_name, playlist_url in playlists.items():
    target_dir = os.path.join(parent_dir, playlist_name)
    os.makedirs(target_dir, exist_ok=True)
    base_download_options["download_archive"] = os.path.join(parent_dir, f"{playlist_name}_archive.txt")
    download_playlist(playlist_url, target_dir, playlist_name, base_download_options)
