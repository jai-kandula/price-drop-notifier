import sys
import os
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

CHROMIUM_PATH = os.path.expandvars(
    r"%LOCALAPPDATA%\ms-playwright\chromium-1161\chrome-win\chrome.exe"
)

async def scrape_price(url):
    print(f"\n🌐 Starting scrape for: {url}")
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, executable_path=CHROMIUM_PATH)
            context = await browser.new_context()
            page = await context.new_page()
            await stealth_async(page)
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            })
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path="screenshot.png", full_page=True)
            print("✅ Screenshot captured.")

            selectors = [
                "#corePrice_feature_div span.a-offscreen",
                "#priceblock_ourprice",
                "#priceblock_dealprice",
                "#price_inside_buybox",
                "span.a-price > span.a-offscreen"
            ]

            for selector in selectors:
                element = await page.query_selector(selector)
                if element:
                    price_text = await element.inner_text()
                    price = float(price_text.replace("$", "").replace(",", "").strip())
                    await browser.close()
                    return price

            print("❌ Price not found.")
            await browser.close()
            return None
    except Exception as e:
        print(f"💥 Error scraping price: {e}")
        return None
