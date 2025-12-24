from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import logging
import subprocess
import time
import socket
from src.config import Config

logger = logging.getLogger(__name__)


def is_port_in_use(port):
    """Check if a port is in use (Chrome debugging port)"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


class BrowserManager:
    def __init__(self, use_profile=True):
        self.driver = None
        self.wait = None
        self.use_profile = use_profile
        self.attached_to_existing = False
        
    def initialize_browser(self):
        """
        Initialize browser with multiple fallback strategies:
        1. Try to attach to existing Chrome with remote debugging
        2. Try to start Chrome with profile (requires all Chrome closed)
        3. Fall back to clean browser without profile
        """
        
        # Strategy 1: Try to attach to existing Chrome with remote debugging
        if self.use_profile and is_port_in_use(Config.REMOTE_DEBUGGING_PORT):
            try:
                logger.info(f"Found Chrome on debugging port {Config.REMOTE_DEBUGGING_PORT}, attaching...")
                return self._attach_to_existing_chrome()
            except Exception as e:
                logger.warning(f"Failed to attach to existing Chrome: {e}")
        
        # Strategy 2: Try to start Chrome with profile
        if self.use_profile:
            try:
                logger.info("Starting Chrome with profile...")
                return self._start_chrome_with_profile()
            except Exception as e:
                logger.warning(f"Failed to start Chrome with profile: {e}")
                logger.info("Chrome profile might be in use. Trying without profile...")
        
        # Strategy 3: Start Chrome without profile (clean browser)
        logger.info("Starting Chrome without profile (you'll need to login manually)")
        return self._start_chrome_clean()
    
    def _attach_to_existing_chrome(self):
        """Attach to an already running Chrome with remote debugging enabled"""
        try:
            options = Config.get_chrome_options_attach()
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)
            self.attached_to_existing = True
            
            # Hide webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Successfully attached to existing Chrome!")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to attach to existing Chrome: {e}")
            raise
    
    def _start_chrome_with_profile(self):
        """Start a new Chrome instance with profile"""
        try:
            logger.info(f"Profile path: {Config.CHROME_PROFILE_PATH}")
            logger.info(f"Profile name: {Config.CHROME_PROFILE_NAME}")
            
            options = Config.get_chrome_options_with_profile()
            self.driver = webdriver.Chrome(options=options)
            
            time.sleep(2)
            self._close_extra_tabs()
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)
            
            logger.info("Browser initialized successfully with profile")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to start Chrome with profile: {e}")
            raise
    
    def _start_chrome_clean(self):
        """Start Chrome without any profile"""
        try:
            options = Config.get_chrome_options_clean()
            self.driver = webdriver.Chrome(options=options)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, Config.WAIT_TIMEOUT)
            
            logger.info("Browser initialized successfully (clean - no profile)")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to start clean Chrome: {e}")
            raise
    
    def _close_extra_tabs(self):
        """Close any restore tabs that Chrome might have opened"""
        try:
            windows = self.driver.window_handles
            if len(windows) > 1:
                logger.info(f"Found {len(windows)} windows open, closing extras...")
                for window in windows[:-1]:
                    self.driver.switch_to.window(window)
                    self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception as e:
            logger.debug(f"No extra tabs to close: {e}")
    
    def navigate_to(self, url):
        try:
            logger.info(f"Navigating to {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            return False
    
    def close(self):
        """Close browser - but don't close if we attached to existing Chrome"""
        if self.driver:
            if self.attached_to_existing:
                logger.info("Detaching from Chrome (browser will remain open)")
                # Just detach, don't close the user's browser
                self.driver = None
                self.wait = None
            else:
                logger.info("Closing browser...")
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
                self.wait = None


def start_chrome_with_debugging():
    """
    Helper function to start Chrome with remote debugging enabled.
    Run this separately if you want to keep Chrome open between bot runs.
    """
    import os
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    
    cmd = [
        chrome_path,
        f"--remote-debugging-port={Config.REMOTE_DEBUGGING_PORT}",
        f"--user-data-dir={Config.CHROME_PROFILE_PATH}",
        f"--profile-directory={Config.CHROME_PROFILE_NAME}",
    ]
    
    print(f"Starting Chrome with debugging on port {Config.REMOTE_DEBUGGING_PORT}...")
    subprocess.Popen(cmd)
    print("Chrome started! You can now run the trading bot.")