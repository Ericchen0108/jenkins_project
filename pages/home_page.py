from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage


class HomePage(BasePage):
    
    SEARCH_BOX = (By.NAME, "search_query")
    SEARCH_BUTTON = (By.ID, "search-icon-legacy")
    YOUTUBE_LOGO = (By.ID, "logo")
    TRENDING_LINK = (By.XPATH, "//a[@title='Trending']")
    SUBSCRIPTIONS_LINK = (By.XPATH, "//a[@title='Subscriptions']")
    LIBRARY_LINK = (By.XPATH, "//a[@title='Library']")
    HISTORY_LINK = (By.XPATH, "//a[@title='History']")
    MENU_BUTTON = (By.XPATH, "//button[@aria-label='Guide']")
    VOICE_SEARCH_BUTTON = (By.ID, "voice-search-button")
    VIDEO_THUMBNAILS = (By.XPATH, "//div[@id='dismissible']//a[@id='thumbnail']")
    VIDEO_TITLES = (By.XPATH, "//div[@id='dismissible']//a[@id='video-title']")
    CHANNEL_NAMES = (By.XPATH, "//div[@id='dismissible']//a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = "https://www.youtube.com"
    
    def open(self):
        self.navigate_to(self.url)
        return self.wait_for_page_load()
    
    def search_for_video(self, search_term: str) -> bool:
        if self.send_keys_to_element(self.SEARCH_BOX, search_term):
            return self.click_element(self.SEARCH_BUTTON)
        return False
    
    def click_voice_search(self) -> bool:
        return self.click_element(self.VOICE_SEARCH_BUTTON)
    
    def click_youtube_logo(self) -> bool:
        return self.click_element(self.YOUTUBE_LOGO)
    
    def click_trending(self) -> bool:
        return self.click_element(self.TRENDING_LINK)
    
    def click_subscriptions(self) -> bool:
        return self.click_element(self.SUBSCRIPTIONS_LINK)
    
    def click_library(self) -> bool:
        return self.click_element(self.LIBRARY_LINK)
    
    def click_history(self) -> bool:
        return self.click_element(self.HISTORY_LINK)
    
    def click_menu_button(self) -> bool:
        return self.click_element(self.MENU_BUTTON)
    
    def get_video_thumbnails(self) -> list:
        return self.find_elements(self.VIDEO_THUMBNAILS)
    
    def get_video_titles(self) -> list:
        elements = self.find_elements(self.VIDEO_TITLES)
        return [element.get_attribute("title") for element in elements if element.get_attribute("title")]
    
    def get_channel_names(self) -> list:
        elements = self.find_elements(self.CHANNEL_NAMES)
        return [element.text for element in elements if element.text]
    
    def click_first_video(self) -> bool:
        videos = self.get_video_thumbnails()
        if videos:
            videos[0].click()
            return True
        return False
    
    def is_youtube_logo_visible(self) -> bool:
        return self.is_element_visible(self.YOUTUBE_LOGO)
    
    def is_search_box_visible(self) -> bool:
        return self.is_element_visible(self.SEARCH_BOX)