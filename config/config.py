import os
from dotenv import load_dotenv

load_dotenv()


class TestConfig:
    
    YOUTUBE_BASE_URL = "https://www.youtube.com"
    
    DEFAULT_TIMEOUT = 10
    
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    
    REPORTS_DIR = os.path.join(os.getcwd(), "reports")
    
    SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
    
    PARALLEL_TESTS = int(os.getenv("PARALLEL_TESTS", "1"))
    
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", "1"))
    
    @classmethod
    def ensure_directories_exist(cls):
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)
        os.makedirs(cls.SCREENSHOTS_DIR, exist_ok=True)