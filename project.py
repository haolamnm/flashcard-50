import streamlit as st
import csv
from validator_collection import checkers
import re
import os
import pandas as pd
from datetime import date
import time


# GLOBAL
USER_DATA_FILE = "user_data.csv"
DECKS_DATA_FILE = "decks_data.csv"
INCORRECT_ANS_DELAY = 1.5
CORRECT_ANS_DELAY = 0.5


# INTIAL SETUP
def setup_page():
    st.set_page_config(
        page_title="CS50P PROJECT",
        page_icon="🎩",
    )
    st.title("CS50P Flashcards Project")


# USER CLASS
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
        if not name or not re.match(r"^[A-Za-z .,]+$", name):
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
            writer = csv.DictWriter(file, fieldnames=["username", "name", "email"])
            writer.writeheader()
            writer.writerow(
                {
                    "username": self.username,
                    "name": self.name,
                    "email": self.email,
                }
            )


# FLASHCARD CLASS
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
            writer = csv.DictWriter(file, fieldnames=["front", "back"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "front": self.front,
                    "back": self.back,
                }
            )


def main():
    # SETUP
    setup_page()
    if not check_decks_data_exist():
        setup_decks_data()
    if not check_user_data_exist():
        setup_user_data()

    # MAIN
    else:
        settings_popover()
        st.markdown("---")
        st.header("CONFIG SECTION")
        col1, col2 = st.columns(2)
        decks = list_deck()
        decks_name = list_deck_name(decks)
        with col1:
            tab1, tab2, tab3, tab4 = st.tabs(["ADD", "REMOVE", "DOWNLOAD", "UPLOAD"])
            with tab1:
                add_section()
            with tab2:
                with st.container(border=True):
                    filepath_to_remove = choose_deck_name(decks_name, "deck_to_remove")
                    remove_section(filepath_to_remove)
            with tab3:
                with st.container(border=True):
                    filepath_to_download = choose_deck_name(decks_name, "deck_to_download")
                    download_deck(filepath_to_download)
            with tab4:
                with st.container(border=True):
                    upload_deck()
        with col2:
            lastest_decks_df = pd.DataFrame(decks[-10:])
            lastest_decks_df = lastest_decks_df.rename(
                columns={"deck_name": "Deck name", "created_date": "Created date"}
            )
            lastest_decks_df = lastest_decks_df.reset_index(drop=True)
            st.table(lastest_decks_df)

        st.markdown("---")
        st.header("LEARNING SECTION")
        with st.container(border=True):
            filepath_to_learn = choose_deck_name(decks_name, "deck_to_learn")

            if filepath_to_learn:
                learn_deck(filepath_to_learn)


def settings_popover() -> None:
    with st.popover("SETTINGS"):
        tab1, tab2 = st.tabs(["ABOUT", "USER"])
        with tab1:
            st.markdown(
                "This is a CS50P project that allows you to create and manage flashcards. "
                "You can create new decks, add cards, remove and review them interactively. "
                "[GitHub](https://github.com/haolamnm/CS50P-project). "
                "[LinkedIn](https://www.linkedin.com/in/haolamnm/). "
            )
        with tab2:
            st.write("Edit user information")
            update_user_data()
            USER_DATA_DF = pd.read_csv(USER_DATA_FILE)
            st.table(USER_DATA_DF)


