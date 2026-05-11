import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from bank_system import BankSystem

app = BankSystem()

# ------------------------
# MODERN FINTECH COLOR THEME
# ------------------------

# Main Colors
PRIMARY = "#4f46e5"       # Indigo
SECONDARY = "#7c3aed"     # Purple
SUCCESS = "#10b981"       # Green
DANGER = "#ef4444"        # Red
WARNING = "#f59e0b"       # Orange

# Backgrounds
BG_COLOR = "#f3f4f6"      # Light gray background
SIDEBAR = "#111827"       # Dark sidebar
CARD = "#ffffff"          # White cards
TOPBAR = "#ffffff"

# Text Colors
TEXT = "#111827"
LIGHT_TEXT = "#6b7280"
WHITE = "#ffffff"

# Border / Inputs
BORDER = "#d1d5db"
INPUT_BG = "#f9fafb"

# Button Hover Colors
PRIMARY_HOVER = "#4338ca"
SUCCESS_HOVER = "#059669"
DANGER_HOVER = "#dc2626"


    # ------------------------
    # CUSTOMER DROPDOWN WINDOW
    # ------------------------
def open_customer_ops():

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("Customer Operations")
    win.geometry("700x900")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Customer Operations",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 30, "bold")).pack(pady=(30, 5))

    tk.Label(win,
             text="Manage deposits and withdrawals",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # MAIN CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=40,
                    pady=35,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=25,
              pady=15,
              fill="x")

    # ------------------------
    # SELECT CUSTOMER
    # ------------------------
    tk.Label(card,
             text="Select Customer",
             bg="white",
             fg=TEXT,
             font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                 pady=(0, 8))

    customer_var = tk.StringVar()

    customer_names = [c.get_last_name() for c in app.accounts_list]

    customer_var.set(customer_names[0])

    dropdown = tk.OptionMenu(card,
                             customer_var,
                             *customer_names)

    dropdown.config(font=("Segoe UI", 12),
                    bg=INPUT_BG,
                    fg=TEXT,
                    width=25,
                    relief="solid",
                    bd=1)

    dropdown.pack(ipady=3,
                  pady=(0, 10))

    # ------------------------
    # BALANCE CARD
    # ------------------------
    balance_frame = tk.Frame(card,
                             bg="#f9fafb",
                             padx=15,
                             pady=12,
                             highlightbackground="#e5e7eb",
                             highlightthickness=1)

    balance_frame.pack(fill="x",
                       pady=5)

    tk.Label(balance_frame,
             text="Current Balance",
             bg="#f9fafb",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    balance_label = tk.Label(balance_frame,
                             text="£0.00",
                             bg="#f9fafb",
                             fg=SUCCESS,
                             font=("Segoe UI", 24, "bold"))

    balance_label.pack(pady=5)

    # ------------------------
    # SHOW BALANCE
    # ------------------------
    def show_balance():

        customer = app.search_customers_by_name(
            customer_var.get()
        )

        if customer:

            balance_label.config(
                text=f"£{customer.get_balance():,.2f}"
            )

    show_balance()

    # ------------------------
    # REFRESH BUTTON
    # ------------------------
    tk.Button(card,
              text="Refresh Balance",
              command=show_balance,
              bg=PRIMARY,
              fg="white",
              activebackground=PRIMARY_HOVER,
              activeforeground="white",
              relief="flat",
              cursor="hand2",
              font=("Segoe UI", 11, "bold"),
              width=22,
              pady=10).pack(pady=10)

    # ------------------------
    # FORM LABEL HELPER
    # ------------------------
    def form_label(text):

        tk.Label(card,
                 text=text,
                 bg="white",
                 fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                     pady=(10, 3))

    # ------------------------
    # DEPOSIT SECTION
    # ------------------------
    form_label("Deposit Amount")

    deposit_entry = tk.Entry(card,
                             font=("Segoe UI", 13),
                             bg=INPUT_BG,
                             fg=TEXT,
                             relief="solid",
                             bd=1)

    deposit_entry.pack(fill="x",
                       ipady=10)

    # ------------------------
    # DEPOSIT FUNCTION
    # ------------------------
    def deposit():

        customer = app.search_customers_by_name(
            customer_var.get()
        )

        try:

            amount = float(deposit_entry.get())

            success = customer.deposit(amount)

            if success:

                app.save_data()

                show_balance()

                deposit_entry.delete(0, tk.END)

                messagebox.showinfo(
                    "Success",
                    "Deposit successful"
                )

            else:

                messagebox.showerror(
                    "Error",
                    "Deposit amount must be greater than zero"
                )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid amount"
            )

    # ------------------------
    # DEPOSIT BUTTON
    # ------------------------
    tk.Button(card,
              text="Deposit Funds",
              bg=SUCCESS,
              fg="white",
              activebackground=SUCCESS_HOVER,
              activeforeground="white",
              relief="flat",
              cursor="hand2",
              font=("Segoe UI", 12, "bold"),
              width=25,
              pady=8,
              command=deposit).pack(pady=5)

    # ------------------------
    # WITHDRAW SECTION
    # ------------------------
    form_label("Withdraw Amount")

    withdraw_entry = tk.Entry(card,
                              font=("Segoe UI", 13),
                              bg=INPUT_BG,
                              fg=TEXT,
                              relief="solid",
                              bd=1)

    withdraw_entry.pack(fill="x",
                        ipady=10)

    # ------------------------
    # WITHDRAW FUNCTION
    # ------------------------
    def withdraw():

        customer = app.search_customers_by_name(
            customer_var.get()
        )

        try:

            amount = float(withdraw_entry.get())

            success, msg = customer.withdraw(amount)

            if success:

                app.save_data()

                show_balance()

                withdraw_entry.delete(0, tk.END)

                messagebox.showinfo(
                    "Success",
                    msg
                )

            else:

                messagebox.showerror(
                    "Error",
                    msg
                )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid amount"
            )

    # ------------------------
    # WITHDRAW BUTTON
    # ------------------------
    tk.Button(card,
              text="Withdraw Funds",
              bg=DANGER,
              fg="white",
              activebackground=DANGER_HOVER,
              activeforeground="white",
              relief="flat",
              cursor="hand2",
              font=("Segoe UI", 12, "bold"),
              width=25,
              pady=8,
              command=withdraw).pack(pady=25)

