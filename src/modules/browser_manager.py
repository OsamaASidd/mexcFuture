from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import OperationType
import logging
import platform
from src.config import Config

logger = logging.getLogger(__name__)

class BrowserManager:
    def __init__(self, use_profile=True):
        self.driver = None
        self.wait = None
        self.use_profile = use_profile
        
    def initialize_browser(self):
        try:
            logger.info("Initializing Chrome browser...")
            
            if self.use_profile:
                logger.info(f"Profile path: {Config.CHROME_PROFILE_PATH}")
                logger.info(f"Profile name: {Config.CHROME_PROFILE_NAME}")
                options = Config.get_chrome_options()
            else:
                logger.info("Running without profile (clean browser)")
                options = webdriver.ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--start-maximized")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            
            # Wait a moment for browser to load
            import time
            time.sleep(2)
            
            # Close any restore tabs/windows
            try:
                # Get all window handles
                windows = self.driver.window_handles
                if len(windows) > 1:
                    logger.info(f"Found {len(windows)} windows open, closing extras...")
                    # Keep the last window, close others
                    for window in windows[:-1]:
                        self.driver.switch_to.window(window)
                        self.driver.close()
                    # Switch back to the main window
                    self.driver.switch_to.window(windows[-1])
                
                # Check if current page is a restore page
                current_url = self.driver.current_url
                if "chrome://restart" in current_url or "chrome://settings/resetProfileSettings" in current_url:
                    logger.info("Detected restore page, opening new tab...")
                    self.driver.get("about:blank")
                    
            except Exception as e:
                logger.debug(f"No restore tabs to close: {e}")
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)
            
            logger.info("Browser initialized successfully")
            return self.driver
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            if "Chrome instance exited" in str(e):
                logger.error("Chrome profile might be in use. Close all Chrome windows or run without profile.")
            raise
    
    def navigate_to(self, url):
        try:
            logger.info(f"Navigating to {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            return False
    
    def close(self):
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()
            self.driver = None
            self.wait = None