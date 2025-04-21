# Web Scraper with APScheduler

This Python project scrapes quotes from [quotes.toscrape.com](https://quotes.toscrape.com/), stores them in a MySQL database, and runs every 15 minutes using APScheduler.

## Features

- Scrapes quotes, authors, and tags from the website.
- Stores scraped data in a MySQL database.
- Runs the scraper every 15 minutes using APScheduler.

## Setup

### 1. Install dependencies

Create a virtual environment and install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Set up the MySQL database

Before running the scraper, ensure you have a MySQL database set up. Create a `.env` file in the root of the project with the following content:

```ini
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```

Replace the placeholders with your actual MySQL credentials.

### 3. Create the MySQL table

The script will automatically create the necessary table in the database. If you want to create it manually, run the following SQL command:

```sql
CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT,
    author VARCHAR(255),
    tags VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(text(255))
);
```

### 4. Run the scraper

To start the scraper and APScheduler, run the following command:

```bash
python3 main.py
```

This will start the APScheduler and execute the scraper every 15 minutes.

## File Structure

```bash
scraper/
│
├── scraper.py        # Main scraping logic
├── db.py             # Database connection and queries
├── log_config.py     # Logging configuration
├── scheduler.py      # APScheduler setup
│
└── main.py 
└── .env              # Environment variables (DB credentials)
```

## Testing

You can run the tests using `pytest`:

```bash
pytest
```

Make sure the `.env` file is present with the correct configuration before running the tests.

## License

MIT License. See LICENSE for more information.

