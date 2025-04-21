from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
import random
import string

class PasswordGeneratorWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        self.layout = QVBoxLayout(self)

        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Website")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_label = QLabel("Generated Password")
        self.generate_button = QPushButton("Generate")
        self.save_button = QPushButton("Save Password")

        self.generate_button.clicked.connect(self.generate_password)
        self.save_button.clicked.connect(self.save_password)

        self.layout.addWidget(self.website_input)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.save_button)

    def generate_password(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choices(chars, k=16))
        self.password_label.setText(password)

    def save_password(self):
        website = self.website_input.text()
        email = self.email_input.text()
        password = self.password_label.text()
        self.db_manager.save_password(website, email, password)
        self.website_input.clear()
        self.email_input.clear()
        self.password_label.setText("Saved!")
