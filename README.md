# Web Scraper for Court Listener

Web scraper designed to extract employment discrimination case data from the Court Listener website. It uses asynchronous programming and the Playwright library to navigate and scrape web pages while simulating human-like behavior to avoid detection.

## Features

- Asynchronous scraping using `asyncio` and Playwright
- Date range-based scraping
- Automatic pagination handling
- Human-like behavior simulation (mouse movements, scrolling)
- User-agent rotation
- Error handling and retry mechanism
- CAPTCHA solving capability (placeholder)
- Saves scraped content as HTML files

## Requirements

- Python 3.7+
- Playwright
- asyncio

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/advanced-court-listener-scraper.git
   cd advanced-court-listener-scraper
   ```

2. Install the required packages:
   ```
   pip install playwright asyncio
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

1. Modify the `main()` function in the script to set your desired parameters:
   - `base_url`: The base URL for Court Listener search results
   - `start_date`: The start date for your search range
   - `end_date`: The end date for your search range

2. Run the script:
   ```
   python advanced_scraper.py
   ```

3. The script will create a `scraped_pages` directory and save the HTML content of each scraped page as separate files.

## Configuration

- User Agents: Add or modify the list of user agents in the `AdvancedScraper` class to expand the rotation.
- Proxies: If you want to use proxies, add them to the `proxies` list in the `AdvancedScraper` class.

## Customization

- CAPTCHA Solving: Implement your CAPTCHA solving logic in the `solve_captcha` method if needed.
- Scraping Logic: Modify the `scrape_page` method to extract specific data from the pages if required.

## Ethical Considerations

This scraper is designed for educational and research purposes. Always respect the website's terms of service and robots.txt file. Consider implementing rate limiting and be mindful of the load you put on the target website.

## Disclaimer

This tool is provided as-is, without any guarantees or warranty. The authors are not responsible for any damage or data loss incurred from using this scraper. Use at your own risk and responsibility.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/advanced-court-listener-scraper/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
