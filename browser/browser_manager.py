from PySide6.QtCore import QObject, Signal
import logging
from typing import Dict
from .browser_thread import BrowserThread


class BrowserManager(QObject):
    exception_occurred = Signal(str, str)  # profile_name, exception_text
    status_changed = Signal(str, str)  # profile_name, status

    def __init__(self):
        super().__init__()
        self._setup_logging()
        self.browsers: Dict[str, BrowserThread] = {}

    def _setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def start_browser(self, profile):
        self.logger.info(f"Request to start browser for profile: {profile.name}")

        if profile.name in self.browsers:
            self.logger.warning(f"Browser already running for profile: {profile.name}")
            return

        browser_thread = BrowserThread(profile)
        self._setup_thread_connections(browser_thread)
        browser_thread.start()

        self.browsers[profile.name] = browser_thread
        self.logger.info(f"Browser thread started for profile: {profile.name}")

    def _setup_thread_connections(self, browser_thread: BrowserThread):
        browser_thread.exception_occurred.connect(self.exception_occurred)
        browser_thread.status_changed.connect(self.status_changed)
        browser_thread.finished.connect(lambda: self._on_browser_finished(browser_thread.profile.name))

    def stop_browser(self, profile_name: str):
        if profile_name in self.browsers:
            self.logger.info(f"Stopping browser for profile: {profile_name}")
            browser_thread = self.browsers[profile_name]
            browser_thread.stop()
            browser_thread.wait()
            del self.browsers[profile_name]
            self.logger.info(f"Browser stopped for profile: {profile_name}")
        else:
            self.logger.warning(f"Attempted to stop non-existent browser for profile: {profile_name}")

    def _on_browser_finished(self, profile_name: str):
        if profile_name in self.browsers:
            del self.browsers[profile_name]
            self.logger.info(f"Browser finished for profile: {profile_name}")

    def cleanup(self):
        self.logger.info("Starting cleanup of all browser threads")
        for profile_name in list(self.browsers.keys()):
            self.stop_browser(profile_name)
        self.logger.info("Cleanup completed")