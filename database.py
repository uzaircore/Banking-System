import json    # JSON data ko parhnay aur likhnay ke liye library import ki
import os      # File ka wajood check karne ke liye operating system library import ki

DB_FILE = "bank_accounts_db.json"  # Nayi database file taake purana plain-text data masla na kare

def load_data():
    # Agar database file mojood nahi hai, toh aik empty dictionary return karein
    if not os.path.exists(DB_FILE):
        return {"accounts": {}}
    try:
        # File ko read mode mein kholen aur JSON data load karein
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Agar file corrupt ya khali ho toh safe empty structure return karein
        return {"accounts": {}}

def save_data(data):
    # Data ko JSON format mein file ke andar write/save karein
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)