import requests
from bs4 import BeautifulSoup
from scraper.log_config import logger
def scrape_quotes():
    """Scrape quotes from the 'quotes.toscrape.com' website."""
    url = "https://quotes.toscrape.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    try:
        # Send a GET request with a timeout of 5 seconds
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL: {e}")
        return []

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
