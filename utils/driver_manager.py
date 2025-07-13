from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
from typing import Optional


class DriverManager:
    
    @staticmethod
    def get_driver(browser: str = "chrome", headless: bool = False) -> webdriver.Remote:
        browser = browser.lower()
        
        if browser == "chrome":
            return DriverManager._get_chrome_driver(headless)
        elif browser == "firefox":
            return DriverManager._get_firefox_driver(headless)
        elif browser == "edge":
            return DriverManager._get_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _get_chrome_driver(headless: bool = False) -> webdriver.Chrome:
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    @staticmethod
    def _get_firefox_driver(headless: bool = False) -> webdriver.Firefox:
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    @staticmethod
    def _get_edge_driver(headless: bool = False) -> webdriver.Edge:
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    @staticmethod
    def quit_driver(driver: Optional[webdriver.Remote]) -> None:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")