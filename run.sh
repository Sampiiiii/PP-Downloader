sudo docker build --build-arg ARCH=arm64 -t pp_downloader .
sudo docker run -v $(pwd)/music:/app/music pp_downloader