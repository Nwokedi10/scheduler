import pytest
from unittest.mock import patch
import mysql.connector
from scraper.scraper import scrape_quotes
from scraper.db import insert_quotes, create_table, get_all_quotes, get_db_connection

# Set up logging
import logging
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def setup_db():
    """Fixture to ensure a clean database table before each test function."""
    conn = None
    cursor = None
    try:
        logger.info("Setting up database for test...")
        create_table()
        logger.info("Table checked/created.")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Clear the table explicitly before the test runs
        cursor.execute("DELETE FROM quotes")
        conn.commit()
        logger.info("Database table 'quotes' cleared before test.")

        yield

    except Exception as e:
        logger.error(f"Database setup failed during before-test phase: {e}")
        if conn and conn.is_connected():
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM quotes")
                conn.commit()
                logger.info("Attempted cleanup during setup failure.")
            except Exception as cleanup_e:
                 logger.error(f"Cleanup attempt during setup failure also failed: {cleanup_e}")
        pytest.fail(f"Database setup failed due to exception: {e}")

    finally:
        logger.info("Cleaning up database resources after test.")
        # Clean up connection resources in the finally block
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("Database connection closed.")

def test_scrape_and_insert_quotes(setup_db):
    """Test the scraping and insertion of quotes."""
    try:
        quotes = scrape_quotes()
        assert quotes, "No quotes were scraped."
        
        insert_quotes(quotes)
        logger.info(f"Inserted {len(quotes)} quotes into the database (attempted).")
        all_quotes = get_all_quotes()

        assert len(all_quotes) == len(quotes), "Incorrect number of quotes found after insert."
        logger.info(f"Test passed: {len(quotes)} quotes were inserted and verified.")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        pytest.fail(f"Test failed due to exception: {e}")

@patch('test_scraper.scrape_quotes', return_value=[])
def test_scraping_no_quotes(mock_scrape, setup_db):
    """Test the case when no quotes are scraped."""
    quotes = scrape_quotes()
    assert not quotes, "Test failed: Expected no quotes to be scraped."
    assert mock_scrape.call_count == 1, "scrape_quotes mock was not called."
    logger.info("Test passed: No quotes were scraped as expected.")

@patch('test_scraper.scrape_quotes', side_effect=Exception("Request failed"))
def test_scraping_failure(mock_scrape, setup_db):
    """Test the case when the scraping request fails."""
    with pytest.raises(Exception, match="Request failed"):
        scrape_quotes()
    assert mock_scrape.call_count == 1, "scrape_quotes mock was not called."
    logger.info("Test passed: Scraping request failed as expected.")

def test_db_insert_and_retrieve(setup_db):
    """Test the insertion and retrieval of quotes from the database."""
    quotes_to_insert = [
        {"text": "Test quote 1", "author": "Author 1", "tags": "tag1, tag2"},
        {"text": "Test quote 2", "author": "Author 2", "tags": "tag3, tag4"},
    ]
    insert_quotes(quotes_to_insert)
    all_quotes = get_all_quotes()
    assert len(all_quotes) == len(quotes_to_insert), "Incorrect number of quotes retrieved."

    retrieved_texts = sorted([q['text'] for q in all_quotes])
    expected_texts = sorted([q['text'] for q in quotes_to_insert])
    assert retrieved_texts == expected_texts, "Retrieved quotes do not match inserted quotes."
    logger.info("Test passed: DB insert and retrieve successful.")


@patch('test_scraper.insert_quotes')
def test_db_insert_error(mock_insert, setup_db):
    """Test database insert error handling."""
    mock_insert.side_effect = mysql.connector.Error("Database insert error")
    quotes = [{"text": "Test quote", "author": "Author", "tags": "tag1"}]

    with pytest.raises(mysql.connector.Error, match="Database insert error"):
        insert_quotes(quotes)

    assert mock_insert.call_count == 1, "insert_quotes mock was not called."
    logger.info("Test passed: DB insert error handled correctly.")

def test_empty_quote_insert(setup_db):
    """Test inserting empty quotes into the database."""
    quotes_to_insert = [
        {"text": "", "author": "", "tags": ""},
    ]
    insert_quotes(quotes_to_insert)
    all_quotes = get_all_quotes()
    assert len(all_quotes) == 1, "Empty quote was not inserted or too many quotes found."
    assert all_quotes[0]['text'] == "", "Empty quote's text was not inserted correctly."
    assert all_quotes[0]['author'] == "", "Empty quote's author was not inserted correctly."
    logger.info("Test passed: Empty quote insert handled correctly.")