# ------------------------
# TRANSFER WINDOW
# ------------------------
def open_transfer():

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("Transfer Money")
    win.geometry("650x750")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Transfer Funds",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 28, "bold")).pack(pady=(30, 5))

    tk.Label(win,
             text="Secure bank transfer between customers",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=40,
                    pady=35,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=40,
              pady=30,
              fill="both",
              expand=True)

    # ------------------------
    # CUSTOMER NAMES
    # ------------------------
    names = [c.get_last_name() for c in app.accounts_list]

    # ------------------------
    # HELPER LABEL
    # ------------------------
    def form_label(text):

        tk.Label(card,
                 text=text,
                 bg="white",
                 fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                     pady=(18, 5))

    # ------------------------
    # SENDER
    # ------------------------
    form_label("Sender")

    sender_var = tk.StringVar(value=names[0])

    sender_menu = tk.OptionMenu(card,
                                sender_var,
                                *names)

    sender_menu.config(font=("Segoe UI", 12),
                       bg=INPUT_BG,
                       fg=TEXT,
                       width=25,
                       relief="solid",
                       bd=1)

    sender_menu.pack(ipady=5)

    # ------------------------
    # RECEIVER
    # ------------------------
    form_label("Receiver")

    receiver_var = tk.StringVar(value=names[1])

    receiver_menu = tk.OptionMenu(card,
                                  receiver_var,
                                  *names)

    receiver_menu.config(font=("Segoe UI", 12),
                         bg=INPUT_BG,
                         fg=TEXT,
                         width=25,
                         relief="solid",
                         bd=1)

    receiver_menu.pack(ipady=5)

    # ------------------------
    # ACCOUNT NUMBER
    # ------------------------
    form_label("Receiver Account Number")

    acc_entry = tk.Entry(card,
                         font=("Segoe UI", 13),
                         bg=INPUT_BG,
                         fg=TEXT,
                         relief="solid",
                         bd=1)

    acc_entry.pack(fill="x",
                   ipady=10)

    # ------------------------
    # AMOUNT
    # ------------------------
    form_label("Transfer Amount (£)")

    amount_entry = tk.Entry(card,
                            font=("Segoe UI", 13),
                            bg=INPUT_BG,
                            fg=TEXT,
                            relief="solid",
                            bd=1)

    amount_entry.pack(fill="x",
                      ipady=10)

    # ------------------------
    # TRANSFER FUNCTION
    # ------------------------
    def transfer():

        account_no = acc_entry.get().strip()
        amount_text = amount_entry.get().strip()

        # Validation
        if account_no == "":

            messagebox.showerror(
                "Error",
                "Please enter account number"
            )

            return

        if amount_text == "":

            messagebox.showerror(
                "Error",
                "Please enter amount"
            )

            return

        # Transfer
        try:

            amount = float(amount_text)

            success, msg = app.transferMoney(
                sender_var.get(),
                receiver_var.get(),
                account_no,
                amount
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    msg
                )

                amount_entry.delete(0, tk.END)
                acc_entry.delete(0, tk.END)

            else:
                if msg == "User not found": messagebox.showerror( "User Not Found", "Receiver account number does not exist" )
                elif msg == "Account balance insufficient":
                    messagebox.showerror( "Error", "Account balance insufficient" )
                elif msg == "Sender and receiver cannot be the same account":
                    messagebox.showerror( "Error", "Sender and receiver cannot be the same account" )
                elif msg == "Amount must be greater than zero":
                    messagebox.showerror( "Error", "Please enter valid amount" )
                else:
                    messagebox.showerror( "Error", msg )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid amount"
            )

    # ------------------------
    # BUTTON
    # ------------------------
    tk.Button(card,
              text="Transfer Money",
              command=transfer,
              bg=PRIMARY,
              fg="white",
              activebackground=PRIMARY_HOVER,
              activeforeground="white",
              relief="flat",
              cursor="hand2",
              font=("Segoe UI", 14, "bold"),
              width=25,
              pady=14).pack(pady=40)
    


