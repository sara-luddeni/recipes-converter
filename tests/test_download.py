"""
Test for TikTok video downloader
"""
import pytest
import os
import tempfile
import shutil
from recipes_bot.tiktok_downloader import download_tiktok_video


def test_download_tiktok_video():
    """
    Test downloading a TikTok video to a tmp folder and verify it exists
    """
    # Create a temporary directory
    tmp_dir = tempfile.mkdtemp()
    
    try:
        url = "https://www.tiktok.com/@frostie014/video/7523906810613402902"
        
        # Download the video
        result = download_tiktok_video(url, output_path=tmp_dir, use_cookies=False)
        
        # Verify download was successful
        assert result is True, "Download function should return True on success"
        
        # Check if files exist in the tmp directory
        files_in_dir = os.listdir(tmp_dir)
        assert len(files_in_dir) > 0, f"Expected at least one file in {tmp_dir}, but found none"
        
        # Check if any file is a video file (common video extensions)
        video_extensions = ['.mp4', '.webm', '.mkv', '.mov', '.avi']
        downloaded_files = [f for f in files_in_dir if any(f.lower().endswith(ext) for ext in video_extensions)]
        
        assert len(downloaded_files) > 0, f"Expected at least one video file, but found: {files_in_dir}"
        
        # Verify the file size is reasonable (at least 1KB)
        for file in downloaded_files:
            file_path = os.path.join(tmp_dir, file)
            file_size = os.path.getsize(file_path)
            assert file_size > 1024, f"Expected file size > 1KB, but got {file_size} bytes for {file}"
            print(f"✓ Downloaded: {file} ({file_size} bytes)")
            
    finally:
        # Clean up temporary directory
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f"✓ Cleaned up temporary directory: {tmp_dir}")
