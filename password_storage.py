from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem, QLabel
from PySide6.QtCore import QTimer

class PasswordStorageWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.db_manager = DatabaseManager(crypto_manager)

        self.layout = QVBoxLayout(self)
        self.password_list = QListWidget()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_passwords)

        self.layout.addWidget(self.password_list)
        self.layout.addWidget(self.refresh_button)

        self.load_passwords()

    def load_passwords(self):
        self.password_list.clear()
        entries = self.db_manager.get_all_passwords()

        for entry in entries:
            item_widget = QWidget()
            h_layout = QHBoxLayout(item_widget)

            label = QLabel(f"{entry['website']} ({entry['email']})")
            password_label = QLabel("********")

            show_button = QPushButton("Show")
            delete_button = QPushButton("Delete")

            def reveal_password(label=password_label, password=entry['password']):
                label.setText(password)
                QTimer.singleShot(15000, lambda: label.setText("********"))

            show_button.clicked.connect(reveal_password)
            delete_button.clicked.connect(lambda _, id=entry['id']: self.delete_entry(id))

            h_layout.addWidget(label)
            h_layout.addWidget(password_label)
            h_layout.addWidget(show_button)
            h_layout.addWidget(delete_button)

            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.password_list.addItem(item)
            self.password_list.setItemWidget(item, item_widget)

    def delete_entry(self, entry_id):
        self.db_manager.delete_password(entry_id)
        self.load_passwords()
