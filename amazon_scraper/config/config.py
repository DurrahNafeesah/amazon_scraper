from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Amazon credentials
AMAZON_EMAIL = os.getenv('AMAZON_EMAIL')
AMAZON_PASSWORD = os.getenv('AMAZON_PASSWORD')

# URLs
BASE_URL = "https://www.amazon.in"
BESTSELLER_URL = "https://www.amazon.in/gp/bestsellers/"

# Category URLs
CATEGORY_URLS = [
    "https://www.amazon.in/gp/bestsellers/kitchen/",
    "https://www.amazon.in/gp/bestsellers/shoes/",
    "https://www.amazon.in/gp/bestsellers/computers/",
    "https://www.amazon.in/gp/bestsellers/electronics/",
    "https://www.amazon.in/gp/bestsellers/beauty/",
    "https://www.amazon.in/gp/bestsellers/clothing/",
    "https://www.amazon.in/gp/bestsellers/sporting-goods/",
    "https://www.amazon.in/gp/bestsellers/home-improvement/",
    "https://www.amazon.in/gp/bestsellers/toys/",
    "https://www.amazon.in/gp/bestsellers/books/"
]

# Scraping settings
MAX_PRODUCTS_PER_CATEGORY = 1500
MIN_DISCOUNT_PERCENTAGE = 50

# Selenium settings
IMPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 30

# Output settings
OUTPUT_DIR = "../data/output"
LOG_DIR = "../logs" 