def show_admin_info(admin):

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("My Profile")
    win.geometry("750x850")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Admin Profile",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 30, "bold")).pack(pady=(30, 5))

    tk.Label(win,
             text="Manage your administrator account",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # PROFILE CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=40,
                    pady=40,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=40,
              pady=30,
              fill="both",
              expand=True)

    # ------------------------
    # PROFILE ICON
    # ------------------------
    tk.Label(card,
             text="👤",
             bg="white",
             fg=PRIMARY,
             font=("Segoe UI", 65)).pack(pady=(0, 10))

    tk.Label(card,
             text=f"{admin.get_first_name()} {admin.get_last_name()}",
             bg="white",
             fg=TEXT,
             font=("Segoe UI", 24, "bold")).pack()

    tk.Label(card,
             text="System Administrator",
             bg="white",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack(pady=(5, 30))

    # ------------------------
    # INFO ROW FUNCTION
    # ------------------------
    def profile_row(title, value):

        row = tk.Frame(card,
                       bg="#f9fafb",
                       padx=20,
                       pady=15,
                       highlightbackground="#e5e7eb",
                       highlightthickness=1)

        row.pack(fill="x",
                 pady=6)

        tk.Label(row,
                 text=title,
                 bg="#f9fafb",
                 fg=LIGHT_TEXT,
                 font=("Segoe UI", 11, "bold")).pack(side="left")

        tk.Label(row,
                 text=value,
                 bg="#f9fafb",
                 fg=TEXT,
                 font=("Segoe UI", 12)).pack(side="right")

    # ------------------------
    # PROFILE DATA
    # ------------------------
    profile_row(
        "Admin ID",
        admin.get_username()
    )

    profile_row(
        "First Name",
        admin.get_first_name()
    )

    profile_row(
        "Last Name",
        admin.get_last_name()
    )

    profile_row(
        "Address",
        " ".join(admin.get_address())
    )

    profile_row(
        "Admin Rights",
        "Full Admin"
        if admin.has_full_admin_right()
        else "Standard Admin"
    )








def update_admin_info(admin):

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("Update Admin Profile")
    win.geometry("700x650")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Update Admin Profile",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 28, "bold")).pack(pady=(25, 5))

    tk.Label(win,
             text="Edit administrator account information",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=25,
                    pady=20,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=30,
              pady=20,
              fill="x")

    # ------------------------
    # PROFILE ICON
    # ------------------------
    tk.Label(card,
             text="👤",
             bg="white",
             fg=PRIMARY,
             font=("Segoe UI", 38)).pack(pady=(0, 8))

    # ------------------------
    # HELPER FUNCTIONS
    # ------------------------
    def styled_label(text):

        tk.Label(card,
                 text=text,
                 bg="white",
                 fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                     pady=(10, 3))

    def styled_entry():

        entry = tk.Entry(card,
                         font=("Segoe UI", 12),
                         bg=INPUT_BG,
                         fg=TEXT,
                         relief="solid",
                         bd=1)

        entry.pack(fill="x",
                   ipady=6)

        return entry

    # ------------------------
    # INPUTS
    # ------------------------
    styled_label("New First Name")
    fname = styled_entry()

    styled_label("New Last Name")
    lname = styled_entry()

    styled_label("New Address")
    addr = styled_entry()

    # ------------------------
    # UPDATE FUNCTION
    # ------------------------
    def update():

        first_name = fname.get().strip()
        last_name = lname.get().strip()
        address = addr.get().strip()

        # Validation
        if first_name == "":

            messagebox.showerror(
                "Error",
                "First name cannot be empty"
            )

            return

        if last_name == "":

            messagebox.showerror(
                "Error",
                "Last name cannot be empty"
            )

            return

        if address == "":

            messagebox.showerror(
                "Error",
                "Address cannot be empty"
            )

            return

        # Update Admin
        admin.update_first_name(first_name)
        admin.update_last_name(last_name)
        admin.update_address(address.split(","))

        messagebox.showinfo(
            "Success",
            "Admin profile updated successfully"
        )

        # Clear fields
        fname.delete(0, tk.END)
        lname.delete(0, tk.END)
        addr.delete(0, tk.END)

    # ------------------------
    # BUTTON
    # ------------------------
    button_frame = tk.Frame(card,
                            bg="white")

    button_frame.pack(pady=20)

    tk.Button(button_frame,
              text="Update Profile",
              bg=PRIMARY,
              fg="white",
              activebackground=PRIMARY_HOVER,
              activeforeground="white",
              relief="flat",
              cursor="hand2",
              font=("Segoe UI", 12, "bold"),
              width=22,
              pady=8,
              command=update).pack()


def print_all_customers():

    win = tk.Toplevel(root)
    win.title("All Customers")
    win.geometry("900x700")
    win.configure(bg=BG_COLOR)

    # Title
    tk.Label(win,
             text="All Customers",
             bg=BG_COLOR,
             fg=TEXT,
             font=("Arial", 28, "bold")).pack(pady=20)

    # Scrollable canvas
    canvas = tk.Canvas(win,
                       bg=BG_COLOR,
                       highlightthickness=0)

    scrollbar = tk.Scrollbar(win,
                             orient="vertical",
                             command=canvas.yview)

    scroll_frame = tk.Frame(canvas,
                            bg=BG_COLOR)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0),
                         window=scroll_frame,
                         anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left",
                fill="both",
                expand=True)

    scrollbar.pack(side="right",
                   fill="y")

    # Customer cards
    for c in app.accounts_list:

        card = tk.Frame(scroll_frame,
                        bg=CARD,
                        padx=20,
                        pady=20)

        card.pack(fill="x",
                  padx=25,
                  pady=12)

        tk.Label(card,
                 text=f"{c.get_first_name()} {c.get_last_name()}",
                 bg=CARD,
                 fg=PRIMARY,
                 font=("Arial", 18, "bold")).pack(anchor="w")

        tk.Label(card,
                 text=f"Account No: {c.get_account_no()}",
                 bg=CARD,
                 fg="white",
                 font=("Arial", 13)).pack(anchor="w", pady=3)

        tk.Label(card,
                 text=f"Address: {' '.join(c.get_address())}",
                 bg=CARD,
                 fg="#475569",
                 font=("Arial", 13)).pack(anchor="w", pady=3)

        tk.Label(card,
                 text=f"Balance: £{c.get_balance():,.2f}",
                 bg=CARD,
                 fg=SUCCESS,
                 font=("Arial", 16, "bold")).pack(anchor="w", pady=8)

