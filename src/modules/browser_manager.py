import logging
import subprocess
import time
import socket
import undetected_chromedriver as uc

from src.config import Config

logger = logging.getLogger(__name__)


def is_port_in_use(port):
    """Check if a port is in use (Chrome debugging port)"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


class BrowserManager:
    def __init__(self, use_profile=True):
        self.driver = None
        self.use_profile = use_profile
        self.attached_to_existing = False

    def initialize_browser(self):
        """
        Initialization order:
        1. Attach to existing Chrome (debugging)
        2. Start Chrome with profile
        3. Start clean Chrome
        """

        # Strategy 1: Attach to existing Chrome
        if self.use_profile and is_port_in_use(Config.REMOTE_DEBUGGING_PORT):
            try:
                logger.info(
                    f"Found Chrome on debugging port {Config.REMOTE_DEBUGGING_PORT}, attaching..."
                )
                return self._attach_to_existing_chrome()
            except Exception as e:
                logger.warning(f"Attach failed: {e}")

        # Strategy 2: Start Chrome with profile
        if self.use_profile:
            try:
                logger.info("Starting Chrome with profile...")
                return self._start_chrome_with_profile()
            except Exception as e:
                logger.warning(f"Profile launch failed: {e}")
                logger.info("Falling back to clean Chrome...")

        # Strategy 3: Clean Chrome
        logger.info("Starting clean Chrome (manual login required)")
        return self._start_chrome_clean()

    def _attach_to_existing_chrome(self):
        options = Config.get_chrome_options_attach()

        self.driver = uc.Chrome(
            options=options,
            use_subprocess=True,
        )

        self.attached_to_existing = True
        logger.info("Attached to existing Chrome successfully")
        return self.driver

    def _start_chrome_with_profile(self):
        logger.info(f"Profile path: {Config.CHROME_PROFILE_PATH}")
        logger.info(f"Profile name: {Config.CHROME_PROFILE_NAME}")

        options = Config.get_chrome_options_with_profile()

        self.driver = uc.Chrome(
            options=options,
            use_subprocess=True,
        )

        time.sleep(2)
        self._close_extra_tabs()

        logger.info("Chrome started with profile successfully")
        return self.driver

    def _start_chrome_clean(self):
        options = Config.get_chrome_options_clean()

        self.driver = uc.Chrome(
            options=options,
            use_subprocess=True,
        )

        logger.info("Clean Chrome started successfully")
        return self.driver

    def _close_extra_tabs(self):
        """Close Chrome restore tabs"""
        try:
            handles = self.driver.window_handles
            if len(handles) > 1:
                logger.info(f"Closing {len(handles) - 1} extra tabs")
                for h in handles[:-1]:
                    self.driver.switch_to.window(h)
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
            logger.error(f"Navigation failed: {e}")
            return False

    def close(self):
        """Close browser unless attached to user's Chrome"""
        if not self.driver:
            return

        if self.attached_to_existing:
            logger.info("Detaching from Chrome (leaving browser open)")
            self.driver = None
        else:
            logger.info("Closing Chrome")
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
