import pytest; from app.core.encryption import EncryptionService
def test_roundtrip():
    s = EncryptionService(); t = "9988776655"; enc = s.encrypt(t)
    assert enc != t; assert s.decrypt(enc) == t
def test_hash():
    s = EncryptionService(); assert s.hash_for_lookup(" 9988776655 ") == s.hash_for_lookup("9988776655")
