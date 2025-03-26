import random
import difflib
from flask import Flask, request, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = 'a-secret-key'  # Needed for sessions to work
counter = 0

tribes = [
    "goblin", "elf", "vampire", "merfolk", "dragon", "zombie", "angel", "wizard",
    "sliver", "human", "soldier", "spirit", "elemental", "demon", "beast", "cat",
    "construct", "knight", "treefolk", "giant"
]

tribe_mechanics = {
    "goblin": "Haste",
    "elf": "Mana Ramp",
    "vampire": "Lifelink",
    "merfolk": "Islandwalk",
    "dragon": "Flying",
    "zombie": "Graveyard Recursion",
    "angel": "Flying",
    "wizard": "Prowess",
    "sliver": "Shared Abilities",
    "human": "Versatility",
    "soldier": "Go-Wide",
    "spirit": "Evasion",
    "elemental": "Triggered Abilities",
    "demon": "High Risk/High Reward",
    "beast": "Powerful Vanilla Creatures",
    "cat": "Exalted",
    "construct": "Artifact Synergy",
    "knight": "First Strike",
    "treefolk": "Toughness Matters",
    "giant": "Cost Reduction"
}

description = ["not ohio", "unslay", "nerfed", "simp", "non-sigma"]

def get_random_card_image_url(tribe):
    url = f"https://api.scryfall.com/cards/search?q=t:{tribe}+type:creature"
    response = requests.get(url)
    data = response.json()

    if 'data' in data and data['data']:
        random_card = random.choice(data['data'])
        image_url = random_card['image_uris']['normal'] if 'image_uris' in random_card else None
        colors = random_card.get('colors', [])
        return image_url, colors
    return None, []

@app.route('/')
def home():
    session["chosen_tribe"] = random.choice(tribes)
    chosen = session["chosen_tribe"]
    hint = tribe_mechanics.get(chosen, "Mystery")
    print(f"🔍 The tribe to guess is: {chosen}")

    return f'''
    <body style="font-family:'Comic Sans MS', cursive; text-align:center; margin-top:50px;">
        <h1>Guess the Magic: The Gathering tribe!</h1>
        <h2>Here is a simple hint: {hint}</h2>
        <form action="/guess" method="post" style="margin-top:20px;">
            <input type="text" name="tribe" placeholder="Enter a tribe" style="padding:10px; font-size:16px;">
            <button type="submit" style="padding:10px 15px; font-size:16px; margin-left:10px;">Guess</button>
        </form>
    </body>
    '''

@app.route('/guess', methods=['POST'])
def guess():
    user_tribe = request.form['tribe'].strip().lower()
    chosen_tribe = session.get('chosen_tribe', None)

    if not chosen_tribe:
        return redirect(url_for('home'))

    matches = difflib.get_close_matches(user_tribe, tribes, n=1, cutoff=0.7)

    if matches and matches[0] == chosen_tribe:
        global counter
        counter += 1
        image_url, colors = get_random_card_image_url(chosen_tribe)

        color_hex = {
            'W': '#f8f3e3',
            'U': '#cce2ff',
            'B': '#2f2f2f',
            'R': '#ffcccc',
            'G': '#d7f5d3'
        }

        bg_color = color_hex.get(colors[0], '#ffffff') if colors else '#ffffff'

        return f'''
        <body style="background-color:{bg_color}; font-family:'Comic Sans MS', cursive; text-align:center; margin-top:50px;">
            <h1 style="font-size:45px; font-weight:bold;">
                Congratulations!<br>I was thinking of the {matches[0]}s. But no matter what I am thinking of, goblins own my heart.
            </h1>
            <img src="{image_url}" alt="MTG Card">
            <br><br>
            <form action="/" method="get">
                <button type="submit" style="font-size: 18px; padding: 10px 15px;">Play Again, you have {counter} correct guesses now.</button>
            </form>
        </body>
        '''
    else:
        corrected = matches[0] if matches else user_tribe
        return f'''
        <body style="font-family:'Comic Sans MS', cursive; text-align:center; margin-top:50px;">
            <h2>That was a good guess, but I do not like the {corrected} tribe.<br>
            Everyone knows they are {random.choice(description)} 😞.</h2>
            <form action="/" method="get">
                <button type="submit" style="font-size: 18px; padding: 10px 15px;">Try Again</button>
            </form>
        </body>
        '''

if __name__ == "__main__":
    app.run(debug=True)
