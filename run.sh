docker build --build-arg ARCH=arm64 --build-arg SLEEP_TIME=30 -t pp_downloader .
docker run -v $(pwd)/music:/app/music pp_downloader