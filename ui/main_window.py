from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, \
    QListWidgetItem, QMessageBox
from PySide6.QtCore import Qt

from browser.playwright_provider import PlaywrightProvider
from browser.selenium_provider import SeleniumProvider
from .profile_dialog import ProfileDialog
from .profile_widget import ProfileWidget
from browser.browser_manager import BrowserManager
from utils.config import save_profiles, load_profiles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anti-Detect Browser Manager")
        self.setGeometry(100, 100, 600, 400)
        self.profiles = load_profiles()
        self.browser_provider = SeleniumProvider()
        self.browser_manager = BrowserManager(self.browser_provider)
        self.init_ui()
        self.connect_signals()
        self.update_profile_list()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.profile_list = QListWidget()
        layout.addWidget(self.profile_list)

        button_layout = QHBoxLayout()
        add_profile_button = QPushButton("Add Profile")
        add_profile_button.clicked.connect(self.add_profile)
        button_layout.addWidget(add_profile_button)

        layout.addLayout(button_layout)

    def connect_signals(self):
        self.browser_manager.exception_occurred.connect(self.on_browser_exception)
        self.browser_manager.status_changed.connect(self.on_browser_status_changed)

    def add_profile(self):
        dialog = ProfileDialog(self)
        if dialog.exec():
            profile = dialog.get_profile()
            self.profiles.append(profile)
            save_profiles(self.profiles)
            self.update_profile_list()

    def update_profile_list(self):
        self.profile_list.clear()
        for profile in self.profiles:
            item = QListWidgetItem(self.profile_list)
            custom_widget = ProfileWidget(profile, self.browser_manager)
            item.setSizeHint(custom_widget.sizeHint())
            self.profile_list.addItem(item)
            self.profile_list.setItemWidget(item, custom_widget)

    def closeEvent(self, event):
        self.browser_manager.cleanup()
        super().closeEvent(event)

    def on_browser_exception(self, profile_name, exception_text):
        QMessageBox.warning(self, "Browser Exception",
                            f"An error occurred in the browser for profile {profile_name}:\n{exception_text}")

    def on_browser_status_changed(self, profile_name, status):
        for index in range(self.profile_list.count()):
            item = self.profile_list.item(index)
            widget = self.profile_list.itemWidget(item)
            if isinstance(widget, ProfileWidget) and widget.profile.name == profile_name:
                widget.update_status(status)
                break