import pytest
from unittest.mock import patch
from scraper.scraper import scrape_quotes
from scraper.db import insert_quotes, create_table, get_all_quotes

# Set up logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def setup_db():
    """Fixture to create the table before running the tests."""
    create_table()
    yield
    logger.info("Test setup complete. Teardown can be performed if needed.")

def test_scrape_and_insert_quotes(setup_db):
    """Test the scraping and insertion of quotes."""
    try:
        quotes = scrape_quotes()

        assert quotes, "No quotes were scraped."

        insert_quotes(quotes)
        logger.info(f"Inserted {len(quotes)} quotes into the database.")

        all_quotes = get_all_quotes()
        assert len(all_quotes) >= len(quotes), "Not all quotes were inserted successfully."

        logger.info(f"Test passed: {len(quotes)} quotes were inserted and verified.")

    except Exception as e:
        logger.error(f"Test failed: {e}")
        pytest.fail(f"Test failed due to exception: {e}") 

@patch('test_scraper.scrape_quotes', return_value=[])
def test_scraping_no_quotes(mock_scrape, setup_db):
    """Test the case when no quotes are scraped."""
    quotes = scrape_quotes()

    # Assert that no quotes were scraped (the mocked return value)
    assert not quotes, "Test failed: Expected no quotes to be scraped."
    assert mock_scrape.call_count == 1, "scrape_quotes mock was not called."
    assert quotes == [], "Returned value was not an empty list as expected from mock."


    logger.info("Test passed: No quotes were scraped as expected.")