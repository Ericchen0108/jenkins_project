from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Optional, List
import time


class BasePage:
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
    
    def navigate_to(self, url: str) -> None:
        self.driver.get(url)
    
    def get_current_url(self) -> str:
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        return self.driver.title
    
    def find_element(self, locator: tuple) -> Optional[WebElement]:
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return None
    
    def find_elements(self, locator: tuple) -> List[WebElement]:
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []
    
    def find_clickable_element(self, locator: tuple) -> Optional[WebElement]:
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            return None
    
    def click_element(self, locator: tuple) -> bool:
        element = self.find_clickable_element(locator)
        if element:
            element.click()
            return True
        return False
    
    def send_keys_to_element(self, locator: tuple, text: str) -> bool:
        element = self.find_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False
    
    def get_element_text(self, locator: tuple) -> str:
        element = self.find_element(locator)
        return element.text if element else ""
    
    def get_element_attribute(self, locator: tuple, attribute: str) -> str:
        element = self.find_element(locator)
        return element.get_attribute(attribute) if element else ""
    
    def is_element_visible(self, locator: tuple) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator: tuple) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_to_disappear(self, locator: tuple) -> bool:
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator: tuple) -> bool:
        element = self.find_element(locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return True
        return False
    
    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def scroll_to_top(self) -> None:
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def refresh_page(self) -> None:
        self.driver.refresh()
    
    def switch_to_window(self, window_handle: str) -> None:
        self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self) -> List[str]:
        return self.driver.window_handles
    
    def take_screenshot(self, filename: str) -> bool:
        try:
            return self.driver.save_screenshot(filename)
        except Exception:
            return False
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        if timeout is None:
            timeout = self.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False