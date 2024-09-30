from project import User, Flashcard, USER_DATA_FILE, DECKS_DATA_FILE
import pytest


VALID_USERNAME = "valid_username"
VALID_NAME = "Lam Chi Hao"
VALID_EMAIL = "valid_email@gmail.com"
VALID_FRONT = "vietnam"
VALID_BACK = "hanoi"


def test_invalid_name():
    with pytest.raises(ValueError, match="Invalid name"):
        User(VALID_USERNAME, "Lam Chi 123", VALID_EMAIL)
        User(VALID_USERNAME, "", VALID_EMAIL)
        User(VALID_USERNAME, "@Hao !Lam", VALID_EMAIL)
        User(VALID_USERNAME, VALID_EMAIL, VALID_EMAIL)


def test_invalid_username():
    with pytest.raises(ValueError, match="Invalid username"):
        User("hao lam", VALID_NAME, VALID_EMAIL)
        User("", VALID_NAME, VALID_EMAIL)
        User(VALID_EMAIL, VALID_NAME, VALID_EMAIL)


def test_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        User(VALID_USERNAME, VALID_NAME, "@gmail.com")
        User(VALID_USERNAME, VALID_NAME, "valid_email@@gmail.com")
        User(VALID_USERNAME, VALID_NAME, "invalid email@gmail.com")
        User(VALID_USERNAME, VALID_NAME, "valid_email@.com")


def test_valid_user():
    user = User(VALID_USERNAME, VALID_NAME, VALID_EMAIL)
    assert user.username == VALID_USERNAME
    assert user.name == VALID_NAME
    assert user.email == VALID_EMAIL


def test_invalid_flashcard():
    with pytest.raises(ValueError, match="Invalid blank"):
        Flashcard("", VALID_BACK)
        Flashcard(VALID_FRONT, "")
        Flashcard("", "")


def test_valid_flashcard():
    flashcard = Flashcard(VALID_FRONT, VALID_BACK)
    assert flashcard.front == VALID_FRONT
    assert flashcard.back == VALID_BACK


def test_invalid_flashcard_save():
    flashcard = Flashcard(VALID_FRONT, VALID_BACK)
    with pytest.raises(ValueError, match="Invalid deck name"):
        flashcard.save("")
        flashcard.save(USER_DATA_FILE)
        flashcard.save(DECKS_DATA_FILE)
