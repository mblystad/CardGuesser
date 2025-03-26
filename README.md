# 🧙‍♂️ MTG Tribe Guesser 🧙‍♀️  
A web-based Magic: The Gathering guessing game —  with Comic Sans and chaotic goblin energy.

## ✨ What is this?

This is a silly, flavorful guessing game built with Flask. You're given a **mechanic-based hint**, and your task is to guess the **Magic: The Gathering creature tribe**. Get it right, and you'll be rewarded with:

- A **random tribal creature card** pulled from Scryfall
- A background color based on the card's color
- A bold **"Congratulations"** in full Comic Sans glory
- A running counter of how many correct guesses you've made

Get it wrong? Well, you’ll get roasted a little... but in a fun way.

---

## 🎮 How to Play

1. Run the server:
    ```bash
    python server.py
    ```
2. Open your browser and go to `http://127.0.0.1:5000`
3. Read the **mechanic hint**
4. Type in the tribe you think it matches
5. Hit **Guess**
6. Bask in your glory or try again

---


## 🛠 Requirements

- Python 3.x
- Flask
- `requests` library

You can install dependencies via:

```bash
pip install flask requests
