import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class TestDataProvider:
    """Centralized test data provider for YouTube automation tests"""
    
    def __init__(self, data_file: str = "test_data.json"):
        self.data_file = os.path.join("config", data_file)
        self._data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load test data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Return default test data if file doesn't exist"""
        return {
            "search_terms": {
                "valid": [
                    "Python programming",
                    "Selenium automation",
                    "Web development tutorial",
                    "Machine learning basics",
                    "JavaScript frameworks"
                ],
                "invalid": ["", "   ", "xyzxyzxyznonexistent"],
                "special_characters": ["C++ programming", "React.js", "API testing @2023"]
            },
            "video_categories": [
                "Education", "Technology", "Music", "Entertainment",
                "News", "Sports", "Gaming", "Science"
            ],
            "browser_resolutions": [
                {"width": 1920, "height": 1080, "name": "Full HD"},
                {"width": 1366, "height": 768, "name": "Laptop"},
                {"width": 1024, "height": 768, "name": "Tablet"}
            ],
            "youtube_urls": {
                "base": "https://www.youtube.com",
                "trending": "https://www.youtube.com/feed/trending",
                "search_base": "https://www.youtube.com/results?search_query="
            }
        }
    
    def get_search_terms(self, category: str = "valid") -> List[str]:
        """Get search terms by category"""
        return self._data.get("search_terms", {}).get(category, [])
    
    def get_valid_search_terms(self) -> List[str]:
        """Get valid search terms for positive testing"""
        return self.get_search_terms("valid")
    
    def get_invalid_search_terms(self) -> List[str]:
        """Get invalid search terms for negative testing"""
        return self.get_search_terms("invalid")
    
    def get_special_character_terms(self) -> List[str]:
        """Get search terms with special characters"""
        return self.get_search_terms("special_characters")
    
    def get_video_categories(self) -> List[str]:
        """Get list of video categories"""
        return self._data.get("video_categories", [])
    
    def get_browser_resolutions(self) -> List[Dict[str, Any]]:
        """Get browser resolution configurations"""
        return self._data.get("browser_resolutions", [])
    
    def get_youtube_urls(self) -> Dict[str, str]:
        """Get YouTube URL configurations"""
        return self._data.get("youtube_urls", {})
    
    def get_expected_elements(self, page: str) -> List[str]:
        """Get expected elements for a specific page"""
        return self._data.get("expected_elements", {}).get(page, [])
    
    def get_test_timeouts(self) -> Dict[str, int]:
        """Get timeout configurations"""
        return self._data.get("test_timeouts", {
            "element_wait": 10,
            "page_load": 30,
            "video_load": 15,
            "search_results": 10
        })
    
    def get_random_search_term(self, category: str = "valid") -> str:
        """Get a random search term from the specified category"""
        import random
        terms = self.get_search_terms(category)
        return random.choice(terms) if terms else ""
    
    def update_data(self, key: str, value: Any) -> None:
        """Update test data dynamically"""
        self._data[key] = value
        self._save_data()
    
    def _save_data(self) -> None:
        """Save current data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as file:
            json.dump(self._data, file, indent=2)


class TestDataGenerator:
    """Generate test data dynamically"""
    
    @staticmethod
    def generate_search_terms(count: int = 10) -> List[str]:
        """Generate search terms for testing"""
        base_terms = [
            "programming", "tutorial", "technology", "music", "news",
            "education", "science", "entertainment", "sports", "gaming"
        ]
        
        prefixes = ["how to", "best", "top 10", "learn", "understand"]
        suffixes = ["2023", "guide", "tips", "basics", "advanced"]
        
        import random
        generated_terms = []
        
        for _ in range(count):
            if random.choice([True, False]):
                term = f"{random.choice(prefixes)} {random.choice(base_terms)}"
            else:
                term = f"{random.choice(base_terms)} {random.choice(suffixes)}"
            
            generated_terms.append(term)
        
        return generated_terms
    
    @staticmethod
    def generate_invalid_inputs() -> List[str]:
        """Generate invalid input data for negative testing"""
        return [
            "",  # Empty string
            " " * 10,  # Only spaces
            "x" * 1000,  # Very long string
            "!@#$%^&*()",  # Special characters only
            "\n\t\r",  # Whitespace characters
            "SELECT * FROM users",  # SQL injection attempt
            "<script>alert('xss')</script>",  # XSS attempt
        ]
    
    @staticmethod
    def generate_performance_test_data() -> Dict[str, Any]:
        """Generate data for performance testing"""
        return {
            "load_test_terms": [
                f"performance test {i}" for i in range(100)
            ],
            "concurrent_searches": [
                f"concurrent search {i}" for i in range(50)
            ],
            "stress_test_data": {
                "search_volume": 1000,
                "concurrent_users": 10,
                "duration_minutes": 5
            }
        }


class TestDataValidator:
    """Validate test data integrity"""
    
    @staticmethod
    def validate_search_terms(terms: List[str]) -> Dict[str, List[str]]:
        """Validate search terms and categorize them"""
        validation_results = {
            "valid": [],
            "invalid": [],
            "warnings": []
        }
        
        for term in terms:
            if not term or not term.strip():
                validation_results["invalid"].append(term)
            elif len(term) > 200:
                validation_results["warnings"].append(f"Long term: {term}")
                validation_results["valid"].append(term)
            else:
                validation_results["valid"].append(term)
        
        return validation_results
    
    @staticmethod
    def validate_urls(urls: Dict[str, str]) -> Dict[str, bool]:
        """Validate URL configurations"""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        validation_results = {}
        for key, url in urls.items():
            validation_results[key] = bool(url_pattern.match(url))
        
        return validation_results
    
    @staticmethod
    def validate_test_data_file(filepath: str) -> Dict[str, Any]:
        """Validate entire test data file"""
        validation_report = {
            "file_exists": os.path.exists(filepath),
            "file_size": 0,
            "json_valid": False,
            "required_sections": {},
            "recommendations": []
        }
        
        if not validation_report["file_exists"]:
            validation_report["recommendations"].append("Create test data file")
            return validation_report
        
        validation_report["file_size"] = os.path.getsize(filepath)
        
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                validation_report["json_valid"] = True
                
                # Check required sections
                required_sections = [
                    "search_terms", "video_categories", 
                    "browser_resolutions", "youtube_urls"
                ]
                
                for section in required_sections:
                    validation_report["required_sections"][section] = section in data
                    if section not in data:
                        validation_report["recommendations"].append(
                            f"Add {section} section to test data"
                        )
                
        except json.JSONDecodeError:
            validation_report["json_valid"] = False
            validation_report["recommendations"].append("Fix JSON syntax errors")
        except Exception as e:
            validation_report["recommendations"].append(f"File access error: {e}")
        
        return validation_report


class DynamicTestData:
    """Generate dynamic test data based on current context"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_timestamped_search_term(self, base_term: str) -> str:
        """Get search term with timestamp for uniqueness"""
        return f"{base_term} {self.timestamp}"
    
    def get_context_specific_data(self, context: str) -> Dict[str, Any]:
        """Get data specific to test context"""
        context_data = {
            "smoke_test": {
                "search_terms": ["quick test", "smoke test"],
                "timeout_multiplier": 0.5,
                "max_results": 5
            },
            "regression_test": {
                "search_terms": self._get_comprehensive_search_terms(),
                "timeout_multiplier": 1.0,
                "max_results": 20
            },
            "performance_test": {
                "search_terms": [f"perf test {i}" for i in range(100)],
                "timeout_multiplier": 2.0,
                "max_results": 50
            }
        }
        
        return context_data.get(context, context_data["smoke_test"])
    
    def _get_comprehensive_search_terms(self) -> List[str]:
        """Get comprehensive list of search terms for regression testing"""
        return [
            "programming tutorial",
            "machine learning",
            "web development",
            "data science",
            "artificial intelligence",
            "cloud computing",
            "cybersecurity",
            "mobile development",
            "game development",
            "software engineering"
        ]
    
    def get_browser_specific_data(self, browser: str) -> Dict[str, Any]:
        """Get browser-specific test data"""
        browser_data = {
            "chrome": {
                "user_agent_check": "Chrome",
                "specific_features": ["webgl", "audio"],
                "performance_baseline": 1.0
            },
            "firefox": {
                "user_agent_check": "Firefox",
                "specific_features": ["webgl", "audio"],
                "performance_baseline": 1.1
            },
            "edge": {
                "user_agent_check": "Edge",
                "specific_features": ["webgl", "audio"],
                "performance_baseline": 1.05
            }
        }
        
        return browser_data.get(browser, browser_data["chrome"])