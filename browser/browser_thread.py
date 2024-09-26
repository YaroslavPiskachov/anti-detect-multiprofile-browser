from PySide6.QtCore import QThread, Signal
import logging

from browser.browser_provider import BrowserProvider

class BrowserThread(QThread):
    exception_occurred = Signal(str, str)
    status_changed = Signal(str, str)

    def __init__(self, profile, browser_provider: BrowserProvider):
        super().__init__()
        self.profile = profile
        self.logger = logging.getLogger(__name__)
        self.browser_provider = browser_provider
        self._stop_requested = False

    def run(self):
        self.logger.info(f"Starting browser for profile: {self.profile.name}")
        self.status_changed.emit(self.profile.name, "Starting")

        try:
            #self.browser_provider.start()
            #self.browser_provider.create_context(self.profile)
            self.browser_provider.start_with_context(self.profile)
            self.status_changed.emit(self.profile.name, "Running")

            # Open an initial page
            #page = self.browser_provider.new_page()
            #page.goto("https://browserleaks.com/javascript")

            # Wait until stop is requested
            while not self._stop_requested:
                self.msleep(1000)
        except Exception as e:
            self.logger.error(f"Exception in browser thread for profile {self.profile.name}: {str(e)}")
            self.exception_occurred.emit(self.profile.name, str(e))
        finally:
            self._cleanup()

    def stop(self):
        self._stop_requested = True

    def _cleanup(self):
        try:
            self.browser_provider.close_context()
            self.browser_provider.stop()
        except Exception as e:
            self.logger.error(f"Error during cleanup for profile {self.profile.name}: {str(e)}")
        finally:
            self.status_changed.emit(self.profile.name, "Stopped")
            self.logger.info(f"Browser thread finished for profile: {self.profile.name}")