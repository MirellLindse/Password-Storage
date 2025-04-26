import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class EncryptionManager:
    def __init__(self, password: str, salt: bytes = b"some_hardcoded_salt_123"):
        self.key = self._derive_key(password, salt)
        self.fernet = Fernet(self.key)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Creates a key from a password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, plain_text: str) -> str:
        return self.fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        try:
            # Важно: cipher_text в базе уже хранится как строка, а Fernet требует байты
            decrypted = self.fernet.decrypt(cipher_text.encode())
            return decrypted.decode()
        except Exception:
            return None  # Вместо "" чтобы явно видеть ошибку
