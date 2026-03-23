import pytest
from app.core.encryption import encrypt, decrypt, hash_for_lookup

def test_encrypt_decrypt_roundtrip():
    """Test that encrypting and then decrypting returns the original string"""
    original = "Hello, World! 123"
    encrypted = encrypt(original)
    decrypted = decrypt(encrypted)
    assert decrypted == original

def test_encrypt_empty_string():
    """Test that encrypting an empty string returns an empty string"""
    assert encrypt("") == ""
    assert decrypt("") == ""

def test_hash_for_lookup_deterministic():
    """Test that hash_for_lookup produces the same output for the same input"""
    value = "9876543210"
    hash1 = hash_for_lookup(value)
    hash2 = hash_for_lookup(value)
    assert hash1 == hash2
    # Should be a 64-character hex string (SHA256)
    assert len(hash1) == 64
    assert all(c in '0123456789abcdef' for c in hash1)

def test_hash_for_lookup_different_inputs():
    """Test that different inputs produce different hashes"""
    value1 = "9876543210"
    value2 = "9876543211"
    hash1 = hash_for_lookup(value1)
    hash2 = hash_for_lookup(value2)
    assert hash1 != hash2
