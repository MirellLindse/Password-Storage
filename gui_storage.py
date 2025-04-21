from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from db_manager import DatabaseManager

class PasswordStorageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.page = 0
        self.page_size = 5

        self.layout = QVBoxLayout(self)

        # Таблица паролей
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(6)
        self.password_table.setHorizontalHeaderLabels(["ID", "Website", "Email", "Password", "Copy", "Delete"])
        self.password_table.cellClicked.connect(self.reveal_password)  # Подключаем клик по ячейке


        self.layout.addWidget(self.password_table)

        # Панель пагинации
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("<< Prev")
        self.page_label = QLabel("Page 1")
        self.next_button = QPushButton("Next >>")
        self.update_button = QPushButton("Update")

        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.update_button.clicked.connect(self.load_passwords)


        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label, alignment=Qt.AlignCenter)
        pagination_layout.addWidget(self.next_button)
        pagination_layout.addWidget(self.update_button)
        self.layout.addLayout(pagination_layout)

        self.load_passwords()

    def load_passwords(self):
        self.password_table.setRowCount(0)
        offset = self.page * self.page_size
        entries = self.db_manager.get_all_passwords(offset)

        for row_index, entry in enumerate(entries):
            self.password_table.insertRow(row_index)

            self.password_table.setItem(row_index, 0, QTableWidgetItem(str(entry["id"])))
            self.password_table.setItem(row_index, 1, QTableWidgetItem(entry["website"]))
            self.password_table.setItem(row_index, 2, QTableWidgetItem(entry["email"]))

            # Пароль с маской и UserRole
            password_item = QTableWidgetItem("********")
            password_item.setData(Qt.ItemDataRole.UserRole, entry["password"])
            password_item.setFlags(password_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.password_table.setItem(row_index, 3, password_item)

            # Кнопка копирования
            copy_button = QPushButton("Copy")
            copy_button.setCursor(Qt.PointingHandCursor)

            # ВАЖНО: создаём lambda с замыканием на row_index
            copy_button.clicked.connect(lambda _, row=row_index: self.copy_to_clipboard(row))
            self.password_table.setCellWidget(row_index, 4, copy_button)
            
            # Кнопка удаления
            delete_button = QPushButton("Delete")
            delete_button.setCursor(Qt.PointingHandCursor)
            delete_button.clicked.connect(lambda _, entry_id=entry['id']: self.delete_entry(entry_id))
            self.password_table.setCellWidget(row_index, 5, delete_button)


        self.page_label.setText(f"Page {self.page + 1}")
        

    def next_page(self):
        self.page += 1
        self.load_passwords()

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.load_passwords()

    def reveal_password(self, row, column):
        if column == 3:  # Клик по колонке "Password"
            item = self.password_table.item(row, column)
            real_password = item.data(Qt.ItemDataRole.UserRole)
            item.setText(real_password)  # Раскрываем пароль
            self.password_table.resizeColumnToContents(3)

    def copy_to_clipboard(self, row):
        item = self.password_table.item(row, 3)
        if item:
            password = item.data(Qt.ItemDataRole.UserRole)
            QGuiApplication.clipboard().setText(password)

    def delete_entry(self, entry_id):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.db_manager.delete_password(entry_id)
            self.load_passwords()  # Обновляем таблицу после удаления
