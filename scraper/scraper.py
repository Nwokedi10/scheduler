import requests
from bs4 import BeautifulSoup
from scraper.log_config import logger
import time

def scrape_quotes():
    """Scrape quotes from the 'quotes.toscrape.com' website."""
    url = "https://quotes.toscrape.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    retries = 3
    for attempt in range(retries):
        try:
            # Send a GET request with a timeout of 10 seconds (increased timeout for reliability)
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Successfully fetched URL: {url}")
            break  # Exit loop if request is successful
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                logger.warning(f"Error fetching URL on attempt {attempt + 1}/{retries}: {e}. Retrying...")
                time.sleep(2)  # Wait before retrying
            else:
                logger.error(f"Error fetching URL after {retries} attempts: {e}")
                return []  # Return empty list if all retries fail

    soup = BeautifulSoup(response.text, 'html.parser')

    quotes_data = []
    quotes = soup.select('.quote')
    if not quotes:
        logger.warning("No quotes found on the page.")

    for quote in quotes:
        try:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.select('.tags .tag')]
            
            quotes_data.append({
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            })
        except AttributeError as e:
            logger.warning(f"Skipping a quote due to missing expected data: {e}")

    return quotes_data
