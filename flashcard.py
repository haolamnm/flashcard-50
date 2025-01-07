from csv import DictWriter
from constants import (
    USER_DATA_FILE,
	DECKS_DATA_FILE,
)


class Flashcard:
    def __init__(self, front: str, back: str) -> None:
        self.front = front
        self.back = back

    def __str__(self) -> str:
        return f"{self.front}: {self.back}"

    @property
    def front(self) -> str:
        return self._front

    @front.setter
    def front(self, front: str) -> None:
        front = front.strip().lower()
        if not front:
            raise ValueError("Invalid blank")
        self._front = front

    @property
    def back(self) -> str:
        return self._back

    @back.setter
    def back(self, back: str) -> None:
        back = back.strip().lower()
        if not back:
            raise ValueError("Invalid blank")
        self._back = back

    def save(self, filename: str) -> None:
        filename = filename.strip().lower()
        if (
            not filename
            or filename == USER_DATA_FILE.removesuffix(".csv")
            or filename == DECKS_DATA_FILE.removesuffix(".csv")
        ):
            raise ValueError("Invalid deck name")

        with open(f"{filename}.csv", "a", newline="") as file:
            writer = DictWriter(file, fieldnames=["front", "back"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "front": self.front,
                    "back": self.back,
                }
            )


if __name__ == '__main__':
	pass
