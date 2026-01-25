import pathlib
import os
import tempfile
import pytest
from recipes_bot import TikTokDownloader

@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Skipped in GitHub Actions"
)
def test_tiktok_downloader():

    tiktok_url = r"https://www.tiktok.com/@mayan_yucateca/video/7535206495110122782"
    tiktok_video = pathlib.Path(__file__).parent.parent / "fixture/test_video.mp4"

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
        temp_path = pathlib.Path(temp_video.name)
        downloaded = TikTokDownloader.download(url=tiktok_url, output=temp_video)
    
    try:
        assert temp_path.exists(), "Downloaded file should exist"
        
        file_size = temp_path.stat().st_size
        assert file_size > 0, "Downloaded file should not be empty"
        assert file_size > 50000, f"Downloaded file should be at least 50KB, got {file_size} bytes"
        
        with open(temp_path, 'rb') as f:
            header = f.read(12)
            assert header[4:8] == b'ftyp', "File should be a valid MP4 file (ftyp signature)"
    
    finally:
        if temp_path.exists():
            temp_path.unlink()
