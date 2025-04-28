# Import required PySide6 modules
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout, \
    QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication


class PasswordStorageWidget(QWidget):
    """
    Widget responsible for displaying, copying, revealing, and deleting password entries from the database.
    Includes pagination and an option to add external buttons (e.g., Settings).
    """

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager  # Instance of the database manager

        self.page = 0  # Current page number
        self.page_size = 5  # Number of entries displayed per page

        self.layout = QVBoxLayout(self)

        # --- Password Table ---
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(7)  # ID, Website, Email, Nickname, Password, Copy, Delete
        self.password_table.setHorizontalHeaderLabels(
            ["ID", "Website", "Email", "Nickname", "Password", "Copy", "Delete"])
        self.password_table.cellClicked.connect(self.reveal_password)

        self.layout.addWidget(self.password_table)

        # --- Pagination Controls ---
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("<< Prev")
        self.page_label = QLabel("Page 1")
        self.next_button = QPushButton("Next >>")
        self.settings_btn = QPushButton("⚙")

        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label, alignment=Qt.AlignCenter)
        self.pagination_layout.addWidget(self.next_button)
        self.layout.addLayout(self.pagination_layout)

        # Initial load
        self.load_passwords()

    def load_passwords(self):
        """
        Load and display password entries from the database.
        """
        self.password_table.setRowCount(0)  # Clear current table contents
        offset = self.page * self.page_size
        entries = self.db_manager.get_all_passwords(offset)

        for row_index, entry in enumerate(entries):
            self.password_table.insertRow(row_index)

            # Fill table cells with ID, Website, Email, Nickname
            self.password_table.setItem(row_index, 0, QTableWidgetItem(str(entry["id"])))
            self.password_table.setItem(row_index, 1, QTableWidgetItem(entry["website"]))
            self.password_table.setItem(row_index, 2, QTableWidgetItem(entry["email"]))
            self.password_table.setItem(row_index, 3, QTableWidgetItem(entry["nickname"]))

            # Password hidden by default, real password stored in UserRole
            password_item = QTableWidgetItem("********")
            password_item.setData(Qt.ItemDataRole.UserRole, entry["password"])
            password_item.setFlags(password_item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # Read-only
            self.password_table.setItem(row_index, 4, password_item)

            # Copy button
            copy_button = QPushButton("Copy")
            copy_button.setCursor(Qt.PointingHandCursor)
            copy_button.clicked.connect(lambda _, row=row_index: self.copy_to_clipboard(row))
            self.password_table.setCellWidget(row_index, 5, copy_button)

            # Delete button
            delete_button = QPushButton("Delete")
            delete_button.setCursor(Qt.PointingHandCursor)
            delete_button.clicked.connect(lambda _, entry_id=entry['id']: self.delete_entry(entry_id))
            self.password_table.setCellWidget(row_index, 6, delete_button)

        self.page_label.setText(f"Page {self.page + 1}")

    def next_page(self):
        """
        Navigate to the next page of password entries.
        """
        self.page += 1
        self.load_passwords()

    def prev_page(self):
        """
        Navigate to the previous page of password entries.
        """
        if self.page > 0:
            self.page -= 1
            self.load_passwords()

    def reveal_password(self, row, column):
        """
        Reveal the real password when clicking on the Password column.
        """
        if column == 4:
            item = self.password_table.item(row, column)
            real_password = item.data(Qt.ItemDataRole.UserRole)
            item.setText(real_password)
            self.password_table.resizeColumnToContents(4)

    def copy_to_clipboard(self, row):
        """
        Copy the selected password to the system clipboard.
        """
        item = self.password_table.item(row, 4)
        if item:
            password = item.data(Qt.ItemDataRole.UserRole)
            QGuiApplication.clipboard().setText(password)

    def delete_entry(self, entry_id):
        """
        Prompt the user to confirm deletion and remove the entry if confirmed.
        """
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.db_manager.delete_password(entry_id)
            self.load_passwords()

    def add_to_pagination(self, widget):
        """
        Add an external widget (e.g., a settings button) to the pagination bar.
        """
        self.pagination_layout.addWidget(widget)
