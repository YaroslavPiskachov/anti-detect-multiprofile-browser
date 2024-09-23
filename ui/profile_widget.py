from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class ProfileWidget(QWidget):
    def __init__(self, profile, browser_manager):
        super().__init__()
        self.profile = profile
        self.browser_manager = browser_manager
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        profile_label = QLabel(f"Profile: {self.profile.name}")
        profile_label.setFixedWidth(150)
        layout.addWidget(profile_label)

        self.toggle_button = QPushButton("Start")
        self.toggle_button.setFixedWidth(80)
        self.toggle_button.clicked.connect(self.toggle_browser)
        layout.addWidget(self.toggle_button)

        self.status_label = QLabel("Stopped")
        self.status_label.setFixedWidth(80)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)

    def toggle_browser(self):
        if self.profile.name in self.browser_manager.browsers:
            self.browser_manager.stop_browser(self.profile.name)
        else:
            self.browser_manager.start_browser(self.profile)

    def update_status(self, status):
        status_styles = {
            "Running": ("Stop", "color: green;"),
            "Stopped": ("Start", "color: red;"),
            "Starting": ("Stop", "color: orange;")
        }

        button_text, label_style = status_styles.get(status, ("Start", ""))
        self.toggle_button.setText(button_text)
        self.status_label.setText(status)
        self.status_label.setStyleSheet(label_style)