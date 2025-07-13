import os
from enum import Enum


class Environment(Enum):
    LOCAL = "local"
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"
    CI = "ci"


class EnvironmentConfig:
    
    def __init__(self, env_name: str = None):
        self.env_name = env_name or os.getenv("TEST_ENVIRONMENT", "local")
        self.environment = Environment(self.env_name.lower())
    
    @property
    def base_url(self) -> str:
        urls = {
            Environment.LOCAL: "https://www.youtube.com",
            Environment.DEV: "https://www.youtube.com",
            Environment.STAGING: "https://www.youtube.com",
            Environment.PROD: "https://www.youtube.com",
            Environment.CI: "https://www.youtube.com"
        }
        return urls.get(self.environment, "https://www.youtube.com")
    
    @property
    def timeout_config(self) -> dict:
        timeouts = {
            Environment.LOCAL: {
                "element_wait": 10,
                "page_load": 30,
                "video_load": 15,
                "implicit_wait": 10
            },
            Environment.DEV: {
                "element_wait": 15,
                "page_load": 45,
                "video_load": 20,
                "implicit_wait": 15
            },
            Environment.STAGING: {
                "element_wait": 15,
                "page_load": 45,
                "video_load": 20,
                "implicit_wait": 15
            },
            Environment.PROD: {
                "element_wait": 20,
                "page_load": 60,
                "video_load": 25,
                "implicit_wait": 20
            },
            Environment.CI: {
                "element_wait": 20,
                "page_load": 60,
                "video_load": 30,
                "implicit_wait": 20
            }
        }
        return timeouts.get(self.environment, timeouts[Environment.LOCAL])
    
    @property
    def browser_config(self) -> dict:
        configs = {
            Environment.LOCAL: {
                "headless": False,
                "window_size": (1920, 1080),
                "browser": "chrome"
            },
            Environment.DEV: {
                "headless": False,
                "window_size": (1920, 1080),
                "browser": "chrome"
            },
            Environment.STAGING: {
                "headless": True,
                "window_size": (1920, 1080),
                "browser": "chrome"
            },
            Environment.PROD: {
                "headless": True,
                "window_size": (1920, 1080),
                "browser": "chrome"
            },
            Environment.CI: {
                "headless": True,
                "window_size": (1920, 1080),
                "browser": "chrome"
            }
        }
        return configs.get(self.environment, configs[Environment.LOCAL])
    
    @property
    def retry_config(self) -> dict:
        retries = {
            Environment.LOCAL: {
                "max_attempts": 2,
                "delay": 1
            },
            Environment.DEV: {
                "max_attempts": 2,
                "delay": 1
            },
            Environment.STAGING: {
                "max_attempts": 3,
                "delay": 2
            },
            Environment.PROD: {
                "max_attempts": 3,
                "delay": 2
            },
            Environment.CI: {
                "max_attempts": 3,
                "delay": 3
            }
        }
        return retries.get(self.environment, retries[Environment.LOCAL])
    
    @property
    def parallel_config(self) -> dict:
        parallel = {
            Environment.LOCAL: {
                "enabled": False,
                "workers": 1
            },
            Environment.DEV: {
                "enabled": True,
                "workers": 2
            },
            Environment.STAGING: {
                "enabled": True,
                "workers": 4
            },
            Environment.PROD: {
                "enabled": True,
                "workers": 4
            },
            Environment.CI: {
                "enabled": True,
                "workers": 4
            }
        }
        return parallel.get(self.environment, parallel[Environment.LOCAL])
    
    @property
    def reporting_config(self) -> dict:
        reporting = {
            Environment.LOCAL: {
                "screenshot_on_failure": True,
                "video_recording": False,
                "html_report": True,
                "allure_report": False
            },
            Environment.DEV: {
                "screenshot_on_failure": True,
                "video_recording": False,
                "html_report": True,
                "allure_report": True
            },
            Environment.STAGING: {
                "screenshot_on_failure": True,
                "video_recording": True,
                "html_report": True,
                "allure_report": True
            },
            Environment.PROD: {
                "screenshot_on_failure": True,
                "video_recording": True,
                "html_report": True,
                "allure_report": True
            },
            Environment.CI: {
                "screenshot_on_failure": True,
                "video_recording": False,
                "html_report": True,
                "allure_report": True
            }
        }
        return reporting.get(self.environment, reporting[Environment.LOCAL])
    
    def get_all_configs(self) -> dict:
        return {
            "environment": self.env_name,
            "base_url": self.base_url,
            "timeouts": self.timeout_config,
            "browser": self.browser_config,
            "retry": self.retry_config,
            "parallel": self.parallel_config,
            "reporting": self.reporting_config
        }


# Environment-specific test data
class EnvironmentTestData:
    
    @staticmethod
    def get_search_terms(environment: Environment) -> list:
        common_terms = [
            "Python programming",
            "Selenium automation",
            "Web development"
        ]
        
        env_specific = {
            Environment.LOCAL: common_terms + ["local test", "development"],
            Environment.DEV: common_terms + ["dev environment", "testing"],
            Environment.STAGING: common_terms + ["staging test", "pre-production"],
            Environment.PROD: common_terms + ["production test", "live"],
            Environment.CI: common_terms + ["ci test", "automated"]
        }
        
        return env_specific.get(environment, common_terms)
    
    @staticmethod
    def get_test_users(environment: Environment) -> dict:
        # Note: In real scenarios, avoid hardcoding credentials
        users = {
            Environment.LOCAL: {
                "test_user": {
                    "username": "local_test_user",
                    "password": "local_password"
                }
            },
            Environment.DEV: {
                "test_user": {
                    "username": "dev_test_user",
                    "password": "dev_password"
                }
            },
            Environment.STAGING: {
                "test_user": {
                    "username": "staging_test_user",
                    "password": "staging_password"
                }
            },
            Environment.PROD: {
                "test_user": {
                    "username": "prod_test_user",
                    "password": "prod_password"
                }
            },
            Environment.CI: {
                "test_user": {
                    "username": "ci_test_user",
                    "password": "ci_password"
                }
            }
        }
        
        return users.get(environment, {})


# Factory function to get environment configuration
def get_environment_config(env_name: str = None) -> EnvironmentConfig:
    return EnvironmentConfig(env_name)