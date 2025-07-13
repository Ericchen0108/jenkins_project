import os
from datetime import datetime
from PIL import Image
from selenium.common.exceptions import WebDriverException
from config.config import TestConfig


class ScreenshotUtils:
    
    @staticmethod
    def take_screenshot(driver, filename=None, custom_path=None):
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"screenshot_{timestamp}.png"
            
            if custom_path:
                filepath = os.path.join(custom_path, filename)
            else:
                filepath = os.path.join(TestConfig.SCREENSHOTS_DIR, filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            success = driver.save_screenshot(filepath)
            
            if success:
                print(f"Screenshot saved: {filepath}")
                return filepath
            else:
                print(f"Failed to save screenshot: {filepath}")
                return None
                
        except WebDriverException as e:
            print(f"WebDriver exception while taking screenshot: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while taking screenshot: {e}")
            return None
    
    @staticmethod
    def take_element_screenshot(driver, element, filename=None, custom_path=None):
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"element_screenshot_{timestamp}.png"
            
            if custom_path:
                filepath = os.path.join(custom_path, filename)
            else:
                filepath = os.path.join(TestConfig.SCREENSHOTS_DIR, filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            success = element.screenshot(filepath)
            
            if success:
                print(f"Element screenshot saved: {filepath}")
                return filepath
            else:
                print(f"Failed to save element screenshot: {filepath}")
                return None
                
        except WebDriverException as e:
            print(f"WebDriver exception while taking element screenshot: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while taking element screenshot: {e}")
            return None
    
    @staticmethod
    def take_full_page_screenshot(driver, filename=None, custom_path=None):
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"fullpage_screenshot_{timestamp}.png"
            
            if custom_path:
                filepath = os.path.join(custom_path, filename)
            else:
                filepath = os.path.join(TestConfig.SCREENSHOTS_DIR, filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            original_size = driver.get_window_size()
            
            driver.execute_script("return document.body.scrollHeight")
            page_height = driver.execute_script("return document.body.scrollHeight")
            driver.set_window_size(original_size['width'], page_height)
            
            success = driver.save_screenshot(filepath)
            
            driver.set_window_size(original_size['width'], original_size['height'])
            
            if success:
                print(f"Full page screenshot saved: {filepath}")
                return filepath
            else:
                print(f"Failed to save full page screenshot: {filepath}")
                return None
                
        except WebDriverException as e:
            print(f"WebDriver exception while taking full page screenshot: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error while taking full page screenshot: {e}")
            return None
    
    @staticmethod
    def take_comparison_screenshot(driver, test_name, step_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{step_name}_{timestamp}.png"
        return ScreenshotUtils.take_screenshot(driver, filename)
    
    @staticmethod
    def take_failure_screenshot(driver, test_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"FAILURE_{test_name}_{timestamp}.png"
        return ScreenshotUtils.take_screenshot(driver, filename)
    
    @staticmethod
    def resize_screenshot(image_path, max_width=1920, max_height=1080):
        try:
            with Image.open(image_path) as img:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                resized_path = image_path.replace('.png', '_resized.png')
                img.save(resized_path, 'PNG', optimize=True)
                
                print(f"Resized screenshot saved: {resized_path}")
                return resized_path
                
        except Exception as e:
            print(f"Error resizing screenshot: {e}")
            return None
    
    @staticmethod
    def create_screenshot_folder(folder_name):
        folder_path = os.path.join(TestConfig.SCREENSHOTS_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    @staticmethod
    def clean_old_screenshots(days_old=7):
        try:
            current_time = datetime.now()
            screenshots_dir = TestConfig.SCREENSHOTS_DIR
            
            if not os.path.exists(screenshots_dir):
                return
            
            for filename in os.listdir(screenshots_dir):
                filepath = os.path.join(screenshots_dir, filename)
                
                if os.path.isfile(filepath) and filename.endswith('.png'):
                    file_modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    days_difference = (current_time - file_modified_time).days
                    
                    if days_difference > days_old:
                        os.remove(filepath)
                        print(f"Removed old screenshot: {filename}")
                        
        except Exception as e:
            print(f"Error cleaning old screenshots: {e}")
    
    @staticmethod
    def create_test_evidence_folder(test_class_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{test_class_name}_{timestamp}"
        return ScreenshotUtils.create_screenshot_folder(folder_name)
    
    @staticmethod
    def get_screenshot_info(image_path):
        try:
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                file_modified = datetime.fromtimestamp(os.path.getmtime(image_path))
                
                with Image.open(image_path) as img:
                    width, height = img.size
                    format_type = img.format
                
                return {
                    'path': image_path,
                    'size_bytes': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'dimensions': f"{width}x{height}",
                    'format': format_type,
                    'modified': file_modified.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error getting screenshot info: {e}")
            return None