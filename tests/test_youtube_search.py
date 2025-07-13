import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from config.config import TestConfig


@pytest.mark.youtube_search
@pytest.mark.smoke
class TestYouTubeSearch:
    
    def test_search_basic_functionality(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        assert home_page.open(), "Failed to open YouTube homepage"
        assert home_page.is_youtube_logo_visible(), "YouTube logo not visible"
        assert home_page.is_search_box_visible(), "Search box not visible"
        
        search_term = "Python programming"
        assert home_page.search_for_video(search_term), "Failed to perform search"
        
        assert search_page.has_search_results(), "No search results found"
        assert search_page.get_search_results_count() > 0, "Search results count is 0"
        
        titles = search_page.get_search_result_titles()
        assert len(titles) > 0, "No video titles found in search results"
        
        assert search_page.verify_search_term_in_results(search_term), f"Search term '{search_term}' not found in results"
    
    def test_search_with_multiple_keywords(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        home_page.open()
        
        search_terms = ["selenium automation", "machine learning", "web development"]
        
        for search_term in search_terms:
            home_page.search_for_video(search_term)
            
            assert search_page.has_search_results(), f"No results for '{search_term}'"
            results_count = search_page.get_search_results_count()
            assert results_count > 0, f"No results count for '{search_term}'"
            
            titles = search_page.get_search_result_titles()
            assert len(titles) > 0, f"No titles found for '{search_term}'"
    
    def test_search_results_content(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        home_page.open()
        home_page.search_for_video("technology news")
        
        titles = search_page.get_search_result_titles()
        descriptions = search_page.get_search_result_descriptions()
        channels = search_page.get_channel_names()
        view_counts = search_page.get_view_counts()
        
        assert len(titles) > 0, "No video titles found"
        assert len(channels) > 0, "No channel names found"
        
        for title in titles[:5]:
            assert len(title) > 0, "Empty video title found"
        
        for channel in channels[:5]:
            assert len(channel) > 0, "Empty channel name found"
    
    def test_search_result_navigation(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        home_page.open()
        home_page.search_for_video("tutorial")
        
        assert search_page.has_search_results(), "No search results to navigate"
        
        original_url = driver.current_url
        assert search_page.click_first_search_result(), "Failed to click first search result"
        
        new_url = driver.current_url
        assert new_url != original_url, "URL did not change after clicking search result"
        assert "watch" in new_url, "Not navigated to video watch page"
    
    def test_empty_search(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        home_page.open()
        home_page.search_for_video("")
        
        current_url = driver.current_url
        assert TestConfig.YOUTUBE_BASE_URL in current_url, "Page navigated unexpectedly for empty search"
    
    def test_special_characters_search(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        home_page.open()
        
        special_searches = [
            "C++ programming",
            "React.js tutorial",
            "API testing @2023",
            "music #trending"
        ]
        
        for search_term in special_searches:
            home_page.search_for_video(search_term)
            
            results_count = search_page.get_search_results_count()
            assert results_count >= 0, f"Unexpected error for search: '{search_term}'"
    
    @pytest.mark.regression
    def test_search_filters_accessibility(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        home_page.open()
        home_page.search_for_video("music")
        
        assert search_page.click_filter_button(), "Filter button not clickable"
    
    def test_search_pagination_scroll(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        
        home_page.open()
        home_page.search_for_video("programming")
        
        initial_results_count = search_page.get_search_results_count()
        assert initial_results_count > 0, "No initial search results"
        
        search_page.scroll_to_load_more_results()
        
        final_results_count = search_page.get_search_results_count()
        assert final_results_count >= initial_results_count, "Results count decreased after scrolling"