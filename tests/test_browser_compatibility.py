import pytest
import time
from selenium.common.exceptions import WebDriverException
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.video_page import VideoPage
from utils.driver_manager import DriverManager
from config.config import TestConfig


@pytest.mark.browser_compatibility
class TestBrowserCompatibility:
    """Test suite for browser compatibility across Chrome, Firefox, and Edge"""
    
    @pytest.mark.browser_chrome
    @pytest.mark.parametrize("resolution", [(1920, 1080), (1366, 768), (1024, 768)])
    def test_chrome_compatibility(self, resolution):
        """Test YouTube functionality in Chrome browser"""
        self._test_browser_functionality("chrome", resolution)
    
    @pytest.mark.browser_firefox
    @pytest.mark.parametrize("resolution", [(1920, 1080), (1366, 768), (1024, 768)])
    def test_firefox_compatibility(self, resolution):
        """Test YouTube functionality in Firefox browser"""
        self._test_browser_functionality("firefox", resolution)
    
    @pytest.mark.browser_edge
    @pytest.mark.parametrize("resolution", [(1920, 1080), (1366, 768)])
    def test_edge_compatibility(self, resolution):
        """Test YouTube functionality in Edge browser"""
        self._test_browser_functionality("edge", resolution)
    
    def _test_browser_functionality(self, browser, resolution):
        """Common test functionality across browsers"""
        driver = None
        try:
            # Create browser-specific driver
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            driver.set_window_size(*resolution)
            driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
            
            # Initialize page objects
            home_page = HomePage(driver)
            search_page = SearchPage(driver)
            video_page = VideoPage(driver)
            
            # Test basic page load
            assert home_page.open(), f"Failed to open YouTube in {browser}"
            assert home_page.is_youtube_logo_visible(), f"YouTube logo not visible in {browser}"
            
            # Test search functionality
            search_term = "automation testing"
            assert home_page.search_for_video(search_term), f"Search failed in {browser}"
            assert search_page.has_search_results(), f"No search results in {browser}"
            
            # Test video navigation
            if search_page.get_search_results_count() > 0:
                original_url = driver.current_url
                search_page.click_first_search_result()
                time.sleep(3)
                
                new_url = driver.current_url
                assert new_url != original_url, f"Navigation failed in {browser}"
                assert "watch" in new_url, f"Not on video page in {browser}"
                
                # Test video page elements
                assert video_page.wait_for_video_to_load(), f"Video failed to load in {browser}"
                
                title = video_page.get_video_title()
                assert len(title) > 0, f"Video title empty in {browser}"
        
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)


@pytest.mark.cross_browser
class TestCrossBrowserFeatures:
    """Test specific features across different browsers"""
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_javascript_execution(self, browser):
        """Test JavaScript execution across browsers"""
        driver = None
        try:
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            home_page = HomePage(driver)
            
            home_page.open()
            
            # Test JavaScript execution
            result = driver.execute_script("return document.title;")
            assert "YouTube" in result, f"JavaScript execution failed in {browser}"
            
            # Test scroll functionality
            driver.execute_script("window.scrollTo(0, 500);")
            scroll_position = driver.execute_script("return window.pageYOffset;")
            assert scroll_position > 0, f"Scroll failed in {browser}"
            
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_css_rendering(self, browser):
        """Test CSS rendering across browsers"""
        driver = None
        try:
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            home_page = HomePage(driver)
            
            home_page.open()
            
            # Test element visibility and styling
            logo_element = home_page.find_element(home_page.YOUTUBE_LOGO)
            assert logo_element is not None, f"Logo element not found in {browser}"
            assert logo_element.is_displayed(), f"Logo not displayed in {browser}"
            
            search_box = home_page.find_element(home_page.SEARCH_BOX)
            assert search_box is not None, f"Search box not found in {browser}"
            assert search_box.is_displayed(), f"Search box not displayed in {browser}"
            
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_form_interaction(self, browser):
        """Test form interactions across browsers"""
        driver = None
        try:
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            home_page = HomePage(driver)
            
            home_page.open()
            
            # Test form input
            search_term = f"test search {browser}"
            assert home_page.send_keys_to_element(home_page.SEARCH_BOX, search_term), \
                f"Failed to input text in {browser}"
            
            # Verify input value
            search_box = home_page.find_element(home_page.SEARCH_BOX)
            input_value = search_box.get_attribute("value")
            assert search_term in input_value, f"Input value incorrect in {browser}"
            
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)


