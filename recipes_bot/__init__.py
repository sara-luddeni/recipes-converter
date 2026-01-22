"""
Recipes Bot Package
A package for downloading TikTok videos and managing recipes
"""

__version__ = "0.1.0"

from .downloaders.tiktok import TikTokDownloader
from .extractors import TextChunk, transcribe, transcribe_to_chunks

__all__ = ["TikTokDownloader", "TextChunk", "transcribe", "transcribe_to_chunks"]
