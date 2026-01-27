# Recipes extractor

A Python package that extracts recipes from TikTok videos using audio transcription and LLM-based extraction. It can be used as a Telegram bot, a Python library, or a command-line tool.

## Features

- **TikTok Video Downloading**: Downloads TikTok videos without watermarks using Playwright
- **Audio Transcription**: Extracts and transcribes audio using OpenAI Whisper
- **Recipe Extraction**: Uses GPT-4o-mini to extract structured recipe information (title, ingredients, instructions)
- **Telegram Bot**: Interactive bot that processes TikTok links and returns formatted recipes
- **Markdown Export**: Saves extracted recipes as Markdown files

## Requirements

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- ffmpeg (for audio extraction)
- Playwright browsers (for TikTok downloading)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/recipes-converter.git
cd recipes-converter

# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for Whisper transcription and GPT extraction |
| `TELEGRAM_BOT_TOKEN` | For bot | Telegram bot token (get from [@BotFather](https://t.me/botfather)) |

## Usage

### Telegram Bot

Run the bot to process TikTok recipe links via Telegram:

```bash
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
export OPENAI_API_KEY="your-openai-api-key"

recipes-bot-run
```

Users can send TikTok video links to the bot and receive formatted recipes with ingredients and instructions.

### Python Library

```python
from recipes_bot import (
    TikTokDownloader,
    extract_recipe,
    extract_recipe_from_url,
    extract_recipe_from_video,
    transcribe,
    transcribe_to_chunks,
)

# Extract recipe directly from TikTok URL
recipe = extract_recipe_from_url(
    "https://www.tiktok.com/@user/video/1234567890",
    "output/recipe.md"
)
print(recipe.title)
print(recipe.ingredients)
print(recipe.instructions)

# Extract from local video file
recipe = extract_recipe_from_video("video.mp4", "output/recipe.md")

# Transcribe video to text
transcript = transcribe("video.mp4")

# Get timestamped chunks
chunks = transcribe_to_chunks("video.mp4")
for chunk in chunks:
    print(f"[{chunk.start_s:.1f}s - {chunk.end_s:.1f}s] {chunk.text}")

# Download TikTok video
TikTokDownloader.download(
    "https://www.tiktok.com/@user/video/1234567890",
    "downloaded_video.mp4"
)
```

### Command-Line Tool

```bash
# Download a TikTok video
tiktok-downloader https://www.tiktok.com/@user/video/1234567890

# Specify output path
tiktok-downloader https://www.tiktok.com/@user/video/1234567890 output/video.mp4
```

## Project Structure

```
recipes_bot/
├── __init__.py              # Package exports
├── bot/
│   └── __init__.py          # Telegram bot implementation
├── downloaders/
│   └── tiktok/
│       └── __init__.py      # TikTok video downloader using Playwright
└── extractors/
    ├── __init__.py          # Extractor exports
    ├── audio.py             # Audio extraction and Whisper transcription
    ├── models.py            # Data models (Recipe, TextChunk)
    └── recipe.py            # LLM-based recipe extraction
```

## Data Models

### Recipe

```python
@dataclass
class Recipe:
    title: str
    ingredients: List[str]
    instructions: List[str]
```

### TextChunk

```python
@dataclass
class TextChunk:
    source: Literal["audio", "ocr"]
    start_s: float
    end_s: float
    text: str
    confidence: Optional[float] = None
```

## Development

Install with development dependencies:

```bash
uv sync --extra dev
```

Run tests:

```bash
uv run pytest
```

## Docker

Build and run using Docker:

```bash
# Build the image
docker build -t recipes-bot .

# Run the container
docker run -e OPENAI_API_KEY="your-key" -e TELEGRAM_BOT_TOKEN="your-token" recipes-bot
```

## Building the Package

```bash
uv build
```

This creates a wheel and source distribution in the `dist/` directory.

## License

MIT
