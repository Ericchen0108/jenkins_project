import time
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from config.config import TestConfig


class WaitHelpers:
    
    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=TestConfig.DEFAULT_TIMEOUT):
        try:
            wait = WebDriverWait(driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return None
    
    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=TestConfig.DEFAULT_TIMEOUT):
        try:
            wait = WebDriverWait(driver, timeout)
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            return None
    
    @staticmethod
    def wait_for_element_present(driver, locator, timeout=TestConfig.DEFAULT_TIMEOUT):
        try:
            wait = WebDriverWait(driver, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return None
    
    @staticmethod
    def wait_for_text_in_element(driver, locator, text, timeout=TestConfig.DEFAULT_TIMEOUT):
        try:
            wait = WebDriverWait(driver, timeout)
            return wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_url_contains(driver, url_fragment, timeout=TestConfig.DEFAULT_TIMEOUT):
        try:
            wait = WebDriverWait(driver, timeout)
            return wait.until(EC.url_contains(url_fragment))
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_page_title_contains(driver, title, timeout=TestConfig.DEFAULT_TIMEOUT):
        try:
            wait = WebDriverWait(driver, timeout)
            return wait.until(EC.title_contains(title))
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_and_retry(func, max_attempts=3, delay=1):
        for attempt in range(max_attempts):
            try:
                result = func()
                if result:
                    return result
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(delay)
        return False


class TestDataHelpers:
    
    @staticmethod
    def get_search_terms():
        return [
            "Python programming",
            "Selenium automation",
            "Web development",
            "Machine learning",
            "Technology news",
            "Music videos",
            "Educational content",
            "Documentary films",
            "Tutorial videos",
            "Entertainment"
        ]
    
    @staticmethod
    def get_invalid_search_terms():
        return [
            "",
            "   ",
            "xyzxyzxyznonexistentcontentxyzxyz",
            "!@#$%^&*()",
            "    invalid    spaces    "
        ]
    
    @staticmethod
    def get_browser_resolutions():
        return [
            (1920, 1080),
            (1366, 768),
            (1024, 768),
            (800, 600),
            (1440, 900)
        ]
    
    @staticmethod
    def get_test_timeouts():
        return {
            "short": 5,
            "medium": 10,
            "long": 30,
            "very_long": 60
        }


class ValidationHelpers:
    
    @staticmethod
    def is_valid_youtube_url(url):
        youtube_domains = ["youtube.com", "www.youtube.com", "m.youtube.com"]
        return any(domain in url for domain in youtube_domains)
    
    @staticmethod
    def is_video_url(url):
        return "watch?v=" in url
    
    @staticmethod
    def is_search_url(url):
        return "search_query=" in url
    
    @staticmethod
    def validate_video_title(title):
        if not title or len(title.strip()) == 0:
            return False
        if len(title) > 200:
            return False
        return True
    
    @staticmethod
    def validate_channel_name(channel_name):
        if not channel_name or len(channel_name.strip()) == 0:
            return False
        if len(channel_name) > 100:
            return False
        return True
    
    @staticmethod
    def validate_view_count(view_count_text):
        if not view_count_text:
            return False
        
        view_indicators = ["view", "watching", "views"]
        return any(indicator in view_count_text.lower() for indicator in view_indicators)


class ScrollHelpers:
    
    @staticmethod
    def scroll_to_element(driver, element):
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(1)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def scroll_to_bottom(driver):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def scroll_to_top(driver):
        try:
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def scroll_by_pixels(driver, x_pixels=0, y_pixels=300):
        try:
            driver.execute_script(f"window.scrollBy({x_pixels}, {y_pixels});")
            time.sleep(1)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def smooth_scroll_to_element(driver, locator, timeout=10):
        element = WaitHelpers.wait_for_element_present(driver, locator, timeout)
        if element:
            return ScrollHelpers.scroll_to_element(driver, element)
        return False


class BrowserHelpers:
    
    @staticmethod
    def maximize_window(driver):
        try:
            driver.maximize_window()
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def set_window_size(driver, width, height):
        try:
            driver.set_window_size(width, height)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def refresh_page(driver):
        try:
            driver.refresh()
            time.sleep(2)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def go_back(driver):
        try:
            driver.back()
            time.sleep(2)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def go_forward(driver):
        try:
            driver.forward()
            time.sleep(2)
            return True
        except WebDriverException:
            return False
    
    @staticmethod
    def get_current_url(driver):
        try:
            return driver.current_url
        except WebDriverException:
            return ""
    
    @staticmethod
    def get_page_title(driver):
        try:
            return driver.title
        except WebDriverException:
            return ""


class RetryHelpers:
    
    @staticmethod
    def retry_on_exception(func, max_attempts=3, delay=1, exceptions=(Exception,)):
        for attempt in range(max_attempts):
            try:
                return func()
            except exceptions as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(delay)
        return None
    
    @staticmethod
    def retry_until_success(func, max_attempts=5, delay=2):
        for attempt in range(max_attempts):
            result = func()
            if result:
                return result
            time.sleep(delay)
        return False