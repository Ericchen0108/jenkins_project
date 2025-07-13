from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage


class SearchPage(BasePage):
    
    SEARCH_RESULTS = (By.XPATH, "//div[@id='contents']//div[@id='dismissible']")
    SEARCH_RESULT_TITLES = (By.XPATH, "//div[@id='contents']//a[@id='video-title']")
    SEARCH_RESULT_THUMBNAILS = (By.XPATH, "//div[@id='contents']//a[@id='thumbnail']")
    SEARCH_RESULT_DESCRIPTIONS = (By.XPATH, "//div[@id='contents']//span[@id='description-text']")
    CHANNEL_NAMES = (By.XPATH, "//div[@id='contents']//a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
    VIEW_COUNTS = (By.XPATH, "//div[@id='contents']//span[contains(@class, 'style-scope ytd-video-meta-block')]")
    FILTER_BUTTON = (By.XPATH, "//button[@aria-label='Search filters']")
    SORT_BUTTON = (By.XPATH, "//button[@aria-label='Sort by']")
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(text(), 'No results found')]")
    SEARCH_BOX = (By.NAME, "search_query")
    SEARCH_SUGGESTIONS = (By.XPATH, "//ul[@role='listbox']//li")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def get_search_results_count(self) -> int:
        results = self.find_elements(self.SEARCH_RESULTS)
        return len(results)
    
    def get_search_result_titles(self) -> list:
        elements = self.find_elements(self.SEARCH_RESULT_TITLES)
        return [element.get_attribute("title") for element in elements if element.get_attribute("title")]
    
    def get_search_result_descriptions(self) -> list:
        elements = self.find_elements(self.SEARCH_RESULT_DESCRIPTIONS)
        return [element.text for element in elements if element.text]
    
    def get_channel_names(self) -> list:
        elements = self.find_elements(self.CHANNEL_NAMES)
        return [element.text for element in elements if element.text]
    
    def get_view_counts(self) -> list:
        elements = self.find_elements(self.VIEW_COUNTS)
        return [element.text for element in elements if element.text and "views" in element.text.lower()]
    
    def click_first_search_result(self) -> bool:
        thumbnails = self.find_elements(self.SEARCH_RESULT_THUMBNAILS)
        if thumbnails:
            thumbnails[0].click()
            return True
        return False
    
    def click_search_result_by_index(self, index: int) -> bool:
        thumbnails = self.find_elements(self.SEARCH_RESULT_THUMBNAILS)
        if 0 <= index < len(thumbnails):
            thumbnails[index].click()
            return True
        return False
    
    def click_filter_button(self) -> bool:
        return self.click_element(self.FILTER_BUTTON)
    
    def click_sort_button(self) -> bool:
        return self.click_element(self.SORT_BUTTON)
    
    def is_no_results_message_displayed(self) -> bool:
        return self.is_element_visible(self.NO_RESULTS_MESSAGE)
    
    def has_search_results(self) -> bool:
        return self.get_search_results_count() > 0
    
    def search_for_new_term(self, search_term: str) -> bool:
        search_box = self.find_element(self.SEARCH_BOX)
        if search_box:
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.submit()
            return True
        return False
    
    def get_search_suggestions(self) -> list:
        elements = self.find_elements(self.SEARCH_SUGGESTIONS)
        return [element.text for element in elements if element.text]
    
    def click_search_suggestion(self, suggestion_text: str) -> bool:
        suggestions = self.find_elements(self.SEARCH_SUGGESTIONS)
        for suggestion in suggestions:
            if suggestion_text.lower() in suggestion.text.lower():
                suggestion.click()
                return True
        return False
    
    def scroll_to_load_more_results(self) -> None:
        self.scroll_to_bottom()
        self.wait_for_page_load()
    
    def verify_search_term_in_results(self, search_term: str) -> bool:
        titles = self.get_search_result_titles()
        descriptions = self.get_search_result_descriptions()
        
        search_term_lower = search_term.lower()
        
        for title in titles:
            if search_term_lower in title.lower():
                return True
        
        for description in descriptions:
            if search_term_lower in description.lower():
                return True
        
        return False