# ------------------------
# REPORT
# ------------------------
def show_report():

    # ------------------------
    # GET REPORT DATA
    # ------------------------
    c, b, o, i = app.management_report()

    # ------------------------
    # WINDOW
    # ------------------------
    report = tk.Toplevel(root)
    report.title("Management Report")
    report.geometry("850x700")
    report.configure(bg="#eef2ff")
    report.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(report,
             text="Management Report",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 30, "bold")).pack(pady=(30, 5))

    tk.Label(report,
             text="Financial overview and banking statistics",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # MAIN CONTAINER
    # ------------------------
    container = tk.Frame(report,
                         bg="#eef2ff")

    container.pack(fill="both",
                   expand=True,
                   padx=30,
                   pady=30)

    # ------------------------
    # CARD FUNCTION
    # ------------------------
    def stat_card(parent,
                  title,
                  value,
                  color,
                  icon):

        card = tk.Frame(parent,
                        bg="white",
                        width=350,
                        height=170,
                        highlightbackground=BORDER,
                        highlightthickness=1)

        card.pack(side="left",
                  padx=15,
                  pady=15)

        card.pack_propagate(False)

        # Icon
        tk.Label(card,
                 text=icon,
                 bg="white",
                 fg=color,
                 font=("Segoe UI", 30)).pack(anchor="w",
                                             padx=25,
                                             pady=(20, 5))

        # Title
        tk.Label(card,
                 text=title,
                 bg="white",
                 fg=LIGHT_TEXT,
                 font=("Segoe UI", 13)).pack(anchor="w",
                                             padx=25)

        # Value
        tk.Label(card,
                 text=value,
                 bg="white",
                 fg=color,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w",
                                                     padx=25,
                                                     pady=10)

    # ------------------------
    # ROW 1
    # ------------------------
    row1 = tk.Frame(container,
                    bg="#eef2ff")

    row1.pack()

    stat_card(row1,
              "Total Customers",
              str(c),
              PRIMARY,
              "👥")

    stat_card(row1,
              "Total Balance",
              f"£{b:,.2f}",
              SUCCESS,
              "💰")

    # ------------------------
    # ROW 2
    # ------------------------
    row2 = tk.Frame(container,
                    bg="#eef2ff")

    row2.pack()

    stat_card(row2,
              "Overdraft Amount",
              f"£{o:,.2f}",
              DANGER,
              "⚠")

    stat_card(row2,
              "Interest Per Year",
              f"£{i:,.2f}",
              WARNING,
              "📈")

    # ------------------------
    # FOOTER SUMMARY
    # ------------------------
    footer = tk.Frame(report,
                      bg="white",
                      height=70,
                      highlightbackground=BORDER,
                      highlightthickness=1)

    footer.pack(fill="x",
                side="bottom")

    tk.Label(footer,
             text="NeoBank Analytics Dashboard",
             bg="white",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 11)).pack(side="left",
                                         padx=25,
                                         pady=20)

    tk.Label(footer,
             text="2025 Financial Report",
             bg="white",
             fg=TEXT,
             font=("Segoe UI", 11, "bold")).pack(side="right",
                                                 padx=25)




# ------------------------
# View Cusomer Details
# ------------------------

def view_customer_details():

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("Customer Details")
    win.geometry("800x680")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Customer Details",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 30, "bold")).pack(pady=(30, 5))

    tk.Label(win,
             text="Search and view customer banking information",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # MAIN CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=15,
                    pady=10,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=30,
              pady=20,
              fill="x")

    # ------------------------
    # SELECT CUSTOMER
    # ------------------------
    tk.Label(card,
             text="Select Customer",
             bg="white",
             fg=TEXT,
             font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                 pady=(0, 8))

    names = [c.get_last_name() for c in app.accounts_list]

    var = tk.StringVar(value=names[0])

    dropdown = tk.OptionMenu(card,
                             var,
                             *names)

    dropdown.config(font=("Segoe UI", 12),
                    bg=INPUT_BG,
                    fg=TEXT,
                    width=25,
                    relief="solid",
                    bd=1)

    dropdown.pack(ipady=5,
                  pady=(0, 25))

    # ------------------------
    # PROFILE SECTION
    # ------------------------
    profile = tk.Frame(card,
                       bg="#f9fafb",
                       padx=2,
                       pady=10)

    profile.pack(fill="x")

    # Avatar
    tk.Label(profile,
             text="👤",
             bg="#f9fafb",
             fg=PRIMARY,
             font=("Segoe UI", 32)).pack(pady=(0, 5))

    # ------------------------
    # PROFILE LABELS
    # ------------------------
    name_label = tk.Label(profile,
                          text="Name",
                          bg="#f9fafb",
                          fg=TEXT,
                          font=("Segoe UI", 18, "bold"))

    name_label.pack(pady=(2, 5))

    def info_row(title):

        row = tk.Frame(profile,
                       bg="#f9fafb")

        row.pack(fill="x",
                 pady=2)

        left = tk.Label(row,
                        text=title,
                        bg="#f9fafb",
                        fg=LIGHT_TEXT,
                        font=("Segoe UI", 12, "bold"))

        left.pack(side="left")

        right = tk.Label(row,
                         text="",
                         bg="#f9fafb",
                         fg=TEXT,
                         font=("Segoe UI", 12))

        right.pack(side="right")

        return right

    acc_value = info_row("Account Number")
    address_value = info_row("Address")
    type_value = info_row("Account Type")
    balance_value = info_row("Balance")

    # ------------------------
    # SHOW CUSTOMER
    # ------------------------
    def show():

        customer = app.search_customers_by_name(var.get())

        if customer:

            name_label.config(
                text=f"{customer.get_first_name()} {customer.get_last_name()}"
            )

            acc_value.config(
                text=customer.get_account_no()
            )

            address_value.config(
                text=" ".join(customer.get_address())
            )

            type_value.config(
                text=type(customer).__name__
            )

            balance_value.config(
                text=f"£{customer.get_balance():,.2f}",
                fg=SUCCESS
            )

    # Initial Load
    show()

    button_frame = tk.Frame(card,
                            bg="white")

    button_frame.pack(pady=5)

    tk.Button(button_frame,
            text="Refresh Details",
            command=show,
            bg=PRIMARY,
            fg="white",
            activebackground=PRIMARY_HOVER,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 12, "bold"),
            width=22,
            pady=8).pack()
    
