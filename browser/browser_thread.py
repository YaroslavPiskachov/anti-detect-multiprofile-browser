from PySide6.QtCore import QThread, Signal
from playwright.sync_api import sync_playwright
import logging
import os
from queue import Queue


class BrowserThread(QThread):
    exception_occurred = Signal(str, str)  # profile_name, exception_text
    status_changed = Signal(str, str)  # profile_name, status

    def __init__(self, profile):
        super().__init__()
        self.profile = profile
        self.exception_queue = Queue()
        self.logger = logging.getLogger(__name__)
        self.playwright = None
        self.browser_context = None

    def run(self):
        self.logger.info(f"Starting browser for profile: {self.profile.name}")
        self.status_changed.emit(self.profile.name, "Starting")

        try:
            with sync_playwright() as self.playwright:
                self._launch_browser()
                self.status_changed.emit(self.profile.name, "Running")
                # Wait for the browser context to be closed
                self.browser_context.wait_for_event('close')
        except Exception as e:
            self.logger.error(f"Exception in browser thread for profile {self.profile.name}: {str(e)}")
            self.exception_occurred.emit(self.profile.name, str(e))
        finally:
            self.status_changed.emit(self.profile.name, "Stopped")
            self.logger.info(f"Browser thread finished for profile: {self.profile.name}")

    def _launch_browser(self):
        self.logger.debug(f"Creating context for profile: {self.profile.name}")
        context_options = self._create_context_options()
        user_data_dir = os.path.join("browser_data", self.profile.name)
        self.browser_context = self.playwright.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            **context_options
        )
        page = self.browser_context.new_page()
        page.goto("https://browserleaks.com/javascript")

    def _create_context_options(self):
        return {
            "proxy": {
                "server": f"http://{self.profile.proxy_settings['ip']}:{self.profile.proxy_settings['port']}",
                "username": self.profile.proxy_settings['username'],
                "password": self.profile.proxy_settings['password'],
            },
            "user_agent": self.profile.fingerprint_data.get('user_agent'),
            "viewport": self.profile.fingerprint_data.get('viewport'),
            "locale": self.profile.fingerprint_data.get('locale'),
            "timezone_id": self.profile.fingerprint_data.get('timezone'),
            "geolocation": self.profile.fingerprint_data.get('geolocation'),
            "permissions": self.profile.fingerprint_data.get('permissions', []),
        }

    def stop(self):
        if self.browser_context:
            self.browser_context.close()