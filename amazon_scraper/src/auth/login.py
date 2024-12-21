from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import AMAZON_EMAIL, AMAZON_PASSWORD, BASE_URL
from src.utils.logger import setup_logger
import time

logger = setup_logger(__name__)

class AmazonAuth:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    def login(self):
        """Login to Amazon using credentials from config"""
        try:
            logger.info("Starting Amazon login process")
            
            # Navigate to Amazon homepage
            self.driver.get(BASE_URL)
            time.sleep(3)
            
            # Click sign-in button
            sign_in = self.wait.until(
                EC.element_to_be_clickable((By.ID, "nav-link-accountList"))
            )
            sign_in.click()
            time.sleep(2)
            
            # Enter email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            email_field.clear()
            email_field.send_keys(AMAZON_EMAIL)
            
            # Click continue
            continue_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "continue"))
            )
            continue_btn.click()
            time.sleep(2)
            
            # Enter password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_field.clear()
            password_field.send_keys(AMAZON_PASSWORD)
            
            # Click sign-in
            sign_in_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "signInSubmit"))
            )
            sign_in_btn.click()
            
            # Wait for login to complete and verify
            time.sleep(5)
            
            # Verify login success
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.ID, "nav-link-accountList-nav-line-1"))
                )
                logger.info("Successfully logged in to Amazon")
                
                # Navigate to Best Sellers page after successful login
                self.driver.get("https://www.amazon.in/gp/bestsellers")
                time.sleep(3)
                
                return True
            except:
                logger.error("Failed to verify login success")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return False 