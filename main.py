from yt_dlp import YoutubeDL
from dotenv import load_dotenv
import json
import os

# Load environment variables
load_dotenv()


# Load playlists from a JSON file
def load_playlists(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Set the parent directory, FFmpeg path, and JSON path
parent_dir = os.getenv('PARENT_DIR')
ffmpeg_path = os.getenv('FFMPEG_PATH')
json_path = os.getenv('JSON_PATH')

# Load playlists
playlists = load_playlists(json_path)

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
    "ignoreerrors": True,
    "download_archive": global_archive_file
}

# Ensure target directories exist and download each playlist
for playlist_name, playlist_url in playlists.items():
    target_dir = os.path.join(parent_dir, playlist_name)
    os.makedirs(target_dir, exist_ok=True)
    download_playlist(playlist_url, target_dir, base_download_options)
