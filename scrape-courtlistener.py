import asyncio
from playwright.async_api import async_playwright
import random
import logging
from datetime import datetime, timedelta
import os
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)

class AdvancedScraper:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
        self.proxies = [
            # I had VPN hopping, so no proxies!
        ]

    async def create_browser_context(self, playwright):
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=random.choice(self.user_agents),
        )
        return browser, context

    async def simulate_human_behavior(self, page):
        await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
        await page.evaluate("""
            window.scrollTo({
                top: Math.floor(Math.random() * window.innerHeight),
                behavior: 'smooth'
            });
        """)
        await asyncio.sleep(random.uniform(1, 3))

    async def solve_captcha(self, page):
        # Implement CAPTCHA solving logic here if necessary - this isn't needed 
        pass

    async def scrape_page(self, page, url, file_name):
        await page.goto(url, wait_until="domcontentloaded")
        await self.simulate_human_behavior(page)

        if await page.query_selector('.captcha-class'):
            await self.solve_captcha(page)

        page_content = await page.content()

        os.makedirs('scraped_pages', exist_ok=True)
        with open(f'scraped_pages/{file_name}', 'w', encoding='utf-8') as file:
            file.write(page_content)

        logging.info(f"Saved content to {file_name}")

        next_page = await page.query_selector('a[rel="next"]')
        if next_page:
            return await next_page.get_attribute('href')
        return None

    async def scrape(self, base_url, start_date, end_date):
        async with async_playwright() as p:
            browser, context = await self.create_browser_context(p)
            page = await context.new_page()

            try:
                current_date = start_date
                while current_date <= end_date:
                    next_month = current_date + timedelta(days=32)
                    next_month = next_month.replace(day=1) - timedelta(days=1)

                    if next_month > end_date:
                        next_month = end_date

                    url = f"{base_url}&filed_after={current_date.strftime('%m%%2F%d%%2F%Y')}&filed_before={next_month.strftime('%m%%2F%d%%2F%Y')}"
                    
                    page_num = 1
                    success = False
                    retries = 0
                    while not success and retries < 3:
                        try:
                            while url:
                                file_name = f"{current_date.strftime('%Y-%m-%d')}_page{page_num}.html"
                                next_url = await self.scrape_page(page, url, file_name)
                                if next_url:
                                    url = urljoin(base_url, next_url)
                                    page_num += 1
                                else:
                                    break
                            success = True
                        except Exception as e:
                            logging.error(f"Error during scraping: {e}")
                            retries += 1
                            if retries < 3:
                                logging.info(f"Retrying in 5 seconds... (Attempt {retries + 1})")
                                await asyncio.sleep(5)
                            else:
                                logging.info("Max retries reached. Moving to previous month.")
                                current_date = current_date.replace(day=1) - timedelta(days=1)
                                next_month = current_date

                    current_date = next_month + timedelta(days=1)

                return "Scraping completed successfully."

            except Exception as e:
                logging.error(f"Error during scraping: {e}")
                return None
            finally:
                await browser.close()

    async def run(self, base_url, start_date, end_date):
        result = await self.scrape(base_url, start_date, end_date)
        if result:
            return result
        return "Failed to complete scraping."

async def main():
    scraper = AdvancedScraper()
    base_url = "https://www.courtlistener.com/?q=employment%20discrimination&type=o&order_by=dateFiled%20asc&stat_Precedential=on"
    start_date = datetime(2010, 12, 1)
    end_date = datetime(2024, 8, 1)
    result = await scraper.run(base_url, start_date, end_date)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
