import base64, hashlib, hmac, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import settings

class EncryptionService:
    def __init__(self):
        key_bytes = base64.b64decode(settings.ENCRYPTION_KEY)
        if len(key_bytes) != 32: raise ValueError("ENCRYPTION_KEY must be 32-byte base64")
        self.aesgcm = AESGCM(key_bytes); self.hmac_key = key_bytes

    def encrypt(self, plaintext: str) -> str:
        if not plaintext: return ""
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode(), None)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        if not encrypted_data: return ""
        try:
            raw = base64.b64decode(encrypted_data)
            decrypted = self.aesgcm.decrypt(raw[:12], raw[12:], None)
            return decrypted.decode('utf-8')
        except: return "[DECRYPTION_FAILED]"

    def hash_for_lookup(self, value: str) -> str:
        if not value: return ""
        return hmac.new(self.hmac_key, value.strip().encode(), hashlib.sha256).hexdigest()

encryption_service = EncryptionService()
