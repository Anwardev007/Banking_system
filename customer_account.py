class BaseAccount:
    def __init__(self, fname, lname, address, account_no, balance):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.account_no = account_no
        self.balance = float(balance)



class BankCustomer(BaseAccount):
    def __init__(self, fname, lname, address, account_no, balance):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.account_no = account_no
        self.balance = float(balance)
        
    
    def update_first_name(self, fname):
        self.fname = fname
    
    def update_last_name(self, lname):
        self.lname = lname
                
    def get_first_name(self):
        return self.fname
    
    def get_last_name(self):
        return self.lname
        
    def update_address(self, addr):
        self.address = addr
        
    def get_address(self):
        return self.address
    
    def deposit(self, amount):

        # Prevent invalid deposits
        if amount <= 0:
            print("Deposit amount must be greater than zero!")
            return False

        # Add money
        self.balance += amount

        print(f"{amount} deposited successfully")

        return True
        
    def withdraw(self, amount):

        # ------------------------
        # INVALID AMOUNT
        # ------------------------
        if amount <= 0:
            print("Invalid amount!")
            return False

        # ------------------------
        # INSUFFICIENT BALANCE
        # ------------------------
        if amount > self.balance:
            print("Account balance insufficient!")
            return False

        # ------------------------
        # SUCCESS
        # ------------------------
        self.balance -= amount

        print(f"{amount} withdrawn successfully")

        return True
        
    def print_balance(self):
        print("\n The account balance is %.2f" %self.balance)
        
    def get_balance(self):
        return self.balance
    
    def get_account_no(self):
        return self.account_no
    
    def account_menu(self):
        print ("\n Your Transaction Options Are:")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Deposit money")
        print ("2) Withdraw money")
        print ("3) Check balance")
        print ("4) Update customer name")
        print ("5) Update customer address")
        print ("6) Show customer details")
        print ("7) Back")
        print (" ")
        option = int(input ("Choose your option: "))
        return option
    
    def print_details(self):
        print("\n--- Customer Details ---")
        print("First name:", self.fname)
        print("Last name:", self.lname)
        print("Account No:", self.account_no)
        print("Address:", " ".join(self.address))
        print("Balance:", self.balance)

    def get_details(self):
        return f"""
    Name: {self.fname} {self.lname}
    Account No: {self.account_no}
    Address: {' '.join(self.address)}
    Balance: {self.balance}
    """

    def run_account_options(self):
        loop = 1
        while loop == 1:
            choice = self.account_menu()
            if choice == 1:
                amount = float(input("\n Enter amount to deposit: "))
                self.deposit(amount)
                self.print_balance()
            elif choice == 2:
                #ToDo
                pass
            elif choice == 3:
                #STEP A.4.4
                pass
            elif choice == 4:
                #STEP A.4.2
                pass
            elif choice == 5:
                #ToDo
                pass
            elif choice == 6:
                self.print_details()
            elif choice == 7:
                loop = 0
        print ("\n Exit account operations")


class SavingsAccount(BankCustomer):
    def __init__(self, fname, lname, address, account_no, balance, interest_rate=0.02):
        super().__init__(fname, lname, address, account_no, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        return self.balance * self.interest_rate


class AdvancedAccount(BankCustomer):
    def __init__(self, fname, lname, address, account_no, balance, overdraft_limit=500):
        super().__init__(fname, lname, address, account_no, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):

        if amount <= 0:
            print("Amount must be greater than zero!")
            return False

        # Allow overdraft
        if self.balance + self.overdraft < amount:
            print("Overdraft limit exceeded!")
            return False

        self.balance -= amount
        print(f"{amount} withdrawn successfully")

        return True