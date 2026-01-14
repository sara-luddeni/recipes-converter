"""
TikTok Video Downloader
Downloads videos from TikTok using yt-dlp library
"""

import yt_dlp
import sys
import os


def download_tiktok_video(url, output_path="downloads"):
    """
    Download a TikTok video from a given URL
    
    Args:
        url: TikTok video URL
        output_path: Directory to save the video (default: "downloads")
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'best',  # Download best quality available
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Output filename template
        'noplaylist': True,  # Download only single video, not playlist
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first to show video details
            info = ydl.extract_info(url, download=False)
            print(f"\nVideo Title: {info.get('title', 'N/A')}")
            print(f"Uploader: {info.get('uploader', 'N/A')}")
            print(f"Duration: {info.get('duration', 'N/A')} seconds")
            print(f"\nDownloading...")
            
            # Download the video
            ydl.download([url])
            print(f"\n✓ Video downloaded successfully to '{output_path}' folder!")
            
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return False
    
    return True


def main():
    """Main function to handle command line usage"""
    if len(sys.argv) < 2:
        print("Usage: tiktok-downloader <TikTok_URL> [output_directory]")
        print("\nExample:")
        print("  tiktok-downloader https://www.tiktok.com/@user/video/1234567890")
        print("  tiktok-downloader https://www.tiktok.com/@user/video/1234567890 my_videos")
        return
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "downloads"
    
    download_tiktok_video(url, output_path)


if __name__ == "__main__":
    main()
