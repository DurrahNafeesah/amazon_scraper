# Amazon Best Sellers Scraper

A Python-based web scraper that extracts information from Amazon's Best Sellers section using Selenium.

## Features
- Authenticates using Amazon credentials
- Scrapes top 1500 best-selling products from 10 categories
- Focuses on products with >50% discount
- Extracts detailed product information
- Stores data in CSV/JSON format

## Setup
1. Clone the repository
2. Install dependencies:   ```bash
   pip install -r requirements.txt   ```
3. Create a `.env` file in the config directory with your Amazon credentials:   ```
   AMAZON_EMAIL=your_email
   AMAZON_PASSWORD=your_password   ```

## Usage
Run the scraper: 