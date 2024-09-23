from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
from models.profile import Profile

class ProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Profile")
        self.layout = QVBoxLayout(self)
        self.init_ui()

    def init_ui(self):
        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        form_layout.addRow("Profile Name:", self.name_edit)

        self.proxy_ip_edit = QLineEdit()
        form_layout.addRow("Proxy IP:", self.proxy_ip_edit)

        self.proxy_port_edit = QLineEdit()
        form_layout.addRow("Proxy Port:", self.proxy_port_edit)

        self.proxy_username_edit = QLineEdit()
        form_layout.addRow("Proxy Username:", self.proxy_username_edit)

        self.proxy_password_edit = QLineEdit()
        self.proxy_password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Proxy Password:", self.proxy_password_edit)

        self.user_agent_edit = QLineEdit()
        form_layout.addRow("User Agent:", self.user_agent_edit)

        self.layout.addLayout(form_layout)

        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        buttons.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(cancel_button)

        self.layout.addLayout(buttons)

    def get_profile(self):
        return Profile(
            name=self.name_edit.text(),
            proxy_settings={
                'ip': self.proxy_ip_edit.text(),
                'port': self.proxy_port_edit.text(),
                'username': self.proxy_username_edit.text(),
                'password': self.proxy_password_edit.text(),
            },
            fingerprint_data={
                'user_agent': self.user_agent_edit.text(),
                'viewport': {'width': 1920, 'height': 1080},
                'locale': 'en-US',
                'timezone': 'America/New_York',
                'geolocation': {'latitude': 40.7128, 'longitude': -74.0060},
                'permissions': ['geolocation']
            }
        )