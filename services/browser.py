# import asyncio
# import os
# from playwright.async_api import async_playwright

# async def capture_chart_screenshot(url: str, output_filename: str) -> str:
#     """Navigates to a TradingView chart URL and captures a screenshot of the page."""
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(
#             headless=True,
#             args=[
#                 "--no-sandbox",
#                 "--disable-setuid-sandbox",
#                 "--disable-dev-shm-usage",
#                 "--disable-accelerated-2d-canvas",
#                 "--disable-gpu"
#             ]
#         )
#         context = await browser.new_context(
#             viewport={"width": 1920, "height": 1080},
#             device_scale_factor=2,
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         )
#         page = await context.new_page()
        
#         try:
#             # Changed from networkidle to domcontentloaded to prevent hanging
#             await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            
#             # Allow canvas and charts extra time to render fully
#             await asyncio.sleep(6)
            
#             os.makedirs("temp", exist_ok=True)
#             file_path = os.path.join("temp", output_filename)
#             await page.screenshot(path=file_path, full_page=False)
            
#             return file_path
#         finally:
#             await browser.close()


import asyncio
import os
from playwright.async_api import async_playwright

async def capture_chart_screenshot(url: str, output_filename: str) -> str:
    """Navigates to a TradingView chart URL and captures a screenshot of the page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--disable-gpu"
            ]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # Keep domcontentloaded so it doesn't hang
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            
            # Increased sleep time from 6 to 12 seconds to give TradingView time to load the chart canvas
            await asyncio.sleep(12)
            
            os.makedirs("temp", exist_ok=True)
            file_path = os.path.join("temp", output_filename)
            await page.screenshot(path=file_path, full_page=False)
            
            return file_path
        finally:
            await browser.close()