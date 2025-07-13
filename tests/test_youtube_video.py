import pytest
import time
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.video_page import VideoPage


@pytest.mark.youtube_video
@pytest.mark.smoke
class TestYouTubeVideo:
    
    def test_video_page_load(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("short video")
        
        if search_page.has_search_results():
            assert search_page.click_first_search_result(), "Failed to click first search result"
            assert video_page.wait_for_video_to_load(), "Video failed to load"
            assert "watch" in driver.current_url, "Not on video watch page"
    
    def test_video_title_and_metadata(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("technology")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            title = video_page.get_video_title()
            assert len(title) > 0, "Video title is empty"
            
            channel_name = video_page.get_channel_name()
            assert len(channel_name) > 0, "Channel name is empty"
            
            view_count = video_page.get_view_count()
    
    def test_video_play_pause(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("music")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            time.sleep(3)
            
            assert video_page.play_video(), "Failed to play video"
            time.sleep(2)
            
            assert video_page.pause_video(), "Failed to pause video"
    
    def test_video_controls_visibility(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("tutorial")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            video_player = video_page.find_element(video_page.VIDEO_PLAYER)
            assert video_player is not None, "Video player not found"
    
    def test_video_interaction_buttons(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("programming")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            like_button = video_page.find_element(video_page.LIKE_BUTTON)
            share_button = video_page.find_element(video_page.SHARE_BUTTON)
            
            assert like_button is not None or share_button is not None, "No interaction buttons found"
    
    def test_video_description_section(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("education")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            description = video_page.get_description()
    
    def test_related_videos_section(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("documentary")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            related_count = video_page.get_related_videos_count()
            assert related_count >= 0, "Related videos count is negative"
    
    def test_video_keyboard_controls(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("short clip")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            time.sleep(2)
            
            video_player = video_page.find_element(video_page.VIDEO_PLAYER)
            if video_player:
                video_player.click()
                time.sleep(1)
                
                assert video_page.skip_forward(), "Failed to skip forward"
                time.sleep(1)
                
                assert video_page.skip_backward(), "Failed to skip backward"
    
    @pytest.mark.regression
    def test_video_quality_and_settings(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("high quality")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            settings_button = video_page.find_element(video_page.SETTINGS_BUTTON)
    
    def test_video_share_functionality(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("viral video")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            assert video_page.click_share_button(), "Failed to click share button"
    
    def test_video_volume_control(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        video_page = VideoPage(driver)
        
        home_page.open()
        home_page.search_for_video("music video")
        
        if search_page.has_search_results():
            search_page.click_first_search_result()
            video_page.wait_for_video_to_load()
            
            time.sleep(2)
            
            assert video_page.set_volume(0.5), "Failed to set volume to 50%"
            time.sleep(1)
            
            assert video_page.mute_video(), "Failed to mute video"
            time.sleep(1)
            
            assert video_page.unmute_video(), "Failed to unmute video"