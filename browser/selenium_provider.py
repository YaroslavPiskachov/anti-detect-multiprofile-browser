import os
import undetected_chromedriver as uc
import logging
from browser.browser_provider import BrowserProvider

class SeleniumProvider(BrowserProvider):
    def __init__(self):
        self.driver = None
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def start(self):
        options = uc.ChromeOptions()

        # Set your user data directory
        user_data_dir = os.path.join("browser_data", "profile")  # Modify as needed
        options.add_argument(f"--user-data-dir={user_data_dir}")  # Load user profile

        # Set additional options as needed
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument("--no-sandbox")  # Caution with security
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--enable-extensions")  # Enable extensions

        # Initialize the undetected Chrome driver
        self.driver = uc.Chrome(options=options)

    def start_with_context(self, profile):
        options = uc.ChromeOptions()

        # User data directory based on the profile
        user_data_dir = os.path.join("browser_data", profile.name)
        os.makedirs(user_data_dir, exist_ok=True)  # Create directory if it doesn't exist
        options.add_argument(f"--user-data-dir={user_data_dir}")  # Load user profile

        # Set context options based on the profile
        context_options = self._create_context_options(profile)
        for option in context_options:
            options.add_argument(option)

        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')

        # Logging preferences
        log_path = os.path.join(user_data_dir, 'chrome_log.txt')  # Specify log file path
        options.add_argument(f'--log-path={log_path}')  # Specify log path
        options.add_argument('--enable-logging')  # Enable logging
        options.add_argument('--v=1')  # Set log verbosity level (0-3)

        # Initialize the undetected Chrome driver
        self.driver = uc.Chrome(options=options)
        self.read_logs(log_path)

    def read_logs(self, log_path):
        try:
            with open(log_path, 'r') as log_file:
                logs = log_file.readlines()
                for log in logs:
                    self.logger.info(log.strip())
        except Exception as e:
            self.logger.error(f"Error reading log file: {e}")

    def stop(self):
        if self.driver:
            self.driver.quit()

    def create_context(self):
        # Create a new browser context (not fully needed for Selenium, as profiles are managed by user-data-dir)
        pass

    def close_context(self):
        # Selenium manages contexts through the user-data-dir
        pass

    def new_page(self):
        # Return the current driver to allow navigation and manipulation
        return self.driver

    def go_to_url(self, url):
        self.driver.get(url)

    @staticmethod
    def _create_context_options(profile):
        options = []

        # Proxy settings
        if profile.proxy_settings:
            proxy = f"{profile.proxy_settings['ip']}:{profile.proxy_settings['port']}"
            options.append(f"--proxy-server={proxy}")
            # Add proxy authentication if username and password are provided
            if 'username' in profile.proxy_settings and 'password' in profile.proxy_settings:
                proxy_auth = f"{profile.proxy_settings['username']}:{profile.proxy_settings['password']}@"
                options.append(f"--proxy-auth={proxy_auth}")

        # User agent
        if 'user_agent' in profile.fingerprint_data:
            options.append(f"user-agent={profile.fingerprint_data['user_agent']}")

        # Viewport
        viewport = profile.fingerprint_data.get('viewport', {})
        if viewport:
            options.append(f"--window-size={viewport['width']},{viewport['height']}")

        # Locale
        if 'locale' in profile.fingerprint_data:
            options.append(f"--lang={profile.fingerprint_data['locale']}")

        # Permissions for geolocation
        options.append("--enable-geolocation")

        return options


# Example usage
if __name__ == "__main__":
    provider = SeleniumProvider()
    provider.start()

    # Navigate to Chrome Web Store
    provider.go_to_url("https://chrome.google.com/webstore/category/extensions")

    # Here you would implement steps to install extensions as needed, or open the extension page directly.

    # Example to install an unpacked extension (update with your unpacked extension ID):
    # provider.install_extension('YOUR_UNPACKED_EXTENSION_ID')

    # Clean up
    provider.stop()
