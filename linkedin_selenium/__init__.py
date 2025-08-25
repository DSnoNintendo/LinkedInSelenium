import html
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
from seleniumbase import Driver

class LinkedInBrowser:
    
    
    def __init__(self):
        self.profile_pic_selector = (By.CSS_SELECTOR, "button[aria-label='open profile picture'] img.pv-top-card-profile-picture__image--show")
        self.login_validation_selector = (By.CSS_SELECTOR, "svg.mercado-match[data-supported-dps='24x24']")
        
        try:
            self.driver = Driver(
                uc=True,
                headless=True,
            )
            self.driver.get("https://www.linkedin.com/login")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize WebDriver: {str(e)}")
        
        load_dotenv()
        
        # Get credentials from environment variables
        self.username = os.environ.get("LINKEDIN_USER")
        self.password = os.environ.get("LINKEDIN_PASSWORD")
        
        if not all([self.username, self.password]):
            self.driver.quit()
            raise ValueError(
                "Missing LinkedIn credentials in environment variables. "
                "Please set LINKEDIN_USER and LINKEDIN_PASSWORD."
            )

    def login(self):
        try:
            # Wait for login elements
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Fill in credentials
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Click login button
            submit_button = self.driver.find_element(
                By.XPATH, "//button[@type='submit' and contains(text(), 'Sign in')]")
            submit_button.click()

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.login_validation_selector)
            )
            
            print("Successfully logged in to LinkedIn!")
        except Exception as e:
            print(f"Login error: {str(e)}")
            self.driver.save_screenshot("login_error.png")
            self.driver.quit()
            raise

    def get_profile_picture_element(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.profile_pic_selector)
        )
        return element
        
    def get_url_from_element(self, element):
        pattern = r'src="([^"]*)"'
        encoded_url = re.search(pattern, element.get_attribute('outerHTML')).group(1)
        decoded_url = html.unescape(encoded_url)
        return decoded_url
    
    def go_to_profile(self, profile_url):
        self.driver.get(profile_url)

    def get_profile_picture_from_url(self, url) -> str | None:
        self.driver.get(url)
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.profile_pic_selector)
        )

        if self.picture_valid(element):
            return self.get_url_from_element(element)

        return None
    
    def picture_valid(self, element):
        # default image
        if "http" not in self.get_url_from_element(element):
            return False
        return True
    
    def close(self):
        if hasattr(self, "driver"):
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "driver"):
            self.driver.quit()
            
    def __del__(self):
        if hasattr(self, "driver"):
            self.driver.quit()
