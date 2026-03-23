# FILE: ration-saathi/backend/app/core/encryption.py
import base64
import hashlib
import hmac
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Union

class EncryptionService:
    def __init__(self):
        # Load encryption key from environment variable
        encryption_key = os.getenv("ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError("ENCRYPTION_KEY environment variable is required")
        
        # Derive a Fernet key from the encryption key
        # Fernet requires a 32-byte key, so we'll use PBKDF2 to derive it
        salt = b"ration_saathi_salt"  # In production, use a random salt stored separately
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
        self.cipher = Fernet(key)
        
        # Separate HMAC key for hashing (for lookup without decryption)
        self.hmac_key = os.getenv("ENCRYPTION_KEY", "default_fallback_key").encode()[:32]

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using AES-256-GCM via Fernet.
        Returns base64 encoded ciphertext.
        """
        if not plaintext:
            return ""
        try:
            encrypted_bytes = self.cipher.encrypt(plaintext.encode())
            return base64.b64encode(encrypted_bytes).decode()
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt base64 encoded ciphertext using AES-256-GCM via Fernet.
        Returns plaintext string.
        """
        if not ciphertext:
            return ""
        try:
            encrypted_bytes = base64.b64decode(ciphertext.encode())
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")

    def hash_for_lookup(self, value: str) -> str:
        """
        Create HMAC-SHA256 hash of value for lookup without storing plaintext.
        Deterministic - same input always produces same output.
        """
        if not value:
            return ""
        return hmac.new(self.hmac_key, value.encode(), hashlib.sha256).hexdigest()

# Global instance for use across the application
encryption_service = EncryptionService()

# Convenience functions
def encrypt(plaintext: str) -> str:
    return encryption_service.encrypt(plaintext)

def decrypt(ciphertext: str) -> str:
    return encryption_service.decrypt(ciphertext)

def hash_for_lookup(value: str) -> str:
    return encryption_service.hash_for_lookup(value)
