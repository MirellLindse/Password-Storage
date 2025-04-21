from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QInputDialog, QMessageBox
import sys
from gui_generation import PasswordGeneratorWidget
from gui_storage import PasswordStorageWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PSAGA")
        self.setFixedSize(680, 530)
        main_layout = QVBoxLayout()
        self.password_widget = PasswordGeneratorWidget()
        self.storage_widget = PasswordStorageWidget()

        main_layout.addWidget(self.password_widget)
        main_layout.addWidget(self.storage_widget)

        self.setLayout(main_layout)


def password_input():
        text, ok = QInputDialog.getText(None, "Авторизация", "Введите пароль:")
        if ok:
            if text:
                return True, text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    result = password_input()
    if result and result[1]:
        window = MainWindow()
        window.show()
        print(result)
        sys.exit(app.exec())
        