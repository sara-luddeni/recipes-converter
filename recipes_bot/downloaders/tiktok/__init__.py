import time

import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class TikTokDownloader:

    @staticmethod
    def download(url: str, output: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = browser.new_context(
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = context.new_page()
            
            page.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            ''')
            
            try:
                page.goto("https://ssstik.io/it-1", timeout=30000)
                
                try:
                    consent_btn = page.locator('button.fc-cta-consent').first
                    consent_btn.click(timeout=5000)
                    time.sleep(1)
                except PlaywrightTimeoutError:
                    pass
                
                input_field = page.locator('#main_page_text')
                input_field.fill(url)
                
                download_button = page.locator('button[type="submit"]')
                download_button.click()
                
                page.wait_for_selector('a.download_link.without_watermark', timeout=30000)
                time.sleep(1)
                
                download_link = page.locator('a.download_link.without_watermark:not(.without_watermark_hd)').first
                video_url = download_link.get_attribute('href')
                
                headers = {
                    'Referer': 'https://ssstik.io/',
                    'User-Agent': page.evaluate('() => navigator.userAgent')
                }
                
                response = requests.get(video_url, stream=True, headers=headers)
                response.raise_for_status()
                
                if isinstance(output, str):
                    with open(output, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        output.write(chunk)
                    output.flush()
                
            finally:
                browser.close()
        
        return output
        