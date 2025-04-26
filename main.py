# Import necessary modules
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QInputDialog, QMessageBox
import sys

# Import local modules
from encryption import EncryptionManager
from gui_generation import PasswordGeneratorWidget
from gui_storage import PasswordStorageWidget
from db_manager import DatabaseManager

# Main window of the application
class MainWindow(QWidget):
    def __init__(self, crypto_manager):
        super().__init__()
        self.setWindowTitle("PSAGA")  # Set the window title
        self.setFixedSize(680, 530)    # Set a fixed window size

        main_layout = QVBoxLayout()    # Create the main vertical layout

        # Initialize database manager with encryption manager
        self.db_manager = DatabaseManager(crypto_manager)

        # Create widgets for password generation and storage
        self.storage_widget = PasswordStorageWidget(self.db_manager)
        self.password_widget = PasswordGeneratorWidget(self.db_manager, self.storage_widget)

        # Add widgets to the main layout
        main_layout.addWidget(self.password_widget)
        main_layout.addWidget(self.storage_widget)

        self.setLayout(main_layout)  # Set the main layout for the window

# Function to ask the user for a master password
def ask_password():
    while True:
        text, ok = QInputDialog.getText(None, "Авторизация", "Введите пароль:")
        if ok:
            try:
                crypto = EncryptionManager(text)  # Try to create an encryption manager
                return crypto  # Return the encryption object if successful
            except Exception as e:
                # Show error if something went wrong (e.g., invalid key derivation)
                QMessageBox.critical(None, "Ошибка", str(e))
        else:
            return None  # If the user canceled the dialog

# Entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    crypto = ask_password()
    if crypto:
        window = MainWindow(crypto)
        window.show()
        sys.exit(app.exec())