def delete_customer(admin):

    # ------------------------
    # ADMIN RIGHTS CHECK
    # ------------------------
    if not admin.has_full_admin_right():

        messagebox.showerror(
            "Permission Denied",
            "Only full admins can delete customers"
        )

        return

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("Delete Customer")
    win.geometry("700x650")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Delete Customer",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 30, "bold")).pack(pady=(30, 5))

    tk.Label(win,
             text="Remove customer accounts securely",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=20,
                    pady=15,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=25,
              pady=15,
              fill="x")

    # ------------------------
    # WARNING SECTION
    # ------------------------
    warning = tk.Frame(card,
                       bg="#fef2f2",
                       padx=20,
                       pady=20,
                       highlightbackground="#fecaca",
                       highlightthickness=1)

    warning.pack(fill="x",
                 pady=(0, 25))

    tk.Label(warning,
             text="⚠ Warning",
             bg="#fef2f2",
             fg=DANGER,
             font=("Segoe UI", 16, "bold")).pack(anchor="w")

    tk.Label(warning,
             text="Deleting a customer account is permanent and cannot be undone.",
             bg="#fef2f2",
             fg="#7f1d1d",
             font=("Segoe UI", 11)).pack(anchor="w",
                                         pady=(8, 0))

    # ------------------------
    # CUSTOMER SELECT
    # ------------------------
    tk.Label(card,
             text="Select Customer",
             bg="white",
             fg=TEXT,
             font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                 pady=(0, 8))

    names = [c.get_last_name() for c in app.accounts_list]

    # No customers
    if not names:

        tk.Label(card,
                 text="No customers available",
                 bg="white",
                 fg=DANGER,
                 font=("Segoe UI", 14)).pack(pady=30)

        return

    var = tk.StringVar(value=names[0])

    menu = tk.OptionMenu(card,
                         var,
                         *names)

    menu.config(font=("Segoe UI", 12),
                bg=INPUT_BG,
                fg=TEXT,
                width=25,
                relief="solid",
                bd=1)

    menu.pack(ipady=5,
              pady=(0, 25))

    # ------------------------
    # PROFILE PREVIEW
    # ------------------------
    preview_frame = tk.Frame(card,
                             bg="#f9fafb",
                             padx=15,
                             pady=8,
                             highlightbackground="#e5e7eb",
                             highlightthickness=1)

    preview_frame.pack(fill="x",
                       pady=10)

    # Avatar
    tk.Label(preview_frame,
             text="👤",
             bg="#f9fafb",
             fg=DANGER,
             font=("Segoe UI", 28)).pack(pady=(0, 5))

    # Customer Info
    preview_name = tk.Label(preview_frame,
                            text="Customer Name",
                            bg="#f9fafb",
                            fg=TEXT,
                            font=("Segoe UI", 16, "bold"))

    preview_name.pack(pady=(2, 8))

    def info_row(title):

        row = tk.Frame(preview_frame,
                       bg="#f9fafb")

        row.pack(fill="x",
                 pady=1)

        left = tk.Label(row,
                        text=title,
                        bg="#f9fafb",
                        fg=LIGHT_TEXT,
                        font=("Segoe UI", 12, "bold"))

        left.pack(side="left")

        right = tk.Label(row,
                         text="",
                         bg="#f9fafb",
                         fg=TEXT,
                         font=("Segoe UI", 12))

        right.pack(side="right")

        return right

    acc_value = info_row("Account Number")
    # balance_value = info_row("Balance")

    # ------------------------
    # SHOW PREVIEW
    # ------------------------
    def show_preview():

        customer = app.search_customers_by_name(
            var.get()
        )

        if customer:

            preview_name.config(
                text=f"{customer.get_first_name()} {customer.get_last_name()}"
            )

            acc_value.config(
                text=customer.get_account_no()
            )


    show_preview()

    # Update preview dynamically
    var.trace("w",
              lambda *args: show_preview())

    # ------------------------
    # DELETE FUNCTION
    # ------------------------
    def delete():

        customer = app.search_customers_by_name(
            var.get()
        )

        if customer:

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete "
                f"{customer.get_first_name()} {customer.get_last_name()}?"
            )

            if confirm:

                app.accounts_list.remove(customer)

                app.save_data()

                messagebox.showinfo(
                    "Success",
                    "Customer deleted successfully"
                )

                win.destroy()

    # ------------------------
    # DELETE BUTTON
    # ------------------------
    button_frame = tk.Frame(card,
                            bg="white")

    button_frame.pack(fill="x",
                    pady=10)

    tk.Button(button_frame,
            text="Delete Customer",
            command=delete,
            bg=DANGER,
            fg="white",
            activebackground=DANGER_HOVER,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 12, "bold"),
            width=22,
            pady=8).pack()
    
    
