from cryptography.fernet import Fernet
import os

# Генерируем ключ один раз и сохраняем его в файл
def generate_key():
    return Fernet.generate_key()

# Загружаем ключ из файла, если он существует
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            return key_file.read()
    else:
        # Если файл не найден, генерируем новый ключ и сохраняем его в файл
        key = generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

# Шифруем пароль
def encrypt_password(password, key):
    return Fernet(key).encrypt(password.encode()).decode()

# Дешифруем пароль
def decrypt_password(encrypted_password, key):
    return Fernet(key).decrypt(encrypted_password.encode()).decode()
