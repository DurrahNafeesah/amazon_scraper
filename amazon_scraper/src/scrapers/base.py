from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from config.config import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT
from src.utils.logger import setup_logger
import os
import logging

logger = setup_logger(__name__)

class BaseScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Setup Chrome driver with optimized options"""
        try:
            chrome_options = Options()
            # Add options to prevent GPU/WebGPU errors
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-dev-shm-usage')
            # Additional stability options
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-popup-blocking')
            chrome_options.add_argument('--disable-extensions')
            # Performance options
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--silent')
            
            # Add these options to suppress GPU warnings
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--ignore-gpu-blocklist')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Create Chrome service
            service = Service()
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            logger.info("WebDriver setup completed successfully")
            
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {str(e)}")
            raise

    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed successfully")