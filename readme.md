# Plex Playlist Downloader

This project arose because youtube dl doesnt work well with plex out of the box in the way that I want. Which is:

- Being able to pass a Key Value pair of playlist names and urls to download
- Each video being treated as its own album where the video title is the album title and track title
- the artist is the video uploader

the way this works is relatively simple but you build it with the following

```bash
# Arch can be etiher amd64 (x86_64 architecure) or arm64(64bit arm)
# Sleep time is how long the script waits before it runs again

docker build --build-arg ARCH=arm64 --build-arg SLEEP_TIME=30 -t pp_downloader .
```