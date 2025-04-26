import sqlite3
from encryption import EncryptionManager

class DatabaseManager:
    def __init__(self, crypto_manager):
        self.conn = sqlite3.connect("passwords.db")
        self.crypto = crypto_manager
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                website TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def save_password(self, website, email, password):
        encrypted = self.crypto.encrypt(password)
        self.conn.execute(
            "INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)",
            (website, email, encrypted)
        )
        self.conn.commit()

    def get_all_passwords(self, offset=0, limit=5):
        query = "SELECT id, website, email, password FROM passwords LIMIT ? OFFSET ?"
        cursor = self.conn.execute(query, (limit, offset))
        return [{
            'id': row[0],
            'website': row[1],
            'email': row[2],
            'password': self.crypto.decrypt(row[3])
        } for row in cursor]

    def delete_password(self, entry_id):
        self.conn.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        self.conn.commit()
