from database import load_data, save_data  # Database se data load aur save karne wale functions import kiye
from datetime import datetime             # Loan transaction ka exact date aur time record karne ke liye

def check_loan_eligibility(acc_no):
    acc_no = str(acc_no).strip()          # Account number ko string format mein convert kar ke extra spaces khatam kiye
    data = load_data()                    # JSON database file se tamam accounts ka data load kiya
    
    # Safe check ke yeh account number database mein mojood hai ya nahi
    if acc_no not in data["accounts"]:
        print("\n[Error] Account record not found!")     # Agar account na mile toh error message dikhaya
        input("\nPress Enter to return to menu...")      # User ke Enter dabane tak screen ko roka
        return                                           # Function yahin khatam kar ke wapas menu par bhej diya

    acc = data["accounts"][acc_no]                       # Logged-in user ke account ka record nikala
    score = int(acc.get("credit_score", 650))            # User ka credit score liya (default 650 agar missing ho)
    balance = float(acc.get("balance", 0.0))             # User ka current balance float format mein liya

    print("\n==========================================")  # Header line print ki
    print("     CREDIT SCORE & LOAN ELIGIBILITY      ")  # Title print kiya
    print("==========================================")  # Header closing line print ki
    print(f"Account Holder   : {acc['name']}")           # Account holder ka naam print kiya
    print(f"Your Credit Score: {score} / 850")           # User ka credit score 850 mein se print kiya
    print(f"Current Balance  : ${balance:.2f}")          # Current balance 2 decimal places ke sath print kiya
    print("-" * 42)                                      # Divider line print ki

    # Credit score aur account balance ki buniyad par loan tier aur maximum limit calculate ki
    if score >= 750:                                     # Agar credit score 750 ya us se zyada ho
        tier = "Excellent"                               # Rating Excellent set ki
        max_loan = balance * 10 if balance > 0 else 5000.0  # Balance ka 10 guna ya minimum $5000 loan limit
    elif score >= 650:                                   # Agar credit score 650 se 749 ke darmiyan ho
        tier = "Good"                                    # Rating Good set ki
        max_loan = balance * 5 if balance > 0 else 2500.0   # Balance ka 5 guna ya minimum $2500 loan limit
    elif score >= 550:                                   # Agar credit score 550 se 649 ke darmiyan ho
        tier = "Fair"                                    # Rating Fair set ki
        max_loan = balance * 2 if balance > 0 else 1000.0   # Balance ka 2 guna ya minimum $1000 loan limit
    else:                                                # Agar credit score 550 se kam ho
        tier = "Poor"                                    # Rating Poor set ki
        max_loan = 0.0                                   # Koi loan nahi mil sakta

    print(f"Credit Rating    : {tier}")                  # Credit rating (Excellent/Good/Fair/Poor) print ki
    if max_loan > 0:                                     # Agar user loan ke liye eligible hai (limit > 0)
        print(f"Max Eligible Loan: ${max_loan:.2f}")     # Maximum loan ki raqam print ki
        print("==========================================")
        
        # User se pucha ke kya woh abhi loan lena (avail karna) chahta hai
        apply = input("\nDo you want to avail/take a loan right now? (y/n): ").strip().lower()
        if apply == 'y':                                 # Agar user 'y' (yes) enter kare
            try:                                         # Invalid text input se bachne ke liye try block lagaya
                loan_amount = float(input(f"Enter loan amount (Max ${max_loan:.2f}): $"))  # Loan amount input li
                if 0 < loan_amount <= max_loan:          # Check kiya ke amount 0 se zyada aur max limit ke andar ho
                    acc["balance"] = balance + loan_amount  # Loan ki raqam user ke account balance mein jama kar di
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Mojooda date aur time hasil kiya
                    
                    if "transactions" not in acc:        # Agar transactions list pehle se mojood na ho
                        acc["transactions"] = []         # Toh nayi empty list bana di
                        
                    # Bank statement ke liye loan transaction ka record add kiya
                    acc["transactions"].append({
                        "type": "Loan Credit",           # Transaction ki qisam
                        "amount": loan_amount,           # Loan ki raqam
                        "balance_after": acc["balance"], # Loan ke baad naya balance
                        "time": timestamp                # Transaction ka waqt
                    })
                    save_data(data)                      # Naya balance aur transaction JSON file mein save kar di
                    print(f"\nCongratulations! Loan of ${loan_amount:.2f} credited to your account.")
                    print(f"New Balance: ${acc['balance']:.2f}")  # Updated balance screen par dikhaya
                else:                                    # Agar raqam 0 se kam ya limit se zyada ho
                    print(f"\n[Error] Invalid amount! Please enter between $1 and ${max_loan:.2f}.")
            except ValueError:                           # Agar user number ke bajaye text (abc) likh de
                print("\n[Error] Please enter a valid number.")
    else:                                                # Agar user ka score bohat kam ho aur loan na mil sake
        print("Status           : Not eligible for a loan right now.")
        print("==========================================")

    input("\nPress Enter to return to menu...")          # Screen ko rokay rakha jab tak user Enter na dabaye