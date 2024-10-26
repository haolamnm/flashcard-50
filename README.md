
# CS50P Flashcard Project

This is a flashcard learning web app created to enable users in creating, managing, and studying flashcards. It uses the Streamlit-driven user-friendly interface to create flashcard decks, add cards to or remove them from decks, and study a deck of cards. Also, the user will be able to upload/download flashcard decks in order to share and keep them for personal use. Students who want to improve their learning by means of digital flashcards will also be able to do it with the help of this web appapp.



## Authors
- [@haolamnm](https://github.com/haolamnm)

My name is Lâm Chí Hào, a student at Vietnam National University in Ho Chi Minh City, University of Science (VNUHCM-US). Since I have some knowledge in coding before, this is my learning CS50P timeline

| Date       | Work               |
| ---------- | ------------------- |
| 16/09/2024 | Week 0              |
| 17/09/2024 | Week 1              |
| 18/09/2024 | Week 2              |
| 19/09/2024 | Week 3              |
| 20/09/2024 | Week 4 and Week 5   |
| 21/09/2024 | Week 6              |
| 22/09/2024 | Week 7              |
| 23/09/2024 | Week 8              |
| 24/09/2024 | Week 9              |
| 25/09/2024 | Start Final Project |

## Final Project Diary
**25/09/2024**: I started to skim through the CS50P Project Gallery for inspiration and stumbled upon a command line-based flashcard project. It inspired me, finally, to do my flashcard project with an additional functionality: downloading or uploading flashcard decks. On this day, the core logic was outlined, and its initial implementation was done using loops in the terminal environment.

**26/09/2024**: Since the school online meetings via Zoom, I wasn't able to work too much, but today, I did find out about the `Streamlit` library, which helps me create a GUI for my project instead of the terminal environment and started fiddling with it regarding my project.

**27/09/2024**: I had to refactor my project for the most part in order to integrate it with the GUI of `Streamlit`. It required replacing lots of the original loop-based logic to fit the GUI model. After about 6 hours of coding - from 12 AM to 6 PM - I was able to get the basic GUI up, fix bugs, and do quite a bit of reading of the `Streamlit` documentation to get the functionality I wanted.

**28/09/2024**: My focus was on further improvements, bug fixing of the learning functionality, adding a bit more new features, refining code: writing type hints and docstrings for each of the functions.

**29/09/2024**: I wrote unit tests for the `User` and `Flashcard` classes, created a `requirements.txt` file, and started drafting the `README.md`. I had also outlined the structure for my demo video.

**30/09/2024**: Today was supposed to be my first day at VNUHCM-US, but my teacher isn't felling well. With this unexpected free time, I'm focusing on my project.  I plan to finalize the download and upload functionalities, complete the `README.md` file, fulfill my demo video script, polish the code and push it all to GitHub.

**01/10/2024**: Today, I recored my demo video, upload it to YouTube, submit to CS50P.

## Final Project Documentation

### Classes

The two main classes in my project are `User` and `Flashcard`. Each class is designed to handle and validate user inputs.

Here is how the `Flashcard.front` property is validated.

```python
@property
def front(self) -> str:
    return self._front

@front.setter
def front(self, front: str) -> None:
    front = front.strip().lower()
    if not front:
        raise ValueError("Invalid blank")
    self._front = front
```

For the `User` class, the `username` is validated as follows:

```python
@property
def username(self) -> str:
    return self._username

@username.setter
def username(self, username: str) -> None:
    username = username.strip().lower()
    if not username or " " in username or checkers.is_email(username):
        raise ValueError("Invalid username")
    self._username = username
```
So, other things like `Flashcard.back`, `User.name`, `User.email` are just similar but have a different logic.  Another method I create for both the class is `save()`. The User class's `save()` method is relatively straightforward. However, the Flashcard class's `save()` method is more complex due to its additional argument.

```python
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
```

### Global Variables

Here, I verify whether it's the user's first time running the app by checking the existence of two CSV files:

```python
# Global Variables
USER_DATA_FILE = "user_data.csv"
DECKS_DATA_FILE = "decks_data.csv"
```

So just to be clear `decks_data.csv` will store all the created deck names, and its created dates. While `user_data.csv` will store the user data.

### Main function

The first part of `main()` function checks if this is the first time a user is visiting the web app; if so, it creates two files:

```python
def main():
    # SETUP
    if not check_decks_data_exist():
        setup_decks_data()
    if not check_user_data_exist():
        setup_user_data()
    else:
        ... # GUI part
```

The following function checks if deck data exists: (The other one `check_user_data_exist()` is just similar)

```python
def check_decks_data_exist() -> bool:
    try:
        with open(DECKS_DATA_FILE, "r", newline=""):
            return True
    except FileNotFoundError:
        return False
```

When the function identifies a person as a first-time visitor, it runs a block of code where the program gathers information of the user such as name, username, and email of the user. Then store it into `user_data.csv`. (maybe in the furture I will implement some kind of reminder to learn sending through the user email)

```python
def setup_user_data() -> None:
    with st.form("REGISTRATION"):
        name = st.text_input(...)
        username = st.text_input(...)
        email = st.text_input(...)
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
```

So I decide that user can chane their information after registration. Through this function:

```python
def update_user_data() -> None:
    with open(USER_DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for user in reader:
            current_user = {
                "username": user["username"],
                "name": user["name"],
                "email": user["email"],
            }
    new_username = st.text_input(...)
    new_name = st.text_input(...)
    new_email = st.text_input(...)
    if st.button("Update"):
        try:
            new_user = User(new_username, new_name, new_email)
            new_user.save()
            st.success("Update user information successfully!")
            time.sleep(0.5)
            st.rerun()
        except ValueError as E:
            st.error(E)
```

### Add function:

```python
def add_section() -> None
    with st.form("ADD CARD"):
        filename = st.text_input(...)
        front = st.text_input(...)
        back = st.text_input(...)
        submit_button = st.form_submit_button("Add")

        if submit_button:
            try:
                card = Flashcard(front, back)
                card.save(filename)
                if check_deck_name_exist(filename):
                    with open(DECKS_DATA_FILE, "a", newline="") as file:
                        writer = csv.DictWriter(
                            file, fieldnames=["deck_name", "created_date"]
                        )
                        writer.writerow(
                            {"deck_name": filename, "created_date": date.today()}
                        )
                st.success("Card saved successfully!")
                time.sleep(0.5)
                st.rerun()
            except ValueError as E:
                st.error(E)

```

Users can input the deck names and the text of the flashcards. The program will store this information in a comma-separated values file. Flashcards are stored in a deck file while the deck names are stored in the `decks_data.csv`.

### Remove Function

```python
def remove_section(filepath: str) -> None:
    ...
```

If there are no decks, then it warns the user. Also, in case of an empty deck, the system warns the user. Users can either delete the entire deck or only remove the cards inside it. The removal of a card simply rewrites the CSV file, excluding the selected card, while deck deletion removes the file and its name from `decks_data.csv`.

### Learning Function

```python
def learn_deck(filepath: str) -> None:
    ...
```

The learning section is the major feature of the project. In order to manage the flow of the learning, I used `st.session_state`. It was really time-consuming to implement.

### Downloading / Uploading Function

```python
def download_deck(filepath: str) -> None:
    ...

def upload_deck() -> None:
    ...
```

When downloaded, it exports the selected deck as a CSV file with the flashcard data in it. In uploading, it is providing a facility for the user to choose a CSV file to upload a deck into the system, and the app will validate the format and integrate it into the existing collection.

### Other Functions

Beside that, there are also a lot more function that I create to support the program or provide more visualization.

For example, `list_deck()` will lay the foundation for me to implement recently created deck view.

```python
def list_deck() -> list[dict]:
        reader = csv.DictReader(file)
        for deck in reader:
            if deck["deck_name"].strip() == USER_DATA_FILE.removesuffix(".csv") or deck[
                "deck_name"
            ].strip() == DECKS_DATA_FILE.removesuffix(".csv"):
                continue
            else:
                decks.append(deck)
    return decks
```

Or `choose_deck_name()` will help on avoiding repeated code:
```python
def choose_deck_name(decks_name: list[str], key: str) -> str:
    filename = st.selectbox(
        label="Choose deck:",
        options=decks_name,
        key=key,
    )
    filepath = f"{filename}.csv"
    return filepath
```


## Demo Video
[YouTube](https://www.youtube.com/watch?v=Q8IJsduPAsE)

To run the project
```
>>> streamlit run project.py
```
