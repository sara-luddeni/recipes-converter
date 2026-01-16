# Recipes Bot

A Python package for downloading TikTok videos and managing recipes.

## Installation

```bash
# Install the package and dependencies
uv sync
```

## Usage

### As a command-line tool

After installation, you can use the `tiktok-downloader` command:

```bash
tiktok-downloader https://www.tiktok.com/@user/video/1234567890
tiktok-downloader https://www.tiktok.com/@user/video/1234567890 my_videos
```

### As a Python module

```python
from recipes_bot import download_tiktok_video

download_tiktok_video("https://www.tiktok.com/@user/video/1234567890", "downloads")
```

## Building the package

```bash
# Build the package
uv build

# This will create a wheel and source distribution in the dist/ directory
```

## Development

Install with development dependencies:

```bash
uv sync --extra dev
```
