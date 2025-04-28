# Import required cryptography modules
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class EncryptionManager:
    """
    EncryptionManager handles encryption and decryption of sensitive user data
    based on a master password.
    """

    def __init__(self, password: str, salt: bytes):
        """
        Initialize the encryption manager with a derived key.
        The key is generated from the user's master password and a fixed salt.
        """
        self.password = password
        self.key = self._derive_key(password, salt)
        self.fernet = Fernet(self.key)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derives a secure key from a password using PBKDF2 and SHA256.

        Args:
            password (str): The master password entered by the user.
            salt (bytes): A static salt for additional security (can be customized later).

        Returns:
            bytes: The derived encryption key.
        """
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
        """
        Encrypts the given plain text.

        Args:
            plain_text (str): The text to encrypt.

        Returns:
            str: The encrypted text, encoded as a string.
        """
        return self.fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        """
        Decrypts the given encrypted text.

        Args:
            cipher_text (str): The encrypted text (stored as a string).

        Returns:
            str: The decrypted plain text if successful, otherwise None.
        """
        try:
            # Important: Database stores ciphertext as string, Fernet expects bytes
            decrypted = self.fernet.decrypt(cipher_text.encode())
            return decrypted.decode()
        except Exception:
            return None  # Explicitly return None on decryption failure
