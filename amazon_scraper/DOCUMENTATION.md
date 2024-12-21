# Amazon Best Sellers Scraper - Documentation

## Overview
This Python-based web scraper extracts information about discounted products from Amazon's Best Sellers section. It focuses on products with discounts greater than 50% across 10 different categories, collecting detailed product information and storing it in JSON format.

## Features
- Automated login to Amazon using provided credentials
- Scrapes up to 1500 best-selling products per category
- Filters products with >50% discount
- Collects comprehensive product details:
  - Product Name
  - Current Price
  - Original Price and Discount
  - Best Seller Rating
  - Shipping Information
  - Seller Details
  - Product Rating
  - Product Description
  - Purchase Statistics
  - Product Images
- Saves data in structured JSON format
- Implements robust error handling
- Provides detailed logging

## Project Structure 
amazon_scraper/
├── config/
│ ├── init.py
│ ├── config.py # Configuration settings
│ └── .env # Credentials (not tracked in git)
├── data/
│ └── output/ # JSON output files
├── logs/ # Log files
├── src/
│ ├── auth/ # Authentication module
│ ├── scrapers/ # Scraping logic
│ └── utils/ # Utility functions
├── requirements.txt # Dependencies
├── README.md # Basic setup instructions
└── main.py # Entry point


## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Chrome browser installed
- Valid Amazon account credentials

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd amazon_scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure credentials:
   - Create `.env` file in the config directory
   - Add your Amazon credentials:
     ```
     AMAZON_EMAIL=your_amazon_email
     AMAZON_PASSWORD=your_amazon_password
     ```

### Configuration Options
Edit `config/config.py` to modify:
- Category URLs
- Maximum products per category
- Minimum discount percentage
- Timeout settings
- Output directory paths

## Usage Guide

### Basic Usage
Run the scraper:
```bash
python main.py
```

### Output Files
The scraper generates two types of JSON files in `data/output/`:
1. Category-specific files: `<category_name>.json`
2. Combined file: `all_products.json`

### JSON Structure
json
{
"scrape_date": "2024-12-18T12:00:00",
"total_products": 10,
"products": [
{
"category_name": "Electronics",
"product_name": "Product Example",
"product_price": 499.99,
"sale_discount": 55.5,
"best_seller_rating": "1",
"ship_from": "Amazon",
"sold_by": "Seller Name",
"rating": "4.5 out of 5",
"product_description": "Product description...",
"number_bought_past_month": "1000+ bought in past month",
"images": ["url1", "url2"],
"url": "product_url"
}
]
}


### Logging
- Logs are stored in `logs/` directory
- Format: `scraper_YYYYMMDD_HHMMSS.log`
- Contains detailed information about:
  - Scraping progress
  - Errors and exceptions
  - Product processing status
  - Save operations

## Error Handling
The scraper implements comprehensive error handling for:
- Network issues
- Missing elements
- Invalid data
- Authentication failures
- Page loading timeouts

## Performance Considerations
- Uses Chrome WebDriver with optimized settings
- Implements delays to respect Amazon's rate limits
- Saves data incrementally to prevent data loss
- Handles pagination automatically

## Limitations
- Subject to Amazon's rate limiting
- Requires valid Amazon credentials
- May be affected by Amazon's layout changes
- Limited to 1500 products per category

## Troubleshooting
1. Login Issues:
   - Verify credentials in `.env`
   - Check network connectivity
   - Ensure no captcha requirements

2. No Data Collected:
   - Verify discount threshold
   - Check category URLs
   - Review log files for errors

3. Browser Issues:
   - Update Chrome browser
   - Clear browser cache
   - Check ChromeDriver compatibility

## Maintenance
- Regularly update dependencies
- Monitor Amazon's HTML structure changes
- Review and update selectors as needed
- Check log files for potential issues

## Compliance
- Respects Amazon's robots.txt
- Implements reasonable delays
- Uses legitimate authentication
- Follows rate limiting guidelines

## Support
For issues and questions:
1. Check log files
2. Review error messages
3. Verify configuration
4. Contact project maintainers

##Note:
This program was run for only 10 minutes. Running it for a longer duration will result in storing additional product data, as more data will be processed and saved over time.
