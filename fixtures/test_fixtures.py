import pytest
import json
import os
from typing import Dict, List, Any
from datetime import datetime
from config.config import TestConfig
from config.test_data import TestDataProvider
from utils.test_helpers import TestDataHelpers, ValidationHelpers


class TestDataFixtures:
    """Central class for managing test data fixtures"""
    
    @staticmethod
    def load_test_data(filename: str) -> Dict[str, Any]:
        """Load test data from JSON file"""
        data_path = os.path.join("config", filename)
        if os.path.exists(data_path):
            with open(data_path, 'r') as file:
                return json.load(file)
        return {}
    
    @staticmethod
    def save_test_results(test_name: str, results: Dict[str, Any]) -> None:
        """Save test results for analysis"""
        results_dir = os.path.join(TestConfig.REPORTS_DIR, "test_results")
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.json"
        filepath = os.path.join(results_dir, filename)
        
        with open(filepath, 'w') as file:
            json.dump(results, file, indent=2)


@pytest.fixture(scope="session")
def test_data_provider():
    """Provide test data throughout the test session"""
    return TestDataProvider()


@pytest.fixture(scope="session")
def youtube_test_data():
    """Load YouTube-specific test data"""
    return TestDataFixtures.load_test_data("test_data.json")


@pytest.fixture(scope="function")
def search_terms(youtube_test_data):
    """Provide search terms for testing"""
    return youtube_test_data.get("search_terms", {})


@pytest.fixture(scope="function")
def valid_search_terms(search_terms):
    """Provide valid search terms"""
    return search_terms.get("valid", TestDataHelpers.get_search_terms())


@pytest.fixture(scope="function")
def invalid_search_terms(search_terms):
    """Provide invalid search terms for negative testing"""
    return search_terms.get("invalid", TestDataHelpers.get_invalid_search_terms())


@pytest.fixture(scope="function")
def special_character_search_terms(search_terms):
    """Provide search terms with special characters"""
    return search_terms.get("special_characters", [
        "C++ programming",
        "React.js tutorial",
        "API testing @2023",
        "music #trending"
    ])


@pytest.fixture(scope="function")
def browser_resolutions(youtube_test_data):
    """Provide browser resolutions for responsive testing"""
    resolutions = youtube_test_data.get("browser_resolutions", [])
    if not resolutions:
        return TestDataHelpers.get_browser_resolutions()
    return [(res["width"], res["height"]) for res in resolutions]


@pytest.fixture(scope="function")
def test_timeouts(youtube_test_data):
    """Provide test timeout configurations"""
    return youtube_test_data.get("test_timeouts", TestDataHelpers.get_test_timeouts())


@pytest.fixture(scope="function")
def youtube_urls(youtube_test_data):
    """Provide YouTube URL configurations"""
    return youtube_test_data.get("youtube_urls", {
        "base": "https://www.youtube.com",
        "trending": "https://www.youtube.com/feed/trending",
        "search_base": "https://www.youtube.com/results?search_query="
    })


@pytest.fixture(scope="function")
def video_categories(youtube_test_data):
    """Provide video categories for testing"""
    return youtube_test_data.get("video_categories", [
        "Education", "Technology", "Music", "Entertainment",
        "News", "Sports", "Gaming", "Science"
    ])


@pytest.fixture(scope="function")
def expected_elements(youtube_test_data):
    """Provide expected page elements for validation"""
    return youtube_test_data.get("expected_elements", {})


@pytest.fixture(scope="function")
def test_user_data():
    """Provide test user data (anonymized)"""
    return {
        "test_user": {
            "username": "test_user_selenium",
            "preferences": {
                "language": "en",
                "region": "US",
                "autoplay": False
            }
        }
    }


@pytest.fixture(scope="function")
def performance_thresholds():
    """Provide performance testing thresholds"""
    return {
        "page_load_time": 10.0,  # seconds
        "search_response_time": 5.0,  # seconds
        "video_load_time": 15.0,  # seconds
        "element_load_time": 3.0,  # seconds
    }


@pytest.fixture(scope="function")
def test_metadata():
    """Provide metadata for the current test"""
    return {
        "execution_time": datetime.now().isoformat(),
        "browser": TestConfig.BROWSER,
        "headless": TestConfig.HEADLESS,
        "environment": os.getenv("TEST_ENVIRONMENT", "local"),
        "parallel": TestConfig.PARALLEL_TESTS > 1
    }


