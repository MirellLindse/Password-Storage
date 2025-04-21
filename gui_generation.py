from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QLineEdit,
    QPushButton, QSlider, QTabWidget
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from Generation import PasswordGenerator  # Import the PasswordGenerator class
from db_manager import DatabaseManager


class PasswordGeneratorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setWindowTitle("Password Generator")  # Set window title

        self.generator = PasswordGenerator()  # Create a password generator instance

        self.layout = QVBoxLayout(self)  # Main vertical layout

        # Create checkboxes for selecting password requirements
        self.special_chars_checkbox = QCheckBox("Special Characters")
        self.numbers_checkbox = QCheckBox("Numbers")
        self.letters_checkbox = QCheckBox("Upper/Lowercase letters")

        # Connect checkbox state changes to update the password requirements
        self.special_chars_checkbox.stateChanged.connect(self.update_requirements)
        self.numbers_checkbox.stateChanged.connect(self.update_requirements)
        self.letters_checkbox.stateChanged.connect(self.update_requirements)

        # Create a slider for selecting the password length
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(8)  # Minimum length 8
        self.length_slider.setMaximum(32)  # Maximum length 32
        self.length_slider.setValue(8)  # Initial value 8
        self.slider_value_label = QLabel("8")  # Label to display the slider value
        self.length_slider.valueChanged.connect(self.update_length)  # Update length when slider value changes

        # LineEdit to display the generated password
        self.password_out_line = QLineEdit()

        # Button to trigger password generation
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_password)  # Connect button click to generate password

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.website_label = QLabel("Website:")
        self.website_line_edit = QLineEdit()

        self.mail_label = QLabel("E-mail:")
        self.mail_line_edit = QLineEdit()

        self.nickname_label = QLabel("Nickname(Optional):")
        self.nickname_line_edit = QLineEdit()

        self.add_storage_button = QPushButton("Add to storage")
        self.add_storage_button.clicked.connect(self.add_to_storage)

        # Layout for checkboxes (horizontal layout)
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(self.special_chars_checkbox)
        self.checkbox_layout.addWidget(self.numbers_checkbox)
        self.checkbox_layout.addWidget(self.letters_checkbox)

        # Layout for slider and its value label (horizontal layout)
        self.slider_layout = QHBoxLayout()
        self.slider_layout.addWidget(self.length_slider)
        self.slider_layout.addWidget(self.slider_value_label)

        # Layout for the password output and generate button (horizontal layout)
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



        # Add all layouts to the main vertical layout
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addLayout(self.slider_layout)
        self.layout.addLayout(self.password_layout)
        self.layout.addLayout(self.details_layout)


        self.setLayout(self.layout)  # Set the main layout for the widget

    def update_requirements(self):
        """Updates the password generator requirements based on checkbox states"""
        self.generator.set_requirements(
            uppercase=self.letters_checkbox.isChecked(),  # Uppercase letters
            lowercase=self.letters_checkbox.isChecked(),  # Lowercase letters
            digit=self.numbers_checkbox.isChecked(),  # Numbers
            special=self.special_chars_checkbox.isChecked(),  # Special characters
            length=self.generator.length  # Keep current password length
        )

    def update_length(self, value):
        """Updates the password length based on the slider value"""
        self.generator.length = value  # Set the new password length
        self.slider_value_label.setText(str(value))  # Update the label to show the new length

    def generate_password(self):
        """Generates and displays a new password"""
        password = self.generator.generate_password()  # Generate the password
        self.password_out_line.setText(password)  # Display the generated password in the input field

    def copy_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.password_out_line.text())

    def add_to_storage(self):
        website = self.website_line_edit.text()
        email = self.mail_line_edit.text()
        password = self.password_out_line.text()
        self.db_manager.save_password(website, email, password)



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PSAGA") # Password Storage And Generation Application

        # Create a QTabWidget instance
        self.tab_widget = QTabWidget(self)

        # Create instances of the widgets to be added to tabs
        self.password_tab = PasswordGeneratorWidget()

        # Add the PasswordGeneratorWidget as a tab
        self.tab_widget.addTab(self.password_tab, "Password Generator")

        # Set up the layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)

        self.setLayout(main_layout)  # Set the main layout for the main window

