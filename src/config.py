import os
from pathlib import Path

class Config:
    # Update this to your actual Chrome profile path
    CHROME_PROFILE_PATH = r"C:\Users\osama.ahmed\AppData\Local\Google\Chrome\User Data"
    CHROME_PROFILE_NAME = "Profile 2"
    
    # Remote debugging port - Chrome must be started with this port
    REMOTE_DEBUGGING_PORT = 9222
    
    MEXC_BASE_URL = "https://futures.testnet.mexc.com/futures/"
    
    DEFAULT_STOP_LOSS_PERCENT = 35
    DEFAULT_TAKE_PROFIT_PERCENT = 50
    
    WAIT_TIMEOUT = 20
    
    LOG_FILE = Path("logs/trading.log")
    
    @classmethod
    def get_chrome_options_with_profile(cls):
        """Chrome options when starting fresh with profile (Chrome must be closed)"""
        from selenium import webdriver
        
        options = webdriver.ChromeOptions()
        
        # Use the Chrome profile
        options.add_argument(f"--user-data-dir={cls.CHROME_PROFILE_PATH}")
        options.add_argument(f"--profile-directory={cls.CHROME_PROFILE_NAME}")
        
        # Enable remote debugging so we can reconnect later
        options.add_argument(f"--remote-debugging-port={cls.REMOTE_DEBUGGING_PORT}")
        
        # Essential options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        
        # Prevent detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        return options
    
    @classmethod
    def get_chrome_options_attach(cls):
        """Chrome options to attach to existing Chrome with remote debugging"""
        from selenium import webdriver
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{cls.REMOTE_DEBUGGING_PORT}")
        
        return options
    
    @classmethod
    def get_chrome_options_clean(cls):
        """Chrome options for clean browser without profile"""
        from selenium import webdriver
        
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        return options