import pytest
from pages.home_page import HomePage
from config.config import TestConfig


@pytest.mark.youtube_navigation
@pytest.mark.smoke
class TestYouTubeNavigation:
    
    def test_homepage_load(self, driver):
        home_page = HomePage(driver)
        
        assert home_page.open(), "Failed to open YouTube homepage"
        assert TestConfig.YOUTUBE_BASE_URL in driver.current_url, "Not on YouTube homepage"
        assert home_page.is_youtube_logo_visible(), "YouTube logo not visible"
        assert "YouTube" in driver.title, "Page title doesn't contain YouTube"
    
    def test_navigation_elements_visibility(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        assert home_page.is_search_box_visible(), "Search box not visible"
        assert home_page.is_youtube_logo_visible(), "YouTube logo not visible"
    
    def test_youtube_logo_navigation(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        home_page.search_for_video("test search")
        
        search_url = driver.current_url
        assert "search" in search_url, "Not on search results page"
        
        assert home_page.click_youtube_logo(), "Failed to click YouTube logo"
        
        home_url = driver.current_url
        assert home_url != search_url, "URL didn't change after clicking logo"
        assert TestConfig.YOUTUBE_BASE_URL in home_url, "Not back to homepage"
    
    def test_search_functionality_navigation(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        original_url = driver.current_url
        search_term = "selenium testing"
        
        assert home_page.search_for_video(search_term), "Failed to perform search"
        
        new_url = driver.current_url
        assert new_url != original_url, "URL didn't change after search"
        assert "search_query" in new_url, "Search query not in URL"
        assert search_term.replace(" ", "+") in new_url, "Search term not in URL"
    
    def test_video_thumbnail_navigation(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        thumbnails = home_page.get_video_thumbnails()
        if len(thumbnails) > 0:
            original_url = driver.current_url
            
            assert home_page.click_first_video(), "Failed to click video thumbnail"
            
            new_url = driver.current_url
            assert new_url != original_url, "URL didn't change after clicking video"
            assert "watch" in new_url, "Not navigated to video watch page"
    
    def test_menu_button_functionality(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        assert home_page.click_menu_button(), "Failed to click menu button"
    
    def test_page_title_consistency(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        title = home_page.get_page_title()
        assert "YouTube" in title, f"Page title '{title}' doesn't contain YouTube"
        assert len(title) > 0, "Page title is empty"
    
    def test_page_responsiveness(self, driver):
        home_page = HomePage(driver)
        
        driver.set_window_size(1920, 1080)
        home_page.open()
        assert home_page.is_youtube_logo_visible(), "Logo not visible at 1920x1080"
        
        driver.set_window_size(1366, 768)
        home_page.refresh_page()
        assert home_page.is_youtube_logo_visible(), "Logo not visible at 1366x768"
        
        driver.set_window_size(1024, 768)
        home_page.refresh_page()
        assert home_page.is_youtube_logo_visible(), "Logo not visible at 1024x768"
    
    @pytest.mark.regression
    def test_navigation_breadcrumbs(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        home_page.search_for_video("automation testing")
        search_url = driver.current_url
        
        if home_page.get_video_thumbnails():
            home_page.click_first_video()
            video_url = driver.current_url
            
            driver.back()
            back_url = driver.current_url
            assert search_url in back_url, "Browser back didn't return to search results"
            
            driver.forward()
            forward_url = driver.current_url
            assert video_url in forward_url, "Browser forward didn't return to video page"
    
    def test_multiple_tab_navigation(self, driver):
        home_page = HomePage(driver)
        home_page.open()
        
        original_handles = driver.window_handles
        assert len(original_handles) == 1, "Expected only one window initially"
        
        driver.execute_script("window.open('https://www.youtube.com');")
        
        new_handles = driver.window_handles
        assert len(new_handles) == 2, "New tab not opened"
        
        driver.switch_to.window(new_handles[1])
        assert TestConfig.YOUTUBE_BASE_URL in driver.current_url, "New tab not on YouTube"
        
        driver.close()
        driver.switch_to.window(original_handles[0])
        assert TestConfig.YOUTUBE_BASE_URL in driver.current_url, "Original tab lost focus"
    
    def test_url_direct_access(self, driver):
        test_urls = [
            f"{TestConfig.YOUTUBE_BASE_URL}/",
            f"{TestConfig.YOUTUBE_BASE_URL}/feed/trending",
            f"{TestConfig.YOUTUBE_BASE_URL}/results?search_query=test"
        ]
        
        for url in test_urls:
            driver.get(url)
            assert TestConfig.YOUTUBE_BASE_URL in driver.current_url, f"Failed to navigate to {url}"
            assert "YouTube" in driver.title, f"Title doesn't contain YouTube for {url}"