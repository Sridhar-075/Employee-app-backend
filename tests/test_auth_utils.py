from auth.utils import hash_password, verify_password
import pytest

# def test_verify_password_accepts_correct_password():
#     hashed = hash_password("secret123")
#     assert verify_password("secret123", hashed) is True


# def test_verify_password_rejects_wrong_password():
#     hashed = hash_password("secret123")
#     assert verify_password("wrong-pass", hashed) is False


# def test_verify_password_rejects_empty_string():
#     hashed = hash_password("secret123")
#     assert verify_password("", hashed) is False

@pytest.fixture
def hashed_password():
    return hash_password("secret123")

def test_correct_password(hashed_password):
    assert verify_password("secret123",hashed_password) is True

def test_verify_password_rejects_wrong_password(hashed_password):
    assert verify_password("wrong",hashed_password) is False

def test_verify_password_rejects_empty_password(hashed_password):
    assert verify_password("",hashed_password) is False