from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import time


class VideoPage(BasePage):
    
    VIDEO_PLAYER = (By.CLASS_NAME, "video-stream")
    PLAY_BUTTON = (By.XPATH, "//button[@title='Play']")
    PAUSE_BUTTON = (By.XPATH, "//button[@title='Pause']")
    MUTE_BUTTON = (By.XPATH, "//button[@title='Mute']")
    UNMUTE_BUTTON = (By.XPATH, "//button[@title='Unmute']")
    VOLUME_SLIDER = (By.XPATH, "//input[@aria-label='Volume']")
    PROGRESS_BAR = (By.CLASS_NAME, "ytp-progress-bar")
    FULLSCREEN_BUTTON = (By.XPATH, "//button[@title='Full screen']")
    SETTINGS_BUTTON = (By.XPATH, "//button[@title='Settings']")
    VIDEO_TITLE = (By.XPATH, "//h1[@class='title style-scope ytd-video-primary-info-renderer']")
    CHANNEL_NAME = (By.XPATH, "//a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
    LIKE_BUTTON = (By.XPATH, "//button[@aria-label='Like this video']")
    DISLIKE_BUTTON = (By.XPATH, "//button[@aria-label='Dislike this video']")
    SUBSCRIBE_BUTTON = (By.XPATH, "//button[contains(@aria-label, 'Subscribe')]")
    SHARE_BUTTON = (By.XPATH, "//button[@aria-label='Share']")
    DOWNLOAD_BUTTON = (By.XPATH, "//button[@aria-label='Download']")
    DESCRIPTION_TEXT = (By.XPATH, "//div[@id='description']")
    VIEW_COUNT = (By.XPATH, "//span[@class='view-count style-scope ytd-video-view-count-renderer']")
    UPLOAD_DATE = (By.XPATH, "//div[@id='info-strings']")
    COMMENTS_SECTION = (By.XPATH, "//div[@id='comments']")
    COMMENT_INPUT = (By.XPATH, "//div[@id='placeholder-area']")
    RELATED_VIDEOS = (By.XPATH, "//div[@id='secondary']//a[@id='thumbnail']")
    QUALITY_MENU = (By.XPATH, "//div[@class='ytp-quality-menu']")
    SPEED_BUTTON = (By.XPATH, "//button[@title='Playback speed']")
    CAPTIONS_BUTTON = (By.XPATH, "//button[@title='Subtitles/closed captions']")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def play_video(self) -> bool:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            video_player.click()
            return True
        return self.click_element(self.PLAY_BUTTON)
    
    def pause_video(self) -> bool:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            video_player.click()
            return True
        return self.click_element(self.PAUSE_BUTTON)
    
    def mute_video(self) -> bool:
        return self.click_element(self.MUTE_BUTTON)
    
    def unmute_video(self) -> bool:
        return self.click_element(self.UNMUTE_BUTTON)
    
    def toggle_fullscreen(self) -> bool:
        return self.click_element(self.FULLSCREEN_BUTTON)
    
    def click_settings(self) -> bool:
        return self.click_element(self.SETTINGS_BUTTON)
    
    def get_video_title(self) -> str:
        return self.get_element_text(self.VIDEO_TITLE)
    
    def get_channel_name(self) -> str:
        return self.get_element_text(self.CHANNEL_NAME)
    
    def get_view_count(self) -> str:
        return self.get_element_text(self.VIEW_COUNT)
    
    def get_description(self) -> str:
        return self.get_element_text(self.DESCRIPTION_TEXT)
    
    def click_like_button(self) -> bool:
        return self.click_element(self.LIKE_BUTTON)
    
    def click_dislike_button(self) -> bool:
        return self.click_element(self.DISLIKE_BUTTON)
    
    def click_subscribe_button(self) -> bool:
        return self.click_element(self.SUBSCRIBE_BUTTON)
    
    def click_share_button(self) -> bool:
        return self.click_element(self.SHARE_BUTTON)
    
    def click_download_button(self) -> bool:
        return self.click_element(self.DOWNLOAD_BUTTON)
    
    def is_video_playing(self) -> bool:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            return not video_player.get_attribute("paused")
        return False
    
    def is_video_paused(self) -> bool:
        return not self.is_video_playing()
    
    def get_video_duration(self) -> str:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            return video_player.get_attribute("duration")
        return ""
    
    def get_current_time(self) -> str:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            return video_player.get_attribute("currentTime")
        return ""
    
    def seek_to_time(self, seconds: int) -> bool:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            self.driver.execute_script(f"arguments[0].currentTime = {seconds};", video_player)
            return True
        return False
    
    def set_volume(self, volume: float) -> bool:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player and 0.0 <= volume <= 1.0:
            self.driver.execute_script(f"arguments[0].volume = {volume};", video_player)
            return True
        return False
    
    def skip_forward(self, seconds: int = 10) -> bool:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            video_player.send_keys(Keys.ARROW_RIGHT)
            return True
        return False
    
    def skip_backward(self, seconds: int = 10) -> bool:
        video_player = self.find_element(self.VIDEO_PLAYER)
        if video_player:
            video_player.send_keys(Keys.ARROW_LEFT)
            return True
        return False
    
    def toggle_captions(self) -> bool:
        return self.click_element(self.CAPTIONS_BUTTON)
    
    def change_playback_speed(self) -> bool:
        return self.click_element(self.SPEED_BUTTON)
    
    def get_related_videos_count(self) -> int:
        related_videos = self.find_elements(self.RELATED_VIDEOS)
        return len(related_videos)
    
    def click_related_video(self, index: int = 0) -> bool:
        related_videos = self.find_elements(self.RELATED_VIDEOS)
        if 0 <= index < len(related_videos):
            related_videos[index].click()
            return True
        return False
    
    def scroll_to_comments(self) -> bool:
        return self.scroll_to_element(self.COMMENTS_SECTION)
    
    def is_comments_section_visible(self) -> bool:
        return self.is_element_visible(self.COMMENTS_SECTION)
    
    def wait_for_video_to_load(self, timeout: int = 15) -> bool:
        for _ in range(timeout):
            if self.is_element_visible(self.VIDEO_PLAYER):
                return True
            time.sleep(1)
        return False