from apscheduler.schedulers.blocking import BlockingScheduler
from scraper.scraper import scrape_quotes
from scraper.db import insert_quotes
from scraper.log_config import logger 

def scheduled_job():
    """Implement proper log detailing operations."""
    logger.info("Scraping job started...")
    try:
        # Scrape quotes
        quotes = scrape_quotes()
        
        if not quotes:
            logger.warning("No quotes found during scraping.")
        
        # Insert quotes into the database
        if quotes:
            insert_quotes(quotes)
            logger.info(f"Scraped and inserted {len(quotes)} quotes.")
        else:
            logger.info("No quotes to insert.")

    except Exception as e:
        logger.error(f"Scraping job failed: {e}")

def start_scheduler():
    """Create a task scheduler that runs every 15 minutes."""
    scheduler = BlockingScheduler()

    # Add scheduled job every 15 minutes
    scheduler.add_job(scheduled_job, 'interval', minutes=15)
    logger.info("Scheduler started. Job runs every 15 minutes.")

    try:
        # Start the scheduler
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped manually.")
    except Exception as e:
        logger.error(f"Scheduler encountered an error: {e}")
        raise
