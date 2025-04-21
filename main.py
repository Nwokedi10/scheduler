from scraper.db import create_table
from scraper.scheduler import start_scheduler

if __name__ == "__main__":
    create_table()
    start_scheduler()
