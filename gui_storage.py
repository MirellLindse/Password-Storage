# Import required PySide6 modules
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from db_manager import DatabaseManager

# Widget for displaying and managing stored passwords
class PasswordStorageWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager  # Receive a ready DatabaseManager instance

        self.page = 0          # Current page number
        self.page_size = 5     # How many entries to show per page

        self.layout = QVBoxLayout(self)

        # Password table
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(6)  # Columns: ID, Website, Email, Password, Copy, Delete
        self.password_table.setHorizontalHeaderLabels(["ID", "Website", "Email", "Password", "Copy", "Delete"])

        self.password_table.cellClicked.connect(self.reveal_password)  # Handle clicks to reveal password

        self.layout.addWidget(self.password_table)

        # Pagination controls
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

        self.load_passwords()  # Load data on start

    def load_passwords(self):
        """Load and display passwords from the database."""
        self.password_table.setRowCount(0)  # Clear the table
        offset = self.page * self.page_size
        entries = self.db_manager.get_all_passwords(offset)

        for row_index, entry in enumerate(entries):
            self.password_table.insertRow(row_index)

            # Add ID, Website, Email columns
            self.password_table.setItem(row_index, 0, QTableWidgetItem(str(entry["id"])))
            self.password_table.setItem(row_index, 1, QTableWidgetItem(entry["website"]))
            self.password_table.setItem(row_index, 2, QTableWidgetItem(entry["email"]))

            # Mask password initially, store real password in UserRole
            password_item = QTableWidgetItem("********")
            password_item.setData(Qt.ItemDataRole.UserRole, entry["password"])
            password_item.setFlags(password_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.password_table.setItem(row_index, 3, password_item)

            # Copy button
            copy_button = QPushButton("Copy")
            copy_button.setCursor(Qt.PointingHandCursor)
            copy_button.clicked.connect(lambda _, row=row_index: self.copy_to_clipboard(row))
            self.password_table.setCellWidget(row_index, 4, copy_button)

            # Delete button
            delete_button = QPushButton("Delete")
            delete_button.setCursor(Qt.PointingHandCursor)
            delete_button.clicked.connect(lambda _, entry_id=entry['id']: self.delete_entry(entry_id))
            self.password_table.setCellWidget(row_index, 5, delete_button)

        self.page_label.setText(f"Page {self.page + 1}")  # Update page label

    def next_page(self):
        """Go to the next page."""
        self.page += 1
        self.load_passwords()

    def prev_page(self):
        """Go to the previous page."""
        if self.page > 0:
            self.page -= 1
            self.load_passwords()

    def reveal_password(self, row, column):
        """Reveal the password when clicking on its cell."""
        if column == 3:
            item = self.password_table.item(row, column)
            real_password = item.data(Qt.ItemDataRole.UserRole)
            item.setText(real_password)  # Show the real password
            self.password_table.resizeColumnToContents(3)

    def copy_to_clipboard(self, row):
        """Copy password to clipboard."""
        item = self.password_table.item(row, 3)
        if item:
            password = item.data(Qt.ItemDataRole.UserRole)
            QGuiApplication.clipboard().setText(password)

    def delete_entry(self, entry_id):
        """Delete a password entry after confirmation."""
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.db_manager.delete_password(entry_id)
            self.load_passwords()  # Refresh table after deletion
