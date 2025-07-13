import pytest
import os
from datetime import datetime
from utils.driver_manager import DriverManager
from config.config import TestConfig


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    TestConfig.ensure_directories_exist()


@pytest.fixture(scope="function")
def driver():
    driver_instance = DriverManager.get_driver(
        browser=TestConfig.BROWSER, 
        headless=TestConfig.HEADLESS
    )
    driver_instance.implicitly_wait(TestConfig.IMPLICIT_WAIT)
    driver_instance.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
    
    yield driver_instance
    
    DriverManager.quit_driver(driver_instance)


@pytest.fixture(scope="function")
def chrome_driver():
    driver_instance = DriverManager.get_driver(browser="chrome", headless=TestConfig.HEADLESS)
    driver_instance.implicitly_wait(TestConfig.IMPLICIT_WAIT)
    driver_instance.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
    
    yield driver_instance
    
    DriverManager.quit_driver(driver_instance)


@pytest.fixture(scope="function")
def firefox_driver():
    driver_instance = DriverManager.get_driver(browser="firefox", headless=TestConfig.HEADLESS)
    driver_instance.implicitly_wait(TestConfig.IMPLICIT_WAIT)
    driver_instance.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
    
    yield driver_instance
    
    DriverManager.quit_driver(driver_instance)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if TestConfig.SCREENSHOT_ON_FAILURE:
            driver = item.funcargs.get('driver')
            if driver:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"{item.name}_{timestamp}.png"
                screenshot_path = os.path.join(TestConfig.SCREENSHOTS_DIR, screenshot_name)
                
                try:
                    driver.save_screenshot(screenshot_path)
                    print(f"\nScreenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"\nFailed to save screenshot: {e}")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "youtube_search: mark test as YouTube search functionality test"
    )
    config.addinivalue_line(
        "markers", "youtube_video: mark test as YouTube video playback test"
    )
    config.addinivalue_line(
        "markers", "youtube_navigation: mark test as YouTube navigation test"
    )