@pytest.fixture(scope="function")
def screenshot_config():
    """Provide screenshot configuration"""
    return {
        "on_failure": TestConfig.SCREENSHOT_ON_FAILURE,
        "directory": TestConfig.SCREENSHOTS_DIR,
        "format": "png",
        "quality": "high"
    }


@pytest.fixture(scope="function")
def validation_helpers():
    """Provide validation helper methods"""
    return ValidationHelpers


@pytest.fixture(scope="function")
def test_result_collector():
    """Collect test results for reporting"""
    results = {
        "test_name": "",
        "status": "unknown",
        "duration": 0.0,
        "screenshots": [],
        "errors": [],
        "assertions": []
    }
    
    class ResultCollector:
        def __init__(self):
            self.results = results
        
        def set_test_name(self, name: str):
            self.results["test_name"] = name
        
        def set_status(self, status: str):
            self.results["status"] = status
        
        def set_duration(self, duration: float):
            self.results["duration"] = duration
        
        def add_screenshot(self, path: str):
            self.results["screenshots"].append(path)
        
        def add_error(self, error: str):
            self.results["errors"].append(error)
        
        def add_assertion(self, assertion: Dict[str, Any]):
            self.results["assertions"].append(assertion)
        
        def get_results(self) -> Dict[str, Any]:
            return self.results.copy()
    
    return ResultCollector()


# Data-driven test fixtures
@pytest.fixture(params=[
    "Python programming",
    "Selenium automation", 
    "Web development",
    "Machine learning"
])
def parametrized_search_term(request):
    """Parametrized fixture for search terms"""
    return request.param


@pytest.fixture(params=["chrome", "firefox"])
def parametrized_browser(request):
    """Parametrized fixture for browsers"""
    return request.param


@pytest.fixture(params=[
    (1920, 1080),
    (1366, 768),
    (1024, 768)
])
def parametrized_resolution(request):
    """Parametrized fixture for screen resolutions"""
    return request.param


# Environment-specific fixtures
@pytest.fixture(scope="session")
def environment_config():
    """Provide environment-specific configuration"""
    env = os.getenv("TEST_ENVIRONMENT", "local")
    
    configs = {
        "local": {
            "base_url": "https://www.youtube.com",
            "timeout_multiplier": 1.0,
            "retry_count": 2
        },
        "ci": {
            "base_url": "https://www.youtube.com",
            "timeout_multiplier": 2.0,
            "retry_count": 3
        },
        "staging": {
            "base_url": "https://www.youtube.com",
            "timeout_multiplier": 1.5,
            "retry_count": 3
        }
    }
    
    return configs.get(env, configs["local"])


# Cleanup fixtures
@pytest.fixture(scope="function", autouse=True)
def test_cleanup():
    """Automatic cleanup after each test"""
    yield
    
    # Cleanup temporary files, clear cache, etc.
    # This runs after each test automatically


@pytest.fixture(scope="session", autouse=True)
def session_cleanup():
    """Automatic cleanup after test session"""
    yield
    
    # Session-level cleanup
    print("\nCleaning up test session...")
    
    # Clean old screenshots if configured
    from utils.screenshot_utils import ScreenshotUtils
    try:
        ScreenshotUtils.clean_old_screenshots(days_old=7)
    except Exception as e:
        print(f"Warning: Could not clean old screenshots: {e}")


# Custom fixture for test reporting integration
@pytest.fixture(scope="function")
def test_report_data(request, test_metadata):
    """Collect data for test reporting"""
    test_data = {
        "test_name": request.node.name,
        "test_file": request.node.fspath.basename,
        "test_class": request.node.cls.__name__ if request.node.cls else None,
        "markers": [marker.name for marker in request.node.iter_markers()],
        "metadata": test_metadata,
        "start_time": datetime.now(),
        "end_time": None,
        "duration": None,
        "status": "running"
    }
    
    yield test_data
    
    # Update end time and duration
    test_data["end_time"] = datetime.now()
    test_data["duration"] = (test_data["end_time"] - test_data["start_time"]).total_seconds()
    
    # Save test report data
    try:
        TestDataFixtures.save_test_results(
            test_data["test_name"], 
            test_data
        )
    except Exception as e:
        print(f"Warning: Could not save test report data: {e}")