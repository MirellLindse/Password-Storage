# Import necessary modules
import os
import sqlite3
import ctypes  # Used to hide the folder on Windows
from encryption import EncryptionManager

class DatabaseManager:
    """
    Class responsible for managing all database operations,
    including saving, loading, and deleting passwords.
    """

    def __init__(self, master_password):
        super().__init__()
        self.master_password = master_password  # EncryptionManager instance

        # Path to LocalAppData\PSAGA
        self.app_folder = os.path.join(os.getenv('LOCALAPPDATA'), "PSAGA")

        # Create the folder if it doesn't exist
        if not os.path.exists(self.app_folder):
            os.makedirs(self.app_folder)
            if os.name == 'nt':  # Hide the folder on Windows
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ctypes.windll.kernel32.SetFileAttributesW(self.app_folder, FILE_ATTRIBUTE_HIDDEN)

        # Full path to the database file
        self.db_path = os.path.join(self.app_folder, "passwords.db")

        # Connect to the SQLite database
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

        salt = self.load_salt()
        if not salt:
            salt = os.urandom(16)
            self.save_salt(salt)

        self.crypto = EncryptionManager(self.master_password, salt)

    def create_table(self):
        """
        Create the passwords table if it doesn't already exist.
        """
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                website TEXT NOT NULL,
                email TEXT NOT NULL,
                nickname TEXT,
                password TEXT NOT NULL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                salt BLOB    
            )   
        """)
        self.conn.commit()


    def save_salt(self, salt: bytes):
        """"Saves salt to DB"""
        self.conn.execute("DELETE FROM settings") #Deletes old salt
        self.conn.execute("INSERT INTO settings (salt) values (?)", (salt,))
        self.conn.commit()

    def load_salt(self) -> bytes:
        """Loads salt from database"""
        cursor = self.conn.execute("SELECT salt FROM settings LIMIT 1")
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def save_password(self, website, email, nickname, password):
        """
        Encrypt the email, nickname, and password, and save them to the database.
        """
        encrypted_email = self.crypto.encrypt(email)
        encrypted_password = self.crypto.encrypt(password)
        encrypted_nickname = self.crypto.encrypt(nickname)

        self.conn.execute(
            "INSERT INTO passwords (website, email, nickname, password) VALUES (?, ?, ?, ?)",
            (website, encrypted_email, encrypted_nickname, encrypted_password)
        )
        self.conn.commit()

    def get_all_passwords(self, offset=0, limit=5):
        """
        Retrieve all passwords from the database, decrypting sensitive fields.
        Supports pagination with OFFSET and LIMIT.
        """
        query = "SELECT id, website, email, nickname, password FROM passwords LIMIT ? OFFSET ?"
        cursor = self.conn.execute(query, (limit, offset))
        return [{
            'id': row[0],
            'website': row[1],
            'email': self.crypto.decrypt(row[2]),   # Decrypt email
            'nickname': self.crypto.decrypt(row[3]),  # Decrypt nickname
            'password': self.crypto.decrypt(row[4])  # Decrypt password
        } for row in cursor]

    def delete_password(self, entry_id):
        """
        Delete a password entry from the database by ID.
        """
        self.conn.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        self.conn.commit()