def create_customer_gui():

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("Create Customer")
    win.geometry("700x780")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Create Customer",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 30, "bold")).pack(pady=(30, 5))

    tk.Label(win,
             text="Register a new banking customer",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=45,
                    pady=35,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=40,
              pady=30,
              fill="both",
              expand=True)

    # ------------------------
    # HELPER FUNCTIONS
    # ------------------------
    def form_label(text):

        tk.Label(card,
                 text=text,
                 bg="white",
                 fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                     pady=(18, 5))

    def form_entry():

        entry = tk.Entry(card,
                         font=("Segoe UI", 13),
                         bg=INPUT_BG,
                         fg=TEXT,
                         relief="solid",
                         bd=1)

        entry.pack(fill="x",
                   ipady=10)

        return entry

    # ------------------------
    # FIRST NAME
    # ------------------------
    form_label("First Name")

    fname = form_entry()

    # ------------------------
    # LAST NAME
    # ------------------------
    form_label("Last Name")

    lname = form_entry()

    # ------------------------
    # ADDRESS
    # ------------------------
    form_label("Address")

    addr = form_entry()

    # ------------------------
    # ACCOUNT TYPE
    # ------------------------
    form_label("Account Type")

    type_var = tk.StringVar(value="normal")

    menu = tk.OptionMenu(card,
                         type_var,
                         "normal",
                         "savings",
                         "advanced")

    menu.config(font=("Segoe UI", 12),
                bg=INPUT_BG,
                fg=TEXT,
                width=25,
                relief="solid",
                bd=1)

    menu.pack(ipady=5,
              pady=5)

    # ------------------------
    # CREATE FUNCTION
    # ------------------------
    def create():

        first_name = fname.get().strip()
        last_name = lname.get().strip()
        address_text = addr.get().strip()

        # Validation
        if first_name == "":

            messagebox.showerror(
                "Error",
                "First name cannot be empty"
            )

            return

        if last_name == "":

            messagebox.showerror(
                "Error",
                "Last name cannot be empty"
            )

            return

        if address_text == "":

            messagebox.showerror(
                "Error",
                "Address cannot be empty"
            )

            return

        # Create customer
        address = address_text.split(",")

        app.create_customer(
            first_name,
            last_name,
            address,
            type_var.get()
        )

        messagebox.showinfo(
            "Success",
            "Customer created successfully"
        )

        # Clear Fields
        fname.delete(0, tk.END)
        lname.delete(0, tk.END)
        addr.delete(0, tk.END)

    # ------------------------
    # BUTTON
    # ------------------------
    tk.Button(card,
              text="Create Customer",
              command=create,
              bg=PRIMARY,
              fg="white",
              activebackground=PRIMARY_HOVER,
              activeforeground="white",
              relief="flat",
              cursor="hand2",
              font=("Segoe UI", 14, "bold"),
              width=25,
              pady=14).pack(pady=45)
    

def update_customer_info():

    # ------------------------
    # WINDOW
    # ------------------------
    win = tk.Toplevel(root)
    win.title("Update Customer")
    win.geometry("750x700")
    win.configure(bg="#eef2ff")
    win.resizable(False, False)

    # ------------------------
    # HEADER
    # ------------------------
    tk.Label(win,
             text="Update Customer",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 30, "bold")).pack(pady=(30, 5))

    tk.Label(win,
             text="Edit and manage customer information",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 12)).pack()

    # ------------------------
    # CARD
    # ------------------------
    card = tk.Frame(win,
                    bg="white",
                    padx=25,
                    pady=15,
                    highlightbackground=BORDER,
                    highlightthickness=1)

    card.pack(padx=25,
              pady=15,
              fill="x")

    # ------------------------
    # SELECT CUSTOMER
    # ------------------------
    tk.Label(card,
             text="Select Customer",
             bg="white",
             fg=TEXT,
             font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                 pady=(0, 8))

    names = [c.get_last_name() for c in app.accounts_list]

    var = tk.StringVar(value=names[0])

    menu = tk.OptionMenu(card,
                         var,
                         *names)

    menu.config(font=("Segoe UI", 12),
                bg=INPUT_BG,
                fg=TEXT,
                width=25,
                relief="solid",
                bd=1)

    menu.pack(ipady=5,
              pady=(0, 25))

    # ------------------------
    # PROFILE ICON
    # ------------------------
    tk.Label(card,
             text="👤",
             bg="white",
             fg=PRIMARY,
             font=("Segoe UI", 36)).pack(pady=(0, 5))

    # ------------------------
    # HELPER FUNCTIONS
    # ------------------------
    def form_label(text):

        tk.Label(card,
                 text=text,
                 bg="white",
                 fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w",
                                                     pady=(10, 3))

    def form_entry():

        entry = tk.Entry(card,
                         font=("Segoe UI", 13),
                         bg=INPUT_BG,
                         fg=TEXT,
                         relief="solid",
                         bd=1)

        entry.pack(fill="x",
                   ipady=6)

        return entry

    # ------------------------
    # INPUTS
    # ------------------------
    form_label("New First Name")
    fname_entry = form_entry()

    form_label("New Last Name")
    lname_entry = form_entry()

    form_label("New Address")
    addr_entry = form_entry()

    # ------------------------
    # UPDATE FUNCTION
    # ------------------------
    def update():

        customer = app.search_customers_by_name(
            var.get()
        )

        if customer:

            first_name = fname_entry.get().strip()
            last_name = lname_entry.get().strip()
            address = addr_entry.get().strip()

            # Validation
            if first_name == "":

                messagebox.showerror(
                    "Error",
                    "First name cannot be empty"
                )

                return

            if last_name == "":

                messagebox.showerror(
                    "Error",
                    "Last name cannot be empty"
                )

                return

            if address == "":

                messagebox.showerror(
                    "Error",
                    "Address cannot be empty"
                )

                return

            # Update
            customer.update_first_name(first_name)

            customer.update_last_name(last_name)

            customer.update_address(
                address.split(",")
            )

            app.save_data()

            messagebox.showinfo(
                "Success",
                "Customer updated successfully"
            )

            # Clear Fields
            fname_entry.delete(0, tk.END)
            lname_entry.delete(0, tk.END)
            addr_entry.delete(0, tk.END)

    # ------------------------
    # UPDATE BUTTON
    # ------------------------
    tk.Button(card,
              text="Update Customer",
              command=update,
              bg=PRIMARY,
              fg="white",
              activebackground=PRIMARY_HOVER,
              activeforeground="white",
              relief="flat",
              cursor="hand2",
              font=("Segoe UI", 14, "bold"),
              width=25,
              pady=8).pack(pady=15)

