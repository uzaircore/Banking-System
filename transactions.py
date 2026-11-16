from database import load_data, save_data
from datetime import datetime

def check_balance(acc_no):
    acc_no = str(acc_no).strip()  # Ensure string format
    data = load_data()
    
    if acc_no not in data["accounts"]:
        print("\n[Error] Account record not found!")
        input("\nPress Enter to return to menu...")
        return

    acc = data["accounts"][acc_no]
    print("\n==============================")
    print("       BALANCE INQUIRY        ")
    print("==============================")
    print(f"Account Number : {acc_no}")
    print(f"Account Holder : {acc['name']}")
    print(f"Current Balance: ${acc['balance']:.2f}")
    print("==============================")
    input("\nPress Enter to return to menu...")  # Screen ko rokne ke liye

def deposit_money(acc_no):
    acc_no = str(acc_no).strip()
    print("\n--- DEPOSIT MONEY ---")
    try:
        amount = float(input("Enter amount to deposit: $"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            input("\nPress Enter to return to menu...")
            return
        
        data = load_data()
        acc = data["accounts"][acc_no]
        acc["balance"] += amount
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "transactions" not in acc:
            acc["transactions"] = []

        acc["transactions"].append({
            "type": "Deposit",
            "amount": amount,
            "balance_after": acc["balance"],
            "time": timestamp
        })
        
        save_data(data)
        print(f"\nSuccessfully deposited ${amount:.2f}.")
        print(f"New Balance: ${acc['balance']:.2f}")
    except ValueError:
        print("Invalid input! Please enter a valid number.")
    
    input("\nPress Enter to return to menu...")

def withdraw_money(acc_no):
    acc_no = str(acc_no).strip()
    print("\n--- WITHDRAW MONEY ---")
    try:
        amount = float(input("Enter amount to withdraw: $"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            input("\nPress Enter to return to menu...")
            return

        data = load_data()
        acc = data["accounts"][acc_no]

        if amount > acc["balance"]:
            print(f"\nInsufficient balance! Current balance is ${acc['balance']:.2f}")
            input("\nPress Enter to return to menu...")
            return

        acc["balance"] -= amount
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "transactions" not in acc:
            acc["transactions"] = []

        acc["transactions"].append({
            "type": "Withdrawal",
            "amount": amount,
            "balance_after": acc["balance"],
            "time": timestamp
        })

        if acc.get("credit_score", 650) < 850:
            acc["credit_score"] = min(850, acc.get("credit_score", 650) + 2)

        save_data(data)
        print(f"\nSuccessfully withdrew ${amount:.2f}.")
        print(f"Remaining Balance: ${acc['balance']:.2f}")
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        
    input("\nPress Enter to return to menu...")

def bank_statement(acc_no):
    acc_no = str(acc_no).strip()
    data = load_data()
    
    if acc_no not in data["accounts"]:
        print("\n[Error] Account record not found!")
        input("\nPress Enter to return to menu...")
        return

    acc = data["accounts"][acc_no]
    print("\n============================================================")
    print("                       BANK STATEMENT                       ")
    print("============================================================")
    print(f"Account Number : {acc_no}")
    print(f"Account Holder : {acc['name']}")
    print(f"Current Balance: ${acc['balance']:.2f}")
    print("-" * 60)
    
    transactions = acc.get("transactions", [])
    if not transactions:
        print("No transactions found yet.")
    else:
        print(f"{'Date & Time':<20} | {'Type':<12} | {'Amount':<10} | {'Balance':<10}")
        print("-" * 60)
        for tx in transactions:
            print(f"{tx['time']:<20} | {tx['type']:<12} | ${tx['amount']:<9.2f} | ${tx['balance_after']:<9.2f}")
    print("============================================================")
    input("\nPress Enter to return to menu...")  # Screen ko rokne ke liye