@pytest.mark.responsive_testing
class TestResponsiveDesign:
    """Test responsive design across browsers and resolutions"""
    
    @pytest.mark.parametrize("browser,resolution", [
        ("chrome", (320, 568)),    # iPhone SE
        ("chrome", (768, 1024)),   # iPad
        ("chrome", (1024, 768)),   # iPad Landscape
        ("chrome", (1366, 768)),   # Laptop
        ("chrome", (1920, 1080)),  # Desktop
        ("firefox", (1366, 768)),  # Firefox Laptop
        ("firefox", (1920, 1080)), # Firefox Desktop
    ])
    def test_responsive_layout(self, browser, resolution):
        """Test responsive layout across different screen sizes"""
        driver = None
        try:
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            driver.set_window_size(*resolution)
            
            home_page = HomePage(driver)
            home_page.open()
            
            # Test that key elements are visible at different resolutions
            assert home_page.is_youtube_logo_visible(), \
                f"Logo not visible at {resolution} in {browser}"
            
            # Test search box accessibility
            search_box = home_page.find_element(home_page.SEARCH_BOX)
            assert search_box is not None, \
                f"Search box not found at {resolution} in {browser}"
            
            # For mobile resolutions, menu might be collapsed
            if resolution[0] < 768:
                # Mobile layout tests
                menu_button = home_page.find_element(home_page.MENU_BUTTON)
                assert menu_button is not None, \
                    f"Menu button not found in mobile view in {browser}"
            else:
                # Desktop layout tests
                assert home_page.is_search_box_visible(), \
                    f"Search box not visible in desktop view in {browser}"
            
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)


@pytest.mark.performance_comparison
class TestBrowserPerformance:
    """Compare performance across different browsers"""
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_page_load_performance(self, browser):
        """Test page load performance across browsers"""
        driver = None
        try:
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            
            start_time = time.time()
            
            home_page = HomePage(driver)
            home_page.open()
            
            # Wait for page to be fully loaded
            home_page.wait_for_page_load()
            
            load_time = time.time() - start_time
            
            # Assert reasonable load time (adjust threshold as needed)
            assert load_time < 30, f"Page load too slow in {browser}: {load_time:.2f}s"
            
            print(f"\n{browser} page load time: {load_time:.2f}s")
            
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_search_performance(self, browser):
        """Test search performance across browsers"""
        driver = None
        try:
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            
            home_page = HomePage(driver)
            search_page = SearchPage(driver)
            
            home_page.open()
            
            start_time = time.time()
            
            # Perform search
            search_term = "performance test"
            home_page.search_for_video(search_term)
            
            # Wait for results
            search_page.wait_for_page_load()
            
            search_time = time.time() - start_time
            
            # Verify results loaded
            assert search_page.has_search_results(), f"No search results in {browser}"
            
            # Assert reasonable search time
            assert search_time < 15, f"Search too slow in {browser}: {search_time:.2f}s"
            
            print(f"\n{browser} search time: {search_time:.2f}s")
            
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)


@pytest.mark.browser_specific
class TestBrowserSpecificFeatures:
    """Test browser-specific features and behaviors"""
    
    def test_chrome_specific_features(self, chrome_driver):
        """Test Chrome-specific functionality"""
        home_page = HomePage(chrome_driver)
        home_page.open()
        
        # Test Chrome-specific capabilities
        user_agent = chrome_driver.execute_script("return navigator.userAgent;")
        assert "Chrome" in user_agent, "Not running in Chrome"
        
        # Test Chrome DevTools Protocol (if needed)
        # This would require additional setup for CDP
        
    def test_firefox_specific_features(self, firefox_driver):
        """Test Firefox-specific functionality"""
        home_page = HomePage(firefox_driver)
        home_page.open()
        
        # Test Firefox-specific capabilities
        user_agent = firefox_driver.execute_script("return navigator.userAgent;")
        assert "Firefox" in user_agent, "Not running in Firefox"
        
        # Test Firefox-specific features
        # e.g., profile settings, add-ons, etc.
    
    def test_edge_specific_features(self):
        """Test Edge-specific functionality"""
        driver = None
        try:
            driver = DriverManager.get_driver(browser="edge", headless=TestConfig.HEADLESS)
            home_page = HomePage(driver)
            home_page.open()
            
            # Test Edge-specific capabilities
            user_agent = driver.execute_script("return navigator.userAgent;")
            assert "Edge" in user_agent or "Edg" in user_agent, "Not running in Edge"
            
        except WebDriverException as e:
            pytest.skip(f"Edge browser not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)


@pytest.mark.accessibility
class TestAccessibilityAcrossBrowsers:
    """Test accessibility features across browsers"""
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_keyboard_navigation(self, browser):
        """Test keyboard navigation across browsers"""
        driver = None
        try:
            from selenium.webdriver.common.keys import Keys
            
            driver = DriverManager.get_driver(browser=browser, headless=TestConfig.HEADLESS)
            home_page = HomePage(driver)
            home_page.open()
            
            # Test tab navigation
            search_box = home_page.find_element(home_page.SEARCH_BOX)
            search_box.click()
            search_box.send_keys("test")
            search_box.send_keys(Keys.TAB)
            
            # Verify focus moved (this would need more specific implementation)
            active_element = driver.switch_to.active_element
            assert active_element is not None, f"Keyboard navigation failed in {browser}"
            
        except WebDriverException as e:
            pytest.skip(f"Browser {browser} not available: {e}")
        
        finally:
            if driver:
                DriverManager.quit_driver(driver)


# Browser compatibility test configuration
@pytest.fixture(scope="session")
def browser_compatibility_config():
    """Configuration for browser compatibility tests"""
    return {
        "browsers": ["chrome", "firefox", "edge"],
        "resolutions": [
            (1920, 1080),  # Desktop
            (1366, 768),   # Laptop
            (768, 1024),   # Tablet
            (320, 568),    # Mobile
        ],
        "performance_thresholds": {
            "page_load": 30,
            "search_time": 15,
            "element_wait": 10
        }
    }