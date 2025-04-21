import logging

log_file = 'scraper.log'

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filemode='a'
)

logger = logging.getLogger(__name__)
