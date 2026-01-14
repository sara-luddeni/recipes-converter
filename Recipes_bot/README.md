# Recipes Bot

A Python package for downloading TikTok videos and managing recipes.

## Installation

### Using uv (recommended)

```bash
# Install the package in development mode
uv pip install -e .

# Or install from source
uv pip install .
```

### Using pip

```bash
pip install -e .
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

### Using uv

```bash
# Build the package
uv build

# This will create a wheel and source distribution in the dist/ directory
```

### Using pip

```bash
pip install build
python -m build
```

## Development

Install with development dependencies:

```bash
uv pip install -e ".[dev]"
```
