# Dusre modules se functions import kiye
from account import create_account, authenticate_user
from transactions import check_balance, deposit_money, withdraw_money, bank_statement
from loan import check_loan_eligibility

def main_menu(acc_no):
    while True:  # Jab tak user logout na kare, menu bar bar chalega
        print("\n==============================")
        print("    BANKING MANAGEMENT SYSTEM ")
        print("==============================")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Bank Statement")
        print("5. Credit Score & Loan Eligibility")
        print("6. Logout")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            check_balance(acc_no)
        elif choice == '2':
            deposit_money(acc_no)
        elif choice == '3':
            withdraw_money(acc_no)
        elif choice == '4':
            bank_statement(acc_no)
        elif choice == '5':
            check_loan_eligibility(acc_no)
        elif choice == '6':
            print("\nLogged out successfully.")
            break  # Loop khatam kar ke user ko main menu par bhej dega
        else:
            print("Invalid choice! Please select between 1 and 6.")

def main():
    while True:  # Main entry loop
        print("\n==============================")
        print("      WELCOME TO BANK         ")
        print("==============================")
        print("1. Create New Account")
        print("2. Login to Account")
        print("3. Exit Program")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            create_account()  # Account creation function call kiya
        elif choice == '2':
            acc_no = authenticate_user()  # Login function call kiya
            if acc_no:
                main_menu(acc_no)  # Agar login successful ho toh internal menu khola
        elif choice == '3':
            print("\nThank you for using Banking Management System. Goodbye!")
            break  # Program close kar diya
        else:
            print("Invalid choice! Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()  # Program yahin se start hota hai
