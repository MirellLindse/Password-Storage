import sqlite3
from encryption import encrypt_password, decrypt_password, load_key

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("passwords.db")
        self.key = load_key()
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
        if not hasattr(self, 'key'):
            self.key = load_key()
        encrypted = encrypt_password(password, self.key)
        self.conn.execute("INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)",
                          (website, email, encrypted))
        self.conn.commit()

    def get_all_passwords(self, offset=0, limit=5):
        # Добавляем пагинацию через LIMIT и OFFSET
        query = "SELECT id, website, email, password FROM passwords LIMIT ? OFFSET ?"
        cursor = self.conn.execute(query, (limit, offset))

        return [{
            'id': row[0],
            'website': row[1],
            'email': row[2],
            'password': decrypt_password(row[3], self.key)
        } for row in cursor]

    def delete_password(self, entry_id):
        self.conn.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        self.conn.commit()
