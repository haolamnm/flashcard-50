from re import match
from csv import DictWriter
from validator_collection import checkers
from constants import USER_DATA_FILE


class User:
    def __init__(self, username: str, name: str, email: str) -> None:
        self.username = username
        self.name = name
        self.email = email

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        username = username.strip().lower()
        if not username or " " in username or checkers.is_email(username):
            raise ValueError("Invalid username")
        self._username = username

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        name = name.strip().title()
        if not name or not match(r"^[A-Za-z .,]+$", name):
            raise ValueError("Invalid name")
        self._name = name

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        email = email.strip().lower()
        if not checkers.is_email(email):
            raise ValueError("Invalid email")
        self._email = email

    def save(self) -> None:
        with open(USER_DATA_FILE, "w", newline="") as file:
            writer = DictWriter(file, fieldnames=["username", "name", "email"])
            writer.writeheader()
            writer.writerow(
                {
                    "username": self.username,
                    "name": self.name,
                    "email": self.email,
                }
            )


if __name__ == '__main__':
    pass
