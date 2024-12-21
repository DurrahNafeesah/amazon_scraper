from src.scrapers.product import ProductScraper
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    try:
        scraper = ProductScraper()
        scraper.run()
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main() 