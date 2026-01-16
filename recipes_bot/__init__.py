"""
Recipes Bot Package
A package for downloading TikTok videos and managing recipes
"""

__version__ = "0.1.0"

from .tiktok_downloader import download_tiktok_video

__all__ = ["download_tiktok_video"]
