# Import necessary system and UI modules
import os.path
import sys
import json

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QInputDialog, QMessageBox, QPushButton
from PySide6.QtGui import QIcon
from qt_material import apply_stylesheet

# Import local project modules
from gui_generation import PasswordGeneratorWidget
from gui_storage import PasswordStorageWidget
from db_manager import DatabaseManager
from settings_dialog import SettingsDialog

# Main application window
class MainWindow(QWidget):
    def __init__(self, master_password, app):
        super().__init__()
        self.app = app
        self.theme = theme  # Store the current theme
        self.setWindowTitle("PSAGA")  # Set the application window title
        self.setFixedSize(785, 576)   # Set a fixed window size

        main_layout = QVBoxLayout()

        # Initialize database manager and functional widgets
        self.db_manager = DatabaseManager(master_password)
        self.storage_widget = PasswordStorageWidget(self.db_manager)
        self.password_widget = PasswordGeneratorWidget(self.db_manager, self.storage_widget)

        # Add widgets to the main layout
        main_layout.addWidget(self.password_widget)
        main_layout.addWidget(self.storage_widget)

        self.setLayout(main_layout)

        # Create a small settings button (gear icon)
        settings_button = QPushButton()
        settings_button.setIcon(QIcon("icons\\settings_icon.png"))  # Set icon for the button
        settings_button.setFixedSize(24, 24)                        # Make the button small
        settings_button.setStyleSheet("border: none;")              # Remove border around button
        settings_button.clicked.connect(lambda: SettingsDialog(app, self.theme).exec())  # Open settings dialog when clicked

        # Add the settings button to the storage widget's pagination layout
        self.storage_widget.add_to_pagination(settings_button)

    def open_settings(self):
        dialog = SettingsDialog(self.app, self.theme)
        dialog.exec()

# Function to prompt the user for a master password
def ask_password():
    while True:
        text, ok = QInputDialog.getText(None, "Authorization", "Enter Password:")
        if ok:
            return text # If successful, return encryption object
        else:
            return None  # If user cancels, return None

# Function to load the saved theme from settings file
def load_theme():
    if os.path.exists(SettingsDialog.SETTINGS_PATH):
        with open(SettingsDialog.SETTINGS_PATH, "r") as f:
            settings = json.load(f)
            return settings.get("theme", None)  # Return the stored theme if exists

# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme = load_theme()
    if theme:
        apply_stylesheet(app, theme=theme, extra={'density_scale': '-2'})  # Apply saved theme
    else:
        apply_stylesheet(app, theme="dark_amber.xml", extra={'density_scale': '-2'})  # Apply default theme

    master_password = ask_password()  # Ask the user for a master password

    if master_password:
        window = MainWindow(master_password, app)
        window.show()
        sys.exit(app.exec())  # Start the main application loop
