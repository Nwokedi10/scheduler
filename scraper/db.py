import mysql.connector
import os
from dotenv import load_dotenv
from scraper.log_config import logger


load_dotenv()

def get_db_connection():
    """Set up the database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        logger.info("Database connection established successfully.")
        return connection
    except mysql.connector.Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def create_table():
    """Create the table in the database if it doesn't exist."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quotes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        text TEXT,
                        author VARCHAR(255),
                        tags VARCHAR(255),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(text(255))
                    )
                """)
                conn.commit()
                logger.info("Table 'quotes' created or already exists.")
    except mysql.connector.Error as e:
        logger.error(f"Error creating table: {e}")
        raise

def insert_quotes(quotes):
    """Insert quotes into the quotes table."""
    if not quotes:
        logger.warning("No quotes to insert.")
        return

    insert_query = """
        INSERT INTO quotes (text, author, tags)
        VALUES (%s, %s, %s)
    """
    data = [(quote['text'], quote['author'], quote['tags']) for quote in quotes]

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(insert_query, data)
                conn.commit()
                logger.info(f"Inserted {len(data)} quotes into the database.")
    except mysql.connector.IntegrityError as e:
        logger.warning(f"Integrity error (likely duplicate quote): {e}")
    except mysql.connector.Error as e:
        logger.error(f"Error inserting quotes: {e}")
        raise

def get_all_quotes():
    """Retrieve all quotes, including their timestamps."""
    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM quotes")
                quotes = cursor.fetchall()
                logger.info(f"Retrieved {len(quotes)} quotes from the database.")
                return quotes
    except mysql.connector.Error as e:
        logger.error(f"Error fetching quotes: {e}")
        raise
