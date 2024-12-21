from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.scrapers.base import BaseScraper
from src.auth.login import AmazonAuth
import time
import logging
import json
from datetime import datetime
import os

logger = logging.getLogger(__name__)

CATEGORY_URLS = [
    "https://www.amazon.in/gp/bestsellers/kitchen/",
    "https://www.amazon.in/gp/bestsellers/electronics/",
    "https://www.amazon.in/gp/bestsellers/computers/",
    "https://www.amazon.in/gp/bestsellers/books/"
]

class ProductScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.auth = AmazonAuth(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        # Create data directory in the correct location
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'output')
        os.makedirs(self.data_dir, exist_ok=True)
        logger.info(f"Created directory: {self.data_dir}")

    def clean_price(self, price_text):
        """Clean price text and convert to float"""
        try:
            # Handle empty or invalid price text
            if not price_text or price_text == '.':
                return None
            
            # Remove currency symbol, commas and whitespace
            cleaned = price_text.replace('₹', '').replace(',', '').replace(' ', '').strip()
            
            # Handle cases where only dot is present
            if cleaned == '.':
                return None
            
            # Convert to float
            return float(cleaned)
        except Exception as e:
            logger.error(f"Error cleaning price: {str(e)}")
            return None

    def extract_product_details(self, product_element, category):
        """Extract all required product details according to requirements"""
        try:
            # Basic product info
            product_data = {
                "category_name": category,
                "product_name": None,
                "product_price": None,
                "sale_discount": None,
                "best_seller_rating": None,
                "ship_from": None,
                "sold_by": None,
                "rating": None,
                "product_description": None,
                "number_bought_past_month": None,
                "images": [],
                "url": None
            }

            # Get product name
            try:
                product_data["product_name"] = product_element.find_element(
                    By.CSS_SELECTOR, 
                    "div[class*='p13n-sc-truncate-desktop-type2']"
                ).text.strip()
            except:
                try:
                    product_data["product_name"] = product_element.find_element(
                        By.CSS_SELECTOR,
                        "div[class*='_cDEzb_p13n-sc-css-line-clamp-']"
                    ).text.strip()
                except:
                    logger.error("Could not find product name")
                    return None

            # Get product URL and navigate to product page
            try:
                product_data["url"] = product_element.find_element(
                    By.CSS_SELECTOR, 
                    "a[class*='a-link-normal'][href*='/dp/']"
                ).get_attribute("href")
                
                # Open product page in new tab
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.get(product_data["url"])
                time.sleep(2)

                # Get detailed information from product page
                try:
                    # Price information
                    price_element = self.driver.find_element(
                        By.CSS_SELECTOR, 
                        "span.a-price-whole"
                    )
                    price_text = price_element.text
                    if '.' not in price_text:
                        try:
                            fraction = self.driver.find_element(
                                By.CSS_SELECTOR, 
                                "span.a-price-fraction"
                            ).text
                            price_text = f"{price_text}.{fraction}"
                        except:
                            price_text = f"{price_text}.00"
                    
                    product_data["product_price"] = self.clean_price(price_text)
                    
                    # Original price and discount
                    try:
                        original_price_element = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "span.a-text-price span.a-offscreen"
                        )
                        original_price_text = original_price_element.get_attribute("innerHTML")
                        original_price = self.clean_price(original_price_text)
                        
                        if original_price and product_data["product_price"] and original_price > product_data["product_price"]:
                            discount = ((original_price - product_data["product_price"]) / original_price) * 100
                            product_data["sale_discount"] = round(discount, 2)
                    except Exception as e:
                        logger.warning(f"Error getting original price: {str(e)}")
                        product_data["sale_discount"] = 0

                    # Best seller rank
                    try:
                        rank_element = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "#SalesRank"
                        )
                        product_data["best_seller_rating"] = rank_element.text.split('#')[1].split(' ')[0]
                    except:
                        pass

                    # Shipping info
                    try:
                        product_data["ship_from"] = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "#tabular-buybox-container .tabular-buybox-text"
                        ).text
                    except:
                        pass

                    # Seller info
                    try:
                        product_data["sold_by"] = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "#merchant-info"
                        ).text
                    except:
                        pass

                    # Rating
                    try:
                        product_data["rating"] = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "#acrPopover"
                        ).get_attribute("title")
                    except:
                        pass

                    # Product description
                    try:
                        product_data["product_description"] = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "#productDescription"
                        ).text.strip()
                    except:
                        pass

                    # Number bought in past month
                    try:
                        bought_element = self.driver.find_element(
                            By.CSS_SELECTOR, 
                            "#social-proofing-faceout-title"
                        )
                        product_data["number_bought_past_month"] = bought_element.text
                    except:
                        pass

                    # Product images
                    try:
                        product_data["images"] = []
                        
                        # Get all image containers
                        image_containers = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            "#altImages li.imageThumbnail, #altImages li.a-spacing-small.item"
                        )
                        
                        for container in image_containers:
                            try:
                                # Get thumbnail image
                                img = container.find_element(By.TAG_NAME, "img")
                                thumb_url = img.get_attribute("src")
                                
                                if thumb_url and "images/I" in thumb_url:
                                    # Convert thumbnail URL to high-res URL
                                    # Example: from '.../I/41abc123_SX38_SY50_CR,0,0,38,50_.jpg'
                                    # to '.../I/41abc123.jpg'
                                    base_url = thumb_url.split('_S')[0]  # Get base URL before size suffix
                                    if base_url:
                                        # Remove any remaining modifiers
                                        high_res_url = base_url.split('._')[0] + '.jpg'
                                        
                                        # Add if it's a unique product image
                                        if (high_res_url not in product_data["images"] and 
                                            "play-button" not in high_res_url and 
                                            "sprite" not in high_res_url and
                                            "overlay" not in high_res_url and
                                            "icon" not in high_res_url):
                                            product_data["images"].append(high_res_url)
                                            logger.info(f"Added image: {high_res_url}")
                            
                            except Exception as e:
                                logger.error(f"Error processing image container: {str(e)}")
                                continue

                        # Get main product image if not already included
                        try:
                            main_image = self.driver.find_element(
                                By.CSS_SELECTOR,
                                "#landingImage, #imgBlkFront"
                            )
                            main_url = main_image.get_attribute("src")
                            if main_url and "images/I" in main_url:
                                high_res_main = main_url.split('_S')[0].split('._')[0] + '.jpg'
                                if high_res_main not in product_data["images"]:
                                    product_data["images"].insert(0, high_res_main)  # Add main image at start
                                    logger.info(f"Added main image: {high_res_main}")
                        except:
                            pass

                        # Additional image sources
                        try:
                            # Check for color variation images
                            color_images = self.driver.find_elements(
                                By.CSS_SELECTOR,
                                "#variation_color_name img, #color_name_0 img"
                            )
                            for img in color_images:
                                src = img.get_attribute("src")
                                if src and "images/I" in src:
                                    high_res_url = src.split('_S')[0].split('._')[0] + '.jpg'
                                    if high_res_url not in product_data["images"]:
                                        product_data["images"].append(high_res_url)
                                        logger.info(f"Added color variation image: {high_res_url}")
                        except:
                            pass

                        logger.info(f"Total images found: {len(product_data['images'])}")

                    except Exception as e:
                        logger.error(f"Error extracting images: {str(e)}")
                        product_data["images"] = []

                finally:
                    # Close product tab and switch back
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                # Only return products with >50% discount
                if product_data["sale_discount"] and product_data["sale_discount"] >= 50:
                    logger.info(f"Found product with {product_data['sale_discount']}% discount")
                    return product_data

            except Exception as e:
                logger.error(f"Error getting product details: {str(e)}")
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                return None

            return None

        except Exception as e:
            logger.error(f"Error in extract_product_details: {str(e)}")
            return None

    def scrape_category(self, category_url):
        """Scrape a single category"""
        products = []
        retries = 3
        max_products = 1500  # From requirements
        products_processed = 0
        
        for attempt in range(retries):
            try:
                self.driver.get(category_url)
                time.sleep(3)

                # Get category name
                category_name = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#zg_banner_text"))
                ).text.replace(" Best Sellers", "").strip()
                
                logger.info(f"Started scraping category: {category_name}")
                
                # Handle pagination - Amazon typically shows 50 items per page
                page = 1
                while products_processed < max_products:
                    logger.info(f"Processing page {page} of {category_name}")
                    
                    # Get all products on current page
                    product_elements = self.wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "div[class*='zg-grid-general-faceout']")
                        )
                    )
                    
                    logger.info(f"Found {len(product_elements)} products on page {page}")
                    
                    # Process products on current page
                    for element in product_elements:
                        try:
                            product_data = self.extract_product_details(element, category_name)
                            if product_data:
                                products.append(product_data)
                                logger.info(f"Found discounted product: {product_data.get('product_name', 'Unknown')} - {product_data.get('sale_discount')}% off")
                                
                                # Save incrementally
                                self.save_to_json(products, category_name.lower().replace(' ', '_'))
                        except Exception as e:
                            logger.error(f"Error processing product: {str(e)}")
                        
                        products_processed += 1
                        if products_processed >= max_products:
                            break
                    
                    # Try to go to next page
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                        if not next_button.is_enabled():
                            break
                        next_button.click()
                        page += 1
                        time.sleep(2)
                    except:
                        logger.info(f"No more pages available for {category_name}")
                        break
                
                logger.info(f"Completed scraping {category_name}. Found {len(products)} products with >50% discount")
                return products, category_name

            except Exception as e:
                logger.error(f"Error scraping category (attempt {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    return [], None
                time.sleep(5)

        return [], None

    def run(self):
        """Main scraping function"""
        try:
            if not self.auth.login():
                logger.error("Failed to login")
                return

            all_products = []
            for i, category_url in enumerate(CATEGORY_URLS, 1):
                logger.info(f"Processing category {i} of {len(CATEGORY_URLS)}")
                products, category_name = self.scrape_category(category_url)
                
                if products:
                    all_products.extend(products)
                    # Save individual category file
                    self.save_to_json(products, f"{category_name.lower().replace(' ', '_')}")
                    logger.info(f"Saved {len(products)} products from {category_name}")
                
                # Save cumulative file after each category
                if all_products:
                    self.save_to_json(all_products, "all_products")
                    logger.info(f"Updated all_products.json - Total products: {len(all_products)}")

            if not all_products:
                logger.warning("No products found with >50% discount")

        except Exception as e:
            logger.error(f"Error in scraper execution: {str(e)}")
        finally:
            self.close()

    def save_to_json(self, data, filename):
        """Save data to JSON file with proper structure"""
        try:
            # Ensure the data directory exists
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
                logger.info(f"Created directory: {self.data_dir}")

            # Save with category name only (without timestamp)
            filepath = os.path.join(self.data_dir, f"{filename}.json")

            # Save with proper formatting
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "scrape_date": datetime.now().isoformat(),
                    "total_products": len(data),
                    "products": data
                }, f, indent=4, ensure_ascii=False)
                
            logger.info(f"Successfully saved {len(data)} products to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False