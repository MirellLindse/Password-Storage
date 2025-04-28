# Import necessary modules
from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton
from qt_material import list_themes, apply_stylesheet
import os
import json

"""
THIS TOOK WAY LONGER THAN IT SHOULD'VE TAKEN...
"""

class SettingsDialog(QDialog):
    # Path to store user settings (in %LOCALAPPDATA%\PSAGA\settings.json)
    SETTINGS_PATH = os.path.join(os.getenv('LOCALAPPDATA'), "PSAGA", "settings.json")

    def __init__(self, app, current_theme):
        super().__init__()
        self.app = app  # Reference to QApplication instance
        self.current_theme = current_theme  # Current applied theme
        self.setWindowTitle("Settings")  # Set dialog window title

        # Main layout for the dialog
        layout = QVBoxLayout(self)

        # Create dropdown with all available themes
        self.combo = QComboBox()
        self.themes = list_themes()  # Fetch available themes from qt_material
        self.combo.addItems(self.themes)
        layout.addWidget(self.combo)

        # Set current theme as selected in dropdown
        self.combo.setCurrentText(self.current_theme)

        # Apply button
        apply_button = QPushButton("Apply Theme")
        apply_button.clicked.connect(self.apply_theme)  # Apply the selected theme when clicked
        layout.addWidget(apply_button)

    def apply_theme(self):
        """Applies the selected theme and saves it."""
        theme = self.combo.currentText()  # Get the selected theme
        apply_stylesheet(self.app, theme=theme, extra={'density_scale': '-2'})  # Apply new theme
        self.save_theme(theme)  # Save the selection
        self.accept()  # Close the settings window

    def save_theme(self, theme):
        """Saves the selected theme to settings.json."""
        os.makedirs(os.path.dirname(self.SETTINGS_PATH), exist_ok=True)  # Create directory if it doesn't exist
        with open(self.SETTINGS_PATH, "w") as f:
            json.dump({"theme": theme}, f)  # Save the theme into a JSON file
