
class BrowserManager:
    def __init__(self):
        self.browsers = []

    def add_browser(self, browser):
        self.browsers.append(browser)

    def list_browsers(self):
        return self.browsers
