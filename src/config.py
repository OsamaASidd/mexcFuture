import os
from pathlib import Path

class Config:
    CHROME_PROFILE_PATH = r"C:\Users\Abdual\AppData\Local\Google\Chrome\User Data"
    CHROME_PROFILE_NAME = "Profile 2"
    
    MEXC_BASE_URL = "https://futures.testnet.mexc.com/futures/"
    
    DEFAULT_STOP_LOSS_PERCENT = 35
    DEFAULT_TAKE_PROFIT_PERCENT = 50
    
    WAIT_TIMEOUT = 20
    
    LOG_FILE = Path("logs/trading.log")
    
    @classmethod
    def get_chrome_options(cls):
        from selenium import webdriver
        
        options = webdriver.ChromeOptions()
        
        # Use the Chrome profile
        options.add_argument(f"--user-data-dir={cls.CHROME_PROFILE_PATH}")
        options.add_argument(f"--profile-directory={cls.CHROME_PROFILE_NAME}")
        
        # Essential options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--start-maximized")
        
        # Prevent detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add preferences
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "exit_type": "Normal",
            "exited_cleanly": True,
            "session.restore_on_startup": 4,
            "session.startup_urls": ["about:blank"]
        }
        options.add_experimental_option("prefs", prefs)
        
        # Disable restore pages
        options.add_argument("--disable-session-crashed-bubble")
        options.add_argument("--disable-infobars")
        
        return options