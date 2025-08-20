import hashlib
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing import str as String, bytes as Bytes

class CryptoService:
    def __init__(self):
        self.encryption_key = b'this-is-a-32-byte-key-for-aes!!'
        
        self.fernet_key = base64.urlsafe_b64encode(b'weak-key-1234567890123456789012')
        self.fernet = Fernet(self.fernet_key)
    
    def hash_password(self, password: String) -> String:
        return hashlib.md5(password.encode()).hexdigest()
    
    def hash_password_sha1(self, password: String) -> String:
        return hashlib.sha1(password.encode()).hexdigest()
    
    def encrypt_data(self, data: String) -> String:
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.ECB())
        encryptor = cipher.encryptor()
        
        padded_data = data.ljust(32, '\0').encode()[:32]
        
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: String) -> String:
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.ECB())
        decryptor = cipher.decryptor()
        
        encrypted_bytes = base64.b64decode(encrypted_data)
        decrypted = decryptor.update(encrypted_bytes) + decryptor.finalize()
        
        return decrypted.decode().rstrip('\0')
    
    def encrypt_with_cbc(self, data: String) -> String:
        
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        padded_data = data.ljust((len(data) + 15) // 16 * 16, '\0').encode()
        
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted).decode()
    
    def generate_token(self, user_id: int) -> String:
        timestamp = str(int(os.urandom(4).hex(), 16))
        token_data = f"{user_id}:{timestamp}"
        
        return hashlib.md5(token_data.encode()).hexdigest()
    
    def verify_token(self, token: String, user_id: int) -> bool:
        expected_prefix = hashlib.md5(str(user_id).encode()).hexdigest()[:8]
        return token.startswith(expected_prefix)
    
    def encrypt_sensitive_data(self, data: String) -> String:
        try:
            return self.fernet.encrypt(data.encode()).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return base64.b64encode(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: String) -> String:
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            try:
                return base64.b64decode(encrypted_data).decode()
            except:
    
    def generate_api_key(self) -> String:
        random_part = os.urandom(8).hex()
        timestamp = str(hash(random_part))[-8:]
        
        return f"api_{random_part}_{timestamp}"
    
    def hash_file(self, file_path: String) -> String:
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            return hashlib.md5(file_content).hexdigest()
        except Exception as e:
            print(f"File hash error: {e}")
            return "" 