import json
from customer_account import BankCustomer, SavingsAccount, AdvancedAccount
from admin import BankAdmin
import os

accounts_list = []
admins_list = []

class BankSystem(object):
    def __init__(self):
        self.accounts_list = []
        self.admins_list = []
        self.load_bank_data()
    
    def load_bank_data(self):
        """
        Load customers from file OR fallback to default data
        """

        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

            DATA_FILE = os.path.join(BASE_DIR, "data.json")

            with open(DATA_FILE, "w") as file:
                data = json.load(file)

                if len(data) > 0:
                    for c in data:
                        account_type = c.get("account_type", "BankCustomer")

                        if account_type == "SavingsAccount":

                            customer = SavingsAccount(
                                c["fname"],
                                c["lname"],
                                c["address"],
                                c["account_no"],
                                c["balance"]
                            )

                        elif account_type == "AdvancedAccount":

                            customer = AdvancedAccount(
                                c["fname"],
                                c["lname"],
                                c["address"],
                                c["account_no"],
                                c["balance"]
                            )

                        else:

                            customer = BankCustomer(
                                c["fname"],
                                c["lname"],
                                c["address"],
                                c["account_no"],
                                c["balance"]
                            )
                        self.accounts_list.append(customer)
                else:
                    self.create_default_data()

        except:
            # File does not exist → create default
            self.create_default_data()

        # Always create admins (not stored in file)
        self.create_admins()

    def create_default_data(self):
        account_no = 1234


        self.accounts_list.append(
            SavingsAccount("Adam", "Smith", ["14", "Wilcot Street", "Bath", "B5 5RT"], account_no, 5000.00)
        )
        account_no += 1

        self.accounts_list.append(
            AdvancedAccount("David", "White", ["60", "Holborn Viaduct", "London", "EC1A 2FD"], account_no, 3200.00)
        )
        account_no += 1

        self.accounts_list.append(BankCustomer("Alice", "Churchil", ["5", "Cardigan Street", "Birmingham", "B4 7BD"], account_no, 18000.00))
        account_no += 1

        self.accounts_list.append(BankCustomer("Ali", "Abdallah", ["44", "Churchill Way West", "Basingstoke", "RG21 6YR"], account_no, 40.00))


    def create_admins(self):
        self.admins_list.append(BankAdmin("id1122", "1234", True, "Julian", "Padget", ["12", "London Road", "Birmingham", "B95 7TT"]))
        self.admins_list.append(BankAdmin("id2244", "4567", False, "Cathy", "Newman", ["47", "Mars Street", "Newcastle", "NE12 6TZ"]))


    def search_admins_by_name(self, admin_username):
        found_admin = None
        for a in self.admins_list:
            if a.get_username() == admin_username:
                found_admin = a
                break

        if found_admin == None:
            print("\n Admin not found!")
            
        return found_admin 
        
    def search_customers_by_name(self, customer_lname):
        found_customer = None
        
        for c in self.accounts_list:
            if c.get_last_name().lower() == customer_lname.lower():
                found_customer = c
                break

        if found_customer == None:
            print("\n Customer not found!")

        return found_customer

    def management_report(self):
        total_customers = len(self.accounts_list)
        total_balance = 0
        total_overdraft = 0
        total_interest = 0

        for acc in self.accounts_list:
            total_balance += acc.get_balance()

            # overdraft
            if hasattr(acc, "overdraft"):
                if acc.get_balance() < 0:
                    total_overdraft += abs(acc.get_balance())

            # interest
            if hasattr(acc, "calculate_interest"):
                total_interest += acc.calculate_interest()

        return total_customers, total_balance, total_overdraft, total_interest


    def main_menu(self):
        #print the options you have
        print()
        print()
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("Welcome to the Python Bank System")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Admin login")
        print ("2) Quit Python Bank System")
        print (" ")
        option = int(input ("Choose your option: "))
        return option


    def run_main_options(self):
        loop = 1         
        while loop == 1:
            choice = self.main_menu()
            if choice == 1:
                username = input ("\n Please input admin username: ")
                password = input ("\n Please input admin password: ")
                msg, admin_obj = self.admin_login(username, password)
                print(msg)
                if admin_obj != None:
                    self.run_admin_options(admin_obj)
            elif choice == 2:
                loop = 0
        print ("\n Thank-You for stopping by the bank!")


    def transferMoney(self, sender_lname, receiver_lname,
                    receiver_account_no, amount):
        print("sender last name", sender_lname)
        print("reciver last name", receiver_lname)

        sender = None
        receiver = None

        # Find sender
        for acc in self.accounts_list:
            if acc.get_last_name().lower() == sender_lname.lower():
                sender = acc
                print("sender",sender)
                break

        # Find receiver
        for acc in self.accounts_list:
            if (acc.get_last_name().lower() == receiver_lname.lower()
                    and str(acc.get_account_no()) == str(receiver_account_no)):
                receiver = acc
                print("receiver", receiver)
                break

        # Prevent same account transfer
        if (sender.get_account_no() == receiver.get_account_no()):
            return False, "Sender and receiver cannot be the same account"

        # Sender validation
        if sender is None:
            return False, "Sender not found"

        # Receiver validation
        if receiver is None:
            return False, "User not found"
        
        if sender == receiver:
            return False, "Sender and receiver cannot be the same account"

        # Amount validation
        if amount <= 0:
            return False, "Amount must be greater than zero"

        # Withdraw from sender
        success = sender.withdraw(amount)
        print(success)

        if not success:
            return False, "Account balance insufficient"

        # Deposit to receiver
        receiver.deposit(amount)

        # Save data
        self.save_data()

        return True, "Transfer completed successfully"

                
    def admin_login(self, username, password):

        # Search for admin
        found_admin = self.search_admins_by_name(username)

        # Username does not exist
        if found_admin is None:
            return "Admin user does not exist!", None

        # Wrong password
        if found_admin.get_password() != password:
            return "Incorrect password!", None

        # Success
        return "Login successful!", found_admin

    def admin_menu(self, admin_obj):
        #print the options you have
         print (" ")
         print ("Welcome Admin %s %s : Avilable options are:" %(admin_obj.get_first_name(), admin_obj.get_last_name()))
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Transfer money")
         print ("2) Customer account operations & profile settings")
         print ("3) Delete customer")
         print ("4) Print all customers detail")
         print ("5) Sign out")
         print ("6) Management Report")
         print (" ")
         option = int(input ("Choose your option: "))
         return option

    def save_data(self):
        """
        Save all customer accounts to JSON file
        """

        data = []

        for c in self.accounts_list:
            customer_dict = {
                "fname": c.get_first_name(),
                "lname": c.get_last_name(),
                "address": c.get_address(),
                "account_no": c.get_account_no(),
                "balance": c.get_balance(),
                "account_type": type(c).__name__
            }
            data.append(customer_dict)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
            
    def generate_account_number(self):
        if not self.accounts_list:
            return 1000
        return max([c.get_account_no() for c in self.accounts_list]) + 1


    def create_customer(self, fname, lname, address, acc_type):
        account_no = self.generate_account_number()

        if acc_type == "savings":
            from customer_account import SavingsAccount
            customer = SavingsAccount(fname, lname, address, account_no, 0)

        elif acc_type == "advanced":
            from customer_account import AdvancedAccount
            customer = AdvancedAccount(fname, lname, address, account_no, 0)

        else:
            from customer_account import BankCustomer
            customer = BankCustomer(fname, lname, address, account_no, 0)

        self.accounts_list.append(customer)
        self.save_data()
    
    
    def run_admin_options(self, admin_obj):
        """
        This function handles all admin menu operations.
        It keeps looping until admin chooses to sign out.
        """
        loop = 1

        while loop == 1:
            # Show admin menu and get choice
            choice = self.admin_menu(admin_obj)

            # ===============================
            # OPTION 1: Transfer Money
            # ===============================
            if choice == 1:
                sender_lname = input("\n Please input sender surname: ")
                amount = float(input("\n Please input the amount to be transferred: "))
                receiver_lname = input("\n Please input receiver surname: ")
                receiver_account_no = input("\n Please input receiver account number: ")

                self.transferMoney(sender_lname, receiver_lname, receiver_account_no, amount)

            # ===========================================
            # OPTION 2: Customer Account Operations
            # ===========================================
            elif choice == 2:
                customer_name = input("\n Please input customer surname: ")
                customer_account = self.search_customers_by_name(customer_name)

                if customer_account != None:
                    # Call customer menu (deposit, withdraw, etc.)
                    customer_account.run_account_options()

            # ===========================================
            # OPTION 3: Delete Customer (TODO next step)
            # ===========================================
            elif choice == 3:
                # Check admin permission
                if admin_obj.has_full_admin_right():

                    customer_name = input("\n Enter customer surname to delete: ")
                    customer_account = self.search_customers_by_name(customer_name)

                    if customer_account != None:
                        self.accounts_list.remove(customer_account)
                        self.save_data()
                        print("Customer account deleted successfully!")

                else:
                    print("You do NOT have permission to delete accounts!")

            # ===========================================
            # OPTION 4: Print All Customers
            # ===========================================
            elif choice == 4:
                print("\n All Customers Details:")
                for customer in self.accounts_list:
                    customer.print_details()

            # ===========================================
            # OPTION 5: Sign Out
            # ===========================================
            elif choice == 5:
                loop = 0
            # ===========================================
            # OPTION 6: Management Report
            # ===========================================

            elif choice == 6:
                self.management_report()

            else:
                print("Invalid option! Try again.")

        print("\n Exit admin menu")




if __name__ == "__main__":
    app = BankSystem()
    app.run_main_options()
