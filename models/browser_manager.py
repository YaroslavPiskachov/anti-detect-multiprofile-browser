import traceback
from threading import Thread
from queue import Queue
from playwright.sync_api import sync_playwright
from PySide6.QtCore import QObject, Signal, QTimer


class BrowserManager(QObject):
    exception_occurred = Signal(str, str)  # profile_name, exception_text

    def __init__(self):
        super().__init__()
        self.browsers = {}  # {profile_name: (thread, exception_queue)}
        self.check_timers = {}  # {profile_name: QTimer}

    def start_browser(self, profile):
        exception_queue = Queue()

        def run_browser():
            try:
                with sync_playwright() as p:
                    browser_type = p.chromium
                    context_options = self._create_context_options(profile)
                    browser = browser_type.launch()
                    context = browser.new_context(**context_options)
                    page = context.new_page()
                    page.goto("https://browserleaks.com/javascript")
                    page.wait_for_timeout(-1)
            except Exception as e:
                exception_queue.put(traceback.format_exc())

        thread = Thread(target=run_browser)
        thread.start()
        self.browsers[profile.name] = (thread, exception_queue)
        self.start_exception_checker(profile.name)

    def _create_context_options(self, profile):
        return {
            "proxy": {
                "server": f"http://{profile.proxy_settings['ip']}:{profile.proxy_settings['port']}",
                "username": profile.proxy_settings['username'],
                "password": profile.proxy_settings['password'],
            },
            "user_agent": profile.fingerprint_data.get('user_agent'),
            "viewport": profile.fingerprint_data.get('viewport'),
            "locale": profile.fingerprint_data.get('locale'),
            "timezone_id": profile.fingerprint_data.get('timezone'),
            "geolocation": profile.fingerprint_data.get('geolocation'),
            "permissions": profile.fingerprint_data.get('permissions', []),
        }

    def stop_browser(self, profile_name):
        if profile_name in self.browsers:
            # Implement browser stopping logic here
            # self.browsers[profile_name][0].stop()
            del self.browsers[profile_name]
            self.stop_exception_checker(profile_name)

    def start_exception_checker(self, profile_name):
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.check_exceptions(profile_name))
        timer.start(1000)  # Check every 1000 ms (1 second)
        self.check_timers[profile_name] = timer

    def stop_exception_checker(self, profile_name):
        if profile_name in self.check_timers:
            self.check_timers[profile_name].stop()
            del self.check_timers[profile_name]

    def check_exceptions(self, profile_name):
        if profile_name in self.browsers:
            thread, exception_queue = self.browsers[profile_name]
            if not exception_queue.empty():
                exception = exception_queue.get()
                self.exception_occurred.emit(profile_name, exception)

            if not thread.is_alive():
                self.stop_exception_checker(profile_name)
                del self.browsers[profile_name]