"""
Recipes Bot Package
A package for downloading TikTok videos and managing recipes
"""

__version__ = "0.1.0"

from .downloaders.tiktok import TikTokDownloader
from .extractors import (
    Recipe,
    TextChunk,
    extract_recipe,
    extract_recipe_from_url,
    extract_recipe_from_video,
    transcribe,
    transcribe_to_chunks,
)

__all__ = [
    "TikTokDownloader",
    "TextChunk",
    "Recipe",
    "transcribe",
    "transcribe_to_chunks",
    "extract_recipe",
    "extract_recipe_from_url",
    "extract_recipe_from_video",
]