# ------------------------
# DASHBOARD
# ------------------------
def open_dashboard(admin):

    dashboard = tk.Toplevel(root)
    dashboard.title("NeoBank Dashboard")
    dashboard.geometry("1400x950")
    dashboard.configure(bg="#eef2ff")

    # ------------------------
    # LOGOUT
    # ------------------------
    def logout():
        dashboard.destroy()
        root.deiconify()

    # ------------------------
    # SIDEBAR
    # ------------------------
    sidebar = tk.Frame(dashboard,
                       bg="#111827",
                       width=260)

    sidebar.pack(side="left",
                 fill="both",
                 expand=True)

    # Brand
    tk.Label(sidebar,
             text="NeoBank",
             bg="#111827",
             fg="white",
             font=("Segoe UI", 26, "bold")).pack(pady=(30, 5))

    tk.Label(sidebar,
             text="Admin Control Panel",
             bg="#111827",
             fg="#9ca3af",
             font=("Segoe UI", 11)).pack()

    # Divider
    tk.Frame(sidebar,
             bg="#374151",
             height=1).pack(fill="x",
                            padx=20,
                            pady=20)

    # ------------------------
    # SIDEBAR BUTTONS
    # ------------------------
    def sidebar_btn(text, command, color="#111827"):

        return tk.Button(
            sidebar,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=PRIMARY,
            activeforeground="white",
            relief="flat",
            anchor="w",
            cursor="hand2",
            padx=30,
            pady=7,
            font=("Segoe UI", 10, "bold"),
            width=22
        )

    sidebar_btn("🏠 Dashboard",
                lambda: None).pack(pady=2)

    sidebar_btn("👥 Customers",
                print_all_customers).pack(pady=2)

    sidebar_btn("🔎 Search Customer",
                view_customer_details).pack(pady=2)

    sidebar_btn("💳 Customer Operations",
                open_customer_ops).pack(pady=2)

    sidebar_btn("💸 Transfer Money",
                open_transfer).pack(pady=2)

    sidebar_btn("➕ Create Customer",
                create_customer_gui).pack(pady=2)

    sidebar_btn("✏ Update Customer",
                update_customer_info).pack(pady=2)

    sidebar_btn("🗑 Delete Customer",
                lambda: delete_customer(admin)).pack(pady=2)

    sidebar_btn("📈 Reports",
                show_report).pack(pady=2)

    sidebar_btn("👤 My Profile",
                lambda: show_admin_info(admin)).pack(pady=2)

    sidebar_btn("⚙ Update Admin",
                lambda: update_admin_info(admin)).pack(pady=2)
    # Spacer pushes logout down
    spacer = tk.Frame(sidebar,
                    bg="#111827")

    spacer.pack(expand=True,
                fill="both")

    # Logout Button
    sidebar_btn("🚪 Logout",
                logout,
                DANGER).pack(side="bottom",
                            padx=15,
                            pady=(10, 70))

    # ------------------------
    # MAIN CONTENT
    # ------------------------
    content = tk.Frame(dashboard,
                       bg="#eef2ff")

    content.pack(side="right",
                 fill="both",
                 expand=True)

    # ------------------------
    # TOPBAR
    # ------------------------
    topbar = tk.Frame(content,
                      bg="white",
                      height=70)

    topbar.pack(fill="x")

    # Welcome Text
    tk.Label(topbar,
             text=f"Welcome, {admin.get_first_name()}",
             bg="white",
             fg=TEXT,
             font=("Segoe UI", 20, "bold")).pack(side="left",
                                                 padx=30,
                                                 pady=15)

    # Admin Info
    tk.Label(topbar,
             text="Full Admin Access",
             bg="white",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 11)).pack(side="right",
                                         padx=30)

    # ------------------------
    # DASHBOARD TITLE
    # ------------------------
    tk.Label(content,
             text="Banking Overview",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 28, "bold")).pack(anchor="w",
                                                 padx=35,
                                                 pady=(30, 5))

    tk.Label(content,
             text="Monitor and manage banking operations",
             bg="#eef2ff",
             fg=LIGHT_TEXT,
             font=("Segoe UI", 13)).pack(anchor="w",
                                         padx=35)

    # ------------------------
    # STATS SECTION
    # ------------------------
    stats_frame = tk.Frame(content,
                           bg="#eef2ff")

    stats_frame.pack(anchor="w",
                     padx=25,
                     pady=30)

    total_customers = len(app.accounts_list)
    total_balance = sum([c.get_balance() for c in app.accounts_list])

    # ------------------------
    # CARD DESIGN
    # ------------------------
    def create_card(parent, title, value, color):

        card = tk.Frame(parent,
                        bg="white",
                        width=260,
                        height=150,
                        highlightbackground="#d1d5db",
                        highlightthickness=1)

        card.pack(side="left",
                  padx=12)

        card.pack_propagate(False)

        tk.Label(card,
                 text=title,
                 bg="white",
                 fg=LIGHT_TEXT,
                 font=("Segoe UI", 13)).pack(anchor="w",
                                             padx=20,
                                             pady=(25, 5))

        tk.Label(card,
                 text=value,
                 bg="white",
                 fg=color,
                 font=("Segoe UI", 30, "bold")).pack(anchor="w",
                                                     padx=20)

    create_card(stats_frame,
                "Total Customers",
                str(total_customers),
                PRIMARY)

    create_card(stats_frame,
                "Total Balance",
                f"£{total_balance:,.2f}",
                SUCCESS)

    create_card(stats_frame,
                "Overdraft Amount",
                "£0.00",
                DANGER)

    # ------------------------
    # QUICK ACTIONS
    # ------------------------
    tk.Label(content,
             text="Quick Actions",
             bg="#eef2ff",
             fg=TEXT,
             font=("Segoe UI", 22, "bold")).pack(anchor="w",
                                                 padx=35,
                                                 pady=(10, 10))

    actions = tk.Frame(content,
                       bg="#eef2ff")

    actions.pack(anchor="w",
                 padx=35)

    def action_btn(text, command):

        return tk.Button(
            actions,
            text=text,
            command=command,
            bg="white",
            fg=TEXT,
            activebackground="#f3f4f6",
            activeforeground=TEXT,
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=20,
            pady=15,
            font=("Segoe UI", 12, "bold"),
            width=20
        )

    action_btn("🔎 Search Customer",
               view_customer_details).pack(side="left",
                                           padx=10)

    action_btn("💸 Transfer Money",
               open_transfer).pack(side="left",
                                   padx=10)

    action_btn("📈 Reports",
               show_report).pack(side="left",
                                 padx=10)

