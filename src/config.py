import os
from pathlib import Path
import undetected_chromedriver as uc


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
        """Start Chrome fresh using an existing profile (Chrome must be closed)"""

        options = uc.ChromeOptions()

        # Use Chrome profile
        options.add_argument(f"--user-data-dir={cls.CHROME_PROFILE_PATH}")
        options.add_argument(f"--profile-directory={cls.CHROME_PROFILE_NAME}")

        # Enable remote debugging
        options.add_argument(f"--remote-debugging-port={cls.REMOTE_DEBUGGING_PORT}")

        # Stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")

        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")

        return options

    @classmethod
    def get_chrome_options_attach(cls):
        """Attach to an already running Chrome with remote debugging enabled"""

        options = uc.ChromeOptions()
        options.add_experimental_option(
            "debuggerAddress",
            f"127.0.0.1:{cls.REMOTE_DEBUGGING_PORT}"
        )

        return options

    @classmethod
    def get_chrome_options_clean(cls):
        """Clean browser session without any profile"""

        options = uc.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return options