def update_user_data() -> None:
    """
    Allows user to update user's information

    Return:
        None
    """
    with open(USER_DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for user in reader:
            current_user = {
                "username": user["username"],
                "name": user["name"],
                "email": user["email"],
            }
    new_username = st.text_input(
        label="New username",
        value=current_user["username"],
        key="new_username",
        placeholder=f"{current_user["username"]}",
    )
    new_name = st.text_input(
        label="New name",
        value=current_user["name"],
        key="new_name",
        placeholder=f"{current_user["name"]}",
    )
    new_email = st.text_input(
        label="New email",
        value=current_user["email"],
        key="new_email",
        placeholder=f"{current_user["email"]}",
    )
    if st.button("Update"):
        try:
            new_user = User(new_username, new_name, new_email)
            new_user.save()
            st.success("Update user information successfully!")
            time.sleep(0.5)
            st.rerun()
        except ValueError as E:
            st.error(E)


def check_user_data_exist() -> bool:
    """
    Checks if the user_data.csv file exist.

    Return:
        True if the file exist, False otherwise.
    """
    try:
        with open(USER_DATA_FILE, "r", newline=""):
            return True
    except FileNotFoundError:
        return False


def check_decks_data_exist() -> bool:
    """
    Checks if the decks_data.csv file exist.

    Return:
        True if the file exist, False otherwise.
    """
    try:
        with open(DECKS_DATA_FILE, "r", newline=""):
            return True
    except FileNotFoundError:
        return False


def check_deck_name_exist(filename: str) -> bool:
    """
    Checks if a deck with the given filename exist in the decks_data.csv file.

    Args:
        filename: The filename to check.

    Return:
        True if a deck with the given filename exists, False otherwise.
    """
    with open(DECKS_DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["deck_name"].strip() == filename:
                return True
    return False


def setup_user_data() -> None:
    """
    Creates a user registration form using Streamlit and save it to user_data.csv upon submission.

    Return:
        None
    """
    with st.form("REGISTRATION"):
        name = st.text_input(
            label="Name:",
            value="",
            key="name",
            placeholder="Lam Chi Hao",
        )
        username = st.text_input(
            label="Username:",
            value="",
            key="username",
            placeholder="haolamm",
        )
        email = st.text_input(
            label="Email:",
            value="",
            key="email",
            placeholder="__@gmail.com",
        )
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            try:
                user = User(username, name, email)
                user.save()
                st.success("User data saved successfully!")
                time.sleep(0.5)
                st.rerun()
            except ValueError as E:
                st.error(E)


def setup_decks_data() -> None:
    """
    Creates decks_data.csv file with needed entries

    Return:
        None
    """
    with open(DECKS_DATA_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["deck_name", "created_date"])
        writer.writeheader()
        writer.writerow(
            {
                "deck_name": "decks_data",
                "created_date": date.today(),
            }
        )
        writer.writerow(
            {
                "deck_name": "user_data",
                "created_date": date.today(),
            }
        )


def add_section() -> None:
    """
    Creates a card addition form using Streamlit and saves a new card upon submission.

    This function allows users to enter deck name, card front and back content.
    If the deck doesn't exist, a new deck entry is created in decks_data.csv.

    Return:
        None
    """
    with st.form("ADD CARD"):
        filename = st.text_input(
            label="Deck name:",
            value="",
            key="filename",
            placeholder="capitals",
            max_chars=30,
        )
        front = st.text_input(
            label="Front:",
            value="",
            key="front",
            placeholder="vietnam",
        )
        back = st.text_input(
            label="Back:",
            value="",
            key="back",
            placeholder="hanoi"
        )
        submit_button = st.form_submit_button("Add")

        if submit_button:
            try:
                card = Flashcard(front, back)
                card.save(filename)
                if not check_deck_name_exist(filename):
                    with open(DECKS_DATA_FILE, "a", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=["deck_name", "created_date"])
                        writer.writerow(
                            {"deck_name": filename, "created_date": date.today()}
                        )
                st.success("Card saved successfully!")
                time.sleep(0.5)
                st.rerun()
            except ValueError as E:
                st.error(E)


def remove_section(filepath: str) -> None:
    """
    Removes a selected card or deck.

    Args:
        filepath: The .csv filepath leads to selected deck.

    Return:
        None
    """
    cards_name = list_card_name(filepath)
    if st.button("Remove deck"):
        filename = filepath.removesuffix(".csv")

        temp_decks = []

        with open(DECKS_DATA_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for deck in reader:
                if deck["deck_name"].strip() != filename:
                    temp_decks.append(deck)

        with open(DECKS_DATA_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["deck_name", "created_date"])
            writer.writeheader()
            writer.writerows(temp_decks)

        os.remove(filepath)
        st.success(f"Deck {filename} removed successfully")
        time.sleep(0.5)
        st.rerun()

    if cards_name:
        rm_card = st.selectbox(
            label="Choose card:",
            options=cards_name,
            key="cardname_toremove",
        )

        if st.button("Remove card"):
            temp_cards = []

            with open(filepath, "r", newline="") as file:
                reader = csv.DictReader(file)
                for card in reader:
                    card_info = f"{card['front']} - {card['back']}"
                    if card_info != rm_card:
                        temp_cards.append(card)

            with open(filepath, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["front", "back"])
                writer.writeheader()
                writer.writerows(temp_cards)

            st.success(f"Card {rm_card} removed successfully")
            time.sleep(0.5)
            st.rerun()
    else:
        st.warning("Empty deck")


def list_deck() -> list[dict]:
    """
    Lists all decks information excluding user_data.csv and decks_data.csv.

    Return:
        A list of decks
    """
    decks = []
    with open(DECKS_DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for deck in reader:
            if deck["deck_name"].strip() == USER_DATA_FILE.removesuffix(".csv") or deck[
                "deck_name"
            ].strip() == DECKS_DATA_FILE.removesuffix(".csv"):
                continue
            else:
                decks.append(deck)
    return decks


def list_deck_name(decks: list[dict]) -> list[str]:
    """
    Extracts deck name from a list of decks.

    Args:
        decks: A list of decks.

    Return:
        A list of deck names.
    """
    decks_name = []
    for deck in decks:
        decks_name.append(deck["deck_name"])
    return decks_name


def list_card_name(filepath: str) -> list[str]:
    """
    Lists card names from a given deck

    Args:
        filepath: The .csv filepath leads to selected deck.

    Return:
        A list of card names of selected deck.
    """
    cards_name = []
    try:
        with open(filepath, "r", newline="") as file:
            reader = csv.DictReader(file)
            for card in reader:
                cards_name.append(f"{card["front"]} - {card["back"]}")
    except FileNotFoundError:
        st.warning("No deck to remove")

    return cards_name


def choose_deck_name(decks_name: list[str], key: str) -> str:
    """
    Allows user to choose a deck from a list of available decks

    Args:
        decks_name: A list of deck names.
        key: A unique key for Steamlit select box.

    Return:
        The filepath of the selected deck.
    """
    filename = st.selectbox(
        label="Choose deck:",
        options=decks_name,
        key=key,
    )
    filepath = f"{filename}.csv"
    return filepath


def learn_deck(filepath: str) -> None:
    """
    Learning session for a selected deck.

    Present flashcard one by one.
    Keeps track of the score.

    Args:
        filepath: The .csv filepath that leads to selected deck.

    Return:
        None
    """
    if "current_card" not in st.session_state:
        st.session_state.current_card = 0

    if (
        "current_filepath" not in st.session_state
        or st.session_state.current_filepath != filepath
    ):
        st.session_state.current_card = 0
        st.session_state.current_filepath = filepath

    try:
        with open(filepath, "r", newline="") as file:
            deck = list(csv.DictReader(file))
            total_cards = len(deck)
            if total_cards == 0:
                raise ValueError("Empty deck")

            current_card = deck[st.session_state.current_card]

            with st.form(f"{st.session_state.current_card}"):
                answer = st.text_input(
                    label=f"{current_card["front"]}",
                    value="",
                    placeholder="answer here ...",
                )
                submit_button = st.form_submit_button("Submit")

                if submit_button:
                    answer = answer.strip().lower()
                    if answer == current_card["back"]:
                        st.success("Correct")
                        time.sleep(CORRECT_ANS_DELAY)
                    else:
                        st.error(f"Incorrect, answer is {current_card["back"]}")
                        time.sleep(INCORRECT_ANS_DELAY)

                    if st.session_state.current_card < total_cards - 1:
                        st.session_state.current_card += 1
                    st.rerun()

        if st.session_state.current_card + 1 == total_cards:
            st.warning("Final card in deck, press Reset to start over.")

        if st.button("Reset"):
            st.session_state.current_card = 0
            st.rerun()

    except FileNotFoundError:
        st.warning("No deck to learn")
    except ValueError as E:
        st.warning(E)


def download_deck(filepath: str) -> None:
    """
    Allows users to download their decks

    Args:
        filepath: The .csv filepath that leads to selected deck.

    Return:
        None
    """
    try:
        with open(filepath, "r", newline="") as file:
            download_button_clicked = st.download_button(
                label="Download",
                data=file,
                file_name=filepath,
                mime="text/csv",
            )
            if download_button_clicked:
                st.success("Download successfully")
                time.sleep(1.5)
                st.rerun()
    except FileNotFoundError:
        st.warning("No deck to download")


def upload_deck() -> None:
    """
    Allows user to upload their card

    Return:
        None
    """
    uploaded_file = st.file_uploader("Upload your deck")

    if uploaded_file:
        filename = os.path.splitext(uploaded_file.name)[0]
        uploaded_file_df = pd.read_csv(uploaded_file)

        if not check_deck_name_exist(filename):
            filepath = f"{filename}.csv"
            uploaded_file_df.to_csv(filepath, index=False)
            with open(DECKS_DATA_FILE, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["deck_name", "created_date"])
                writer.writerow(
                    {"deck_name": filename, "created_date": date.today()}
                )
            st.success("Upload successfully")
            time.sleep(1.5)
            st.rerun()
        else:
            st.warning("Invalid deck name")


if __name__ == "__main__":
    main()
