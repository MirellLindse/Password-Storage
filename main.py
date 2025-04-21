from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
import sys
from gui_generation import PasswordGeneratorWidget
from gui_storage import PasswordStorageWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PSAGA")
        self.setFixedSize(680, 601)
        main_layout = QVBoxLayout()
        self.password_widget = PasswordGeneratorWidget()
        self.storage_widget = PasswordStorageWidget()

        main_layout.addWidget(self.password_widget)
        main_layout.addWidget(self.storage_widget)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