# ------------------------
# LOGIN FUNCTION
# ------------------------
def login():

    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    # Empty fields
    if username == "" or password == "":
        messagebox.showerror("Error", "Please enter username and password")
        return

    msg, admin = app.admin_login(username, password)

    if admin:
        messagebox.showinfo("Success", msg)
        root.withdraw()
        open_dashboard(admin)
    else:
        messagebox.showerror("Login Error", msg)



# ------------------------
# MAIN WINDOW
# ------------------------

root = tk.Tk()
root.title("NeoBank Management System")
root.geometry("1100x650")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# ------------------------
# LEFT SIDE PANEL
# ------------------------
left_frame = tk.Frame(root,
                      bg=PRIMARY,
                      width=420)

left_frame.pack(side="left",
                fill="y")

# Logo
tk.Label(left_frame,
         text="🏦",
         bg=PRIMARY,
         fg="white",
         font=("Arial", 80)).pack(pady=(120, 20))

# Brand
tk.Label(left_frame,
         text="NeoBank",
         bg=PRIMARY,
         fg="white",
         font=("Arial", 34, "bold")).pack()

# Subtitle
tk.Label(left_frame,
         text="Smart Banking Admin System",
         bg=PRIMARY,
         fg="#dbeafe",
         font=("Arial", 16)).pack(pady=15)

# ------------------------
# RIGHT SIDE LOGIN AREA
# ------------------------
right_frame = tk.Frame(root,
                       bg=BG_COLOR)

right_frame.pack(side="right",
                 fill="both",
                 expand=True)

# Login Card
login_card = tk.Frame(right_frame,
                      bg="white",
                      padx=50,
                      pady=50,
                      highlightbackground=BORDER,
                      highlightthickness=1)

login_card.place(relx=0.5,
                 rely=0.5,
                 anchor="center")

# Welcome
tk.Label(login_card,
         text="Welcome Back",
         bg="white",
         fg=TEXT,
         font=("Arial", 28, "bold")).pack(pady=(0, 10))

# Small text
tk.Label(login_card,
         text="Login to continue",
         bg="white",
         fg=LIGHT_TEXT,
         font=("Arial", 13)).pack(pady=(0, 30))

# ------------------------
# USERNAME
# ------------------------
tk.Label(login_card,
         text="Username",
         bg="white",
         fg=TEXT,
         font=("Arial", 12, "bold")).pack(anchor="w")

entry_user = tk.Entry(login_card,
                      font=("Arial", 14),
                      bg=INPUT_BG,
                      fg=TEXT,
                      relief="solid",
                      bd=1,
                      width=30)

entry_user.pack(ipady=10,
                pady=(5, 20))

# ------------------------
# PASSWORD
# ------------------------
tk.Label(login_card,
         text="Password",
         bg="white",
         fg=TEXT,
         font=("Arial", 12, "bold")).pack(anchor="w")

entry_pass = tk.Entry(login_card,
                      font=("Arial", 14),
                      bg=INPUT_BG,
                      fg=TEXT,
                      relief="solid",
                      bd=1,
                      show="*",
                      width=30)

entry_pass.pack(ipady=10,
                pady=(5, 30))

# ------------------------
# LOGIN BUTTON
# ------------------------
login_btn = tk.Button(login_card,
                      text="Login",
                      command=login,
                      bg=PRIMARY,
                      fg="white",
                      activebackground=PRIMARY_HOVER,
                      activeforeground="white",
                      relief="flat",
                      cursor="hand2",
                      font=("Arial", 14, "bold"),
                      width=25,
                      pady=12)

login_btn.pack()

# ------------------------
# FOOTER
# ------------------------
tk.Label(right_frame,
         text="© 2025 NeoBank Management System",
         bg=BG_COLOR,
         fg=LIGHT_TEXT,
         font=("Arial", 10)).pack(side="bottom",
                                  pady=20)

root.mainloop()