from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QLineEdit,
    QPushButton, QSlider, QTabWidget
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from Generation import PasswordGenerator  # Import the PasswordGenerator class


class PasswordGeneratorWidget(QWidget):
    """
    Widget for generating secure passwords and saving them to the database.
    """

    def __init__(self, db_manager, storage_widget):
        super().__init__()
        self.crypto = db_manager.crypto  # Reference to the encryption manager
        self.db_manager = db_manager     # Reference to the database manager
        self.storage_widget = storage_widget  # Reference to the storage widget (for refreshing after save)
        self.generator = PasswordGenerator()  # Initialize password generator logic

        self.setWindowTitle("Password Generator")  # Set window title
        self.layout = QVBoxLayout(self)  # Main vertical layout

        # --- Password Options (Checkboxes) ---
        self.special_chars_checkbox = QCheckBox("Special Characters")
        self.numbers_checkbox = QCheckBox("Numbers")
        self.letters_checkbox = QCheckBox("Upper/Lowercase Letters")

        # Connect checkbox state changes to updating password requirements
        self.special_chars_checkbox.stateChanged.connect(self.update_requirements)
        self.numbers_checkbox.stateChanged.connect(self.update_requirements)
        self.letters_checkbox.stateChanged.connect(self.update_requirements)

        # --- Password Length (Slider + Label) ---
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(8)   # Minimum length
        self.length_slider.setMaximum(32)  # Maximum length
        self.length_slider.setValue(8)     # Default value
        self.slider_value_label = QLabel("8")  # Label showing current length
        self.length_slider.valueChanged.connect(self.update_length)

        # --- Password Output (Line Edit + Buttons) ---
        self.password_out_line = QLineEdit()

        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_password)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # --- Site and User Info ---
        self.website_label = QLabel("Website:")
        self.website_line_edit = QLineEdit()

        self.mail_label = QLabel("E-mail:")
        self.mail_line_edit = QLineEdit()

        self.nickname_label = QLabel("Nickname (Optional):")
        self.nickname_line_edit = QLineEdit()

        self.add_storage_button = QPushButton("Add to Storage")
        self.add_storage_button.clicked.connect(self.add_to_storage)

        # --- Layout organization ---
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(self.special_chars_checkbox)
        self.checkbox_layout.addWidget(self.numbers_checkbox)
        self.checkbox_layout.addWidget(self.letters_checkbox)

        self.slider_layout = QHBoxLayout()
        self.slider_layout.addWidget(self.length_slider)
        self.slider_layout.addWidget(self.slider_value_label)

        self.password_layout = QHBoxLayout()
        self.password_layout.addWidget(self.password_out_line)
        self.password_layout.addWidget(self.generate_button)
        self.password_layout.addWidget(self.copy_button)

        self.details_layout = QVBoxLayout()
        self.details_layout.addWidget(self.website_label)
        self.details_layout.addWidget(self.website_line_edit)
        self.details_layout.addWidget(self.mail_label)
        self.details_layout.addWidget(self.mail_line_edit)
        self.details_layout.addWidget(self.nickname_label)
        self.details_layout.addWidget(self.nickname_line_edit)
        self.details_layout.addWidget(self.add_storage_button)

        # Add all sub-layouts to the main layout
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addLayout(self.slider_layout)
        self.layout.addLayout(self.password_layout)
        self.layout.addLayout(self.details_layout)

        self.setLayout(self.layout)

    def update_requirements(self):
        """
        Updates password generation rules based on selected checkboxes.
        """
        self.generator.set_requirements(
            uppercase=self.letters_checkbox.isChecked(),
            lowercase=self.letters_checkbox.isChecked(),
            digit=self.numbers_checkbox.isChecked(),
            special=self.special_chars_checkbox.isChecked(),
            length=self.generator.length
        )

    def update_length(self, value):
        """
        Updates password length based on the slider value.
        """
        self.generator.length = value
        self.slider_value_label.setText(str(value))

    def generate_password(self):
        """
        Generates a password and displays it in the output field.
        """
        password = self.generator.generate_password()
        self.password_out_line.setText(password)

    def copy_to_clipboard(self):
        """
        Copies the generated password to the system clipboard.
        """
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.password_out_line.text())

    def add_to_storage(self):
        """
        Saves the generated password (and associated data) to the database.
        Also refreshes the storage table after saving.
        """
        website = self.website_line_edit.text()
        email = self.mail_line_edit.text()
        nickname = self.nickname_line_edit.text()
        password = self.password_out_line.text()

        if website and email and password:
            self.db_manager.save_password(website, email, nickname, password)
            # Clear input fields after saving
            self.website_line_edit.clear()
            self.mail_line_edit.clear()
            self.password_out_line.clear()
            self.nickname_line_edit.clear()
            self.storage_widget.load_passwords()  # Refresh the table
