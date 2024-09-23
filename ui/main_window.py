from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QLabel, QListWidgetItem
from PySide6.QtCore import Qt
from .profile_dialog import ProfileDialog
from models.profile import Profile
from models.browser_manager import BrowserManager
from utils.config import save_profiles, load_profiles


def on_exception(profile_name, exception):
    print(f"Exception in browser thread for profile {profile_name}:")
    print(exception)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anti-Detect Browser Manager")
        self.setGeometry(100, 100, 600, 400)
        self.profiles = load_profiles()  # Load profiles from file
        self.browser_manager = BrowserManager()
        self.browser_manager.exception_occurred.connect(on_exception)
        self.init_ui()
        self.update_profile_list()  # Update list with loaded profiles

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


class ProfileWidget(QWidget):
    def __init__(self, profile, browser_manager):
        super().__init__()
        self.profile = profile
        self.browser_manager = browser_manager

        layout = QHBoxLayout(self)
        layout.addWidget(QLabel(f"Profile: {profile.name}"))
        self.toggle_button = QPushButton("Start")
        self.toggle_button.clicked.connect(self.toggle_browser)
        layout.addWidget(self.toggle_button)

        self.status_label = QLabel("Stopped")
        layout.addWidget(self.status_label)

    def toggle_browser(self):
        if self.profile.name in self.browser_manager.browsers:
            # Browser is running, so stop it
            self.browser_manager.stop_browser(self.profile.name)
            self.toggle_button.setText("Start")
            self.status_label.setText("Stopped")
            self.status_label.setStyleSheet("color: red;")
        else:
            # Browser is not running, so start it
            self.browser_manager.start_browser(self.profile)
            self.toggle_button.setText("Stop")
            self.status_label.setText("Running")
            self.status_label.setStyleSheet("color: green;")

    def update_status(self, is_running):
        if is_running:
            self.toggle_button.setText("Stop")
            self.status_label.setText("Running")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.toggle_button.setText("Start")
            self.status_label.setText("Stopped")
            self.status_label.setStyleSheet("color: red;")
