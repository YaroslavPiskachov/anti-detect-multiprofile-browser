import os

from browser.browser_provider import BrowserProvider


class PlaywrightProvider(BrowserProvider):
    def __init__(self):
        self.playwright = None
        self.browser_context = None

    def start(self):
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()

    def stop(self):
        if self.playwright:
            self.playwright.stop()

    def create_context(self, profile):
        context_options = self._create_context_options(profile)
        user_data_dir = os.path.join("browser_data", profile.name)
        self.browser_context = self.playwright.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                '--enable-extensions'  # Allows installation and use of browser extensions
                # '--disable-blink-features=AutomationControlled',  # Prevents sites from detecting automation
                # '--disable-features=IsolateOrigins,site-per-process', # Disables site isolation (help with certain automation scenarios)
                # '--disable-site-isolation-trials',  # Further disables site isolation features
                # '--no-sandbox',  # Disables the Chrome sandbox for more control (reduces security, use with caution)
                # '--disable-setuid-sandbox',  # Disables setuid sandbox (also reduces security)
                # '--ignore-certificate-errors' # Ignores SSL/TLS errors, useful for testing but risky for regular browsing
            ],
            **context_options
        )

    def close_context(self):
        if self.browser_context:
            self.browser_context.close()

    def new_page(self):
        return self.browser_context.new_page()

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