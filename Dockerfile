# Set base image depending on architecture
FROM python:3.12-slim AS base
RUN apt-get update && apt-get install -y wget xz-utils

# Download and install FFmpeg based on architecture
WORKDIR /tmp

ARG ARCH
RUN echo "Architecture: $ARCH"
RUN if [ "$ARCH" = "arm64" ]; then \
        echo "Downloading FFmpeg for ARM64..."; \
        wget --no-cache -O ffmpeg.tar.xz https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linuxarm64-gpl.tar.xz && tar -xf ffmpeg.tar.xz && mv ffmpeg-master-latest-linuxarm64-gpl/bin/* /usr/local/bin; \
    elif [ "$ARCH" = "amd64" ]; then \
        echo "Downloading FFmpeg for AMD64..."; \
        wget --no-cache -O ffmpeg.tar.xz https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz && tar -xf ffmpeg.tar.xz && mv ffmpeg-master-latest-linux64-gpl/bin/* /usr/local/bin; \
    else \
        echo "Architecture not Recognised, adjust your Dockerfile!"; \
    fi

# Install Poetry
FROM base AS poetry-install
RUN pip install poetry

# Install dependencies
FROM poetry-install AS dependencies
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install

# Final stage
FROM dependencies AS final
COPY main.py .

# Set environment variables
ENV PARENT_DIR="/app/music"
ENV FFMPEG_PATH="/usr/local/bin/ffmpeg"
ENV JSON_PATH="/app/music/playlists.json"
ENV PATH="/usr/local/bin:$PATH"

# Run the script
CMD python main.py
