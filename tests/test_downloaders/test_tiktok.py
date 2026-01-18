
import pathlib
import tempfile
from recipes_bot import TikTokDownloader

def test_tiktok_downloader():

    tiktok_url = r"https://www.tiktok.com/@frostie014/video/7523906810613402902"
    tiktok_video = pathlib.Path(__file__).parent.parent / "fixture/7523906810613402902.mp4"

    with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_video:
        downloaded = TikTokDownloader.download(url=tiktok_url, output=temp_video)
    
    assert True # some