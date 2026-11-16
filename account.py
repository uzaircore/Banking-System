import random                  # Random 10-digit account number generate karne ke liye
import hashlib                 # Password hashing (SHA-256) ke liye built-in library
from database import load_data, save_data  # Database functions import kiye

def hash_password(password):
    # Plain password ko bytes mein convert kar ke SHA-256 encrypted hash banaya
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_account():
    print("\n--- CREATE NEW ACCOUNT ---")
    name = input("Enter Full Name: ").strip()  # User se naam liya
    if not name:
        print("Name cannot be empty!")
        input("\nPress Enter to continue...")
        return

    cnic = input("Enter CNIC (must be exactly 13 digits without dashes): ").strip()  # CNIC input liya
    if not cnic.isdigit() or len(cnic) != 13:  # Check kiya ke CNIC 13 digits ka hi ho
        print("Invalid CNIC! It must be exactly 13 digits.")
        input("\nPress Enter to continue...")
        return

    password = input("Set a Password: ").strip()  # Plain password input liya
    if not password:
        print("Password cannot be empty!")
        input("\nPress Enter to continue...")
        return

    # Plain password ko SHA-256 hash mein convert kiya
    hashed_password = hash_password(password)

    # 10 digits ka random account number generate kiya
    account_number = str(random.randint(1000000000, 9999999999))

    data = load_data()  # Database load kiya
    
    # Check kiya ke kya yeh CNIC pehle se registered hai
    for acc in data["accounts"].values():
        if acc["cnic"] == cnic:
            print("An account with this CNIC already exists!")
            input("\nPress Enter to continue...")
            return

    # Naye account mein plain password ki jagah 'hashed_password' save kiya
    data["accounts"][account_number] = {
        "name": name,
        "cnic": cnic,
        "password": hashed_password,
        "balance": 0.0,
        "credit_score": 650,
        "transactions": []
    }

    save_data(data)  # Updated data ko JSON file mein save kiya
    print("\n==========================================")
    print("       ACCOUNT CREATED SUCCESSFULLY!      ")
    print("==========================================")
    print(f"Account Number  : {account_number}")
    print(f"Encrypted Hash  : {hashed_password[:25]}... (SHA-256)")
    print("Please note this Account Number for login.")
    print("==========================================")
    input("\nPress Enter to continue...")

def authenticate_user():
    print("\n--- USER LOGIN ---")
    acc_no = input("Enter Account Number: ").strip()  # Account number liya
    password = input("Enter Password: ").strip()      # Password input liya

    # User ke enter kiye gaye password ko bhi SHA-256 hash mein convert kiya
    hashed_input_password = hash_password(password)

    data = load_data()
    if acc_no in data["accounts"]:
        acc = data["accounts"][acc_no]
        # Database mein mojood hash aur user ke input hash ko match kiya
        if acc["password"] == hashed_input_password:
            print(f"\nLogin Successful! Welcome, {acc['name']}.")
            return acc_no
        else:
            print("\n[Error] Incorrect Password!")
    else:
        print("\n[Error] Account Number not found!")
    
    input("\nPress Enter to continue...")
    return None