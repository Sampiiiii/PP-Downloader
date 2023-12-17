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

The JSON File should be in the root of the volume you mount the docker container to download to and should look something like this:
```json
{
   "jazz" : "https://www.youtube.com/playlist?list=PLkKEwrqC_3hw73ktWYyZUpywRYuYWGbQO",
   "not-jazz": "https://www.youtube.com/playlist?list=PLkKEwrqC_3hwQgz9MuCiDkGcSKsHvSKXP"
}
```
this will create the following in the mounted volume
```
volume
├── jazz
│   └── ...
├── not-jazz
│   └── ...
├── not-jazz_archive.txt
└── playlists.json

```
To hook into plex all you need to do is point plex at the volume and tell it to prefer local metadata and it should just work.