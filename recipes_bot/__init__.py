"""
Recipes Bot Package
A package for downloading TikTok videos and managing recipes
"""

__version__ = "0.1.0"

from .downloaders.tiktok import TikTokDownloader

__all__ = ["TikTokDownloader"]
