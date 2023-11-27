from BankingMethods import BankingMethods
from tkinter import messagebox
from tabulate import tabulate
import tkinter as tk

class Customer(BankingMethods):
    def __init__(self):
        super().__init__()  

    def test(self):
        try:
            self.connect_database()
            if self.check_database_connection():
                pass

        except Exception as e:
            messagebox.showerror("Database Connection Error", str(e))

    def get_checkings_id(self, customer_id):
        cursor = self.connection.cursor()
        get_checkings_id_query = "SELECT checkings_id FROM checkings_account WHERE customer_id = %s"

        cursor.execute(get_checkings_id_query, (customer_id,))
        checkings_id = cursor.fetchone()

        cursor.close()
        return checkings_id[0] if checkings_id else None

    def get_personal_info(self, customer_id):
        cursor = self.connection.cursor()
        
        # query too long so changed its fromat to this
        get_info_query = f"""
            SELECT 
                customer_information.customer_id, 
                customer_information.customer_password, 
                customer_information.first_name, 
                customer_information.last_name, 
                customer_information.email, 
                customer_information.address, 
                customer_information.id_type, 
                customer_information.occupation, 
                customer_information.annual_gross_income, 
                checkings_account.checkings_id, 
                checkings_account.balance
            FROM 
                customer_information 
            JOIN 
                checkings_account 
            ON 
                customer_information.customer_id = checkings_account.customer_id
            WHERE
                customer_information.customer_id = {customer_id};"""
            
        cursor.execute(get_info_query)

        account_info_rows = cursor.fetchall()

        column_names = ["Customer ID", "Password", "First Name", "Last Name", 
                        "Email", "Address", "ID Type", "Occupation", 
                        "Annual Gross Income", "Checkings ID", "Balance"]
        
        accoount_info = tabulate(account_info_rows, headers=column_names,tablefmt="grid")
        
        return accoount_info
    
    def customer_search_transaction(self, customer_id):
        search_transactions_root = tk.Tk()
        search_transactions_root.geometry("300x200")
        search_transactions_root.title("Search Transactions Page")

        search_frame = tk.Frame(search_transactions_root, width=300,)

        search_transaction_id_label = tk.Label(search_frame, text="Transaction ID:")
        search_transaction_id_entry = tk.Entry(search_frame)

        search_transaction_button = tk.Button(search_frame, text="Search", command=lambda: self.search_transaction_button_clicked(search_transaction_id_entry, search_transactions_root, customer_id))

        search_frame.pack(expand=True, fill="none", side="top")
        search_transaction_id_label.pack()
        search_transaction_id_entry.pack()
        search_transaction_button.pack(pady=10)

        search_transactions_root.mainloop()

    def search_transaction_button_clicked(self, transaction_id_entry, root, customer_id):
        transaction_id_entry = transaction_id_entry.get()

        transaction_info = self.search_transactions(transaction_id_entry, 1)

        if transaction_info:
            checkings_id_from_transaction = int(transaction_info.split()[21])  
            checkings_id_from_customer = int(self.get_checkings_id(customer_id))

            if checkings_id_from_transaction == checkings_id_from_customer:
                root.destroy()
                transaction_found_root = tk.Tk()
                transaction_found_root.geometry("900x170")
                transaction_found_root.title("Transaction Search Result Page")

                secondary_frame = tk.Frame(transaction_found_root, width = 300, height = 50)
                main_frame = tk.Frame(transaction_found_root, width = 400, height = 100)

                # content on secondary frame (Transaction Found Label)
                transaction_found_label = tk.Label(secondary_frame, text="Transaction Found!")
                transaction_found_label.pack(side="top", pady=10)

                secondary_frame.pack(side="top", fill="y")

                # content on main frame (Transaction Table)
                transaction_info = self.search_transactions(transaction_id_entry, 1) 
                transaction_info_text = tk.Text(main_frame, height=5.2, width=93, wrap=tk.NONE)
                transaction_info_text.insert(tk.END, transaction_info)
                transaction_info_text.config(state="disabled")
                transaction_info_text.pack(side="top", padx=10, pady=10) 

                # horizontal scrollbar 
                horizontal_scrollbar = tk.Scrollbar(main_frame, orient="horizontal", command=transaction_info_text.xview)
                horizontal_scrollbar.pack(side="bottom", fill="x")
                
                main_frame.pack(side="top", fill="y")

                transaction_found_root.mainloop()
            else:
                messagebox.showerror("Search Failed", "No Transactions with that ID")

        else:
            messagebox.showerror("Search Failed", "No Transactions with that ID")

    def personal_info_button_clicked(self, root, customer_id):
        root.destroy()
        self.customer_account_page(customer_id)

    def transaction_page_button_clicked(self, root, customer_id):
        root.destroy()
        self.transaction_page(customer_id)

    def login_page(self):
        login_root = tk.Tk()
        login_root.geometry("300x200")
        login_root.title("Login Page")

        login_frame = tk.Frame(login_root, width = 300, height = 200)

        label_id = tk.Label(login_frame, text="ID:")
        label_password = tk.Label(login_frame, text="Password:")

        customer_id_entry = tk.Entry(login_frame)
        customer_password_entry = tk.Entry(login_frame, show="*")  # replaces input with "*"s for security

        login_button = tk.Button(login_frame, text="Login", command=lambda: self.login(login_root, customer_id_entry, customer_password_entry, 2))

        # layout 
        login_frame.pack(expand=True, fill="none", side="top")
        label_id.pack()
        customer_id_entry.pack()
        label_password.pack()
        customer_password_entry.pack()
        login_button.pack(pady=20)

        login_root.mainloop()

    def transaction_page(self, id_entry):
        main_root = tk.Tk()
        main_root.geometry("900x500")
        main_root.title("Transactions Page")

        checkings_id = self.get_checkings_id(id_entry)

        # frames
        secondary_frame = tk.Frame(main_root, width = 300, height = 500)
        main_frame = tk.Frame(main_root, width = 700, height = 500)

        # content on secondary frame (Customer Name, Balance, and Buttons)
        first_name, last_name, balance = self.get_name(id_entry, 2)
        employee_name_label = tk.Label(secondary_frame, text=f"Welcome {first_name} {last_name}!")
        employee_balance_label = tk.Label(secondary_frame, text=f"Balance: ${balance}")
        employee_name_label.pack(side="top", pady=10)
        employee_balance_label.pack(side="top", padx=10, pady=10)

        search_transaction_button = tk.Button(secondary_frame, text="Search Transaction", command=lambda: self.customer_search_transaction(id_entry))
        view_personal_info_button = tk.Button(secondary_frame, text="Personal Information Page", command=lambda: self.personal_info_button_clicked(main_root, id_entry))
        withdraw_button = tk.Button(secondary_frame, text="Withdraw")
        deposit_button = tk.Button(secondary_frame, text="Deposit")

        search_transaction_button.pack(side="left", padx=5)
        view_personal_info_button.pack(side="left", padx=5)
        withdraw_button.pack(side="left", padx=5)
        deposit_button.pack(side="left", padx=5)

        secondary_frame.pack(side="top", fill="y")

        # content on main frame
        transaction_info = self.search_transactions(checkings_id, 2)
        transaction_info_text = tk.Text(main_frame, height=10, width=93, wrap=tk.NONE)
        transaction_info_text.insert(tk.END, transaction_info)
        transaction_info_text.config(state="disabled")
        transaction_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # scrollbars for the table if it has many content
        vertical_scrollbar = tk.Scrollbar(main_frame, command=transaction_info_text.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        transaction_info_text.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=transaction_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")  
        transaction_info_text.config(xscrollcommand=horizontal_scrollbar.set)

        main_frame.pack(side="top", fill="y", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def customer_account_page(self, id_entry):
        main_root = tk.Tk()
        main_root.geometry("900x500")
        main_root.title("Personal Information Page")

        # frames
        secondary_frame = tk.Frame(main_root, width = 300, height = 500)
        main_frame = tk.Frame(main_root, width = 700, height = 500)

        # content on secondary frame (Customer Name and Buttons)
        first_name, last_name = self.get_name(id_entry, 1)
        customer_name_label = tk.Label(secondary_frame, text=f"Welcome {first_name} {last_name}!")
        customer_name_label.pack(side="top", pady=10)

        secondary_frame.pack(side="top", fill="y")

        view_transactions_button = tk.Button(secondary_frame, text="Transaction Page", command=lambda: self.transaction_page_button_clicked(main_root, id_entry))
        edit_personal_information = tk.Button(secondary_frame, text="Edit Personal Information")

        view_transactions_button.pack(side="left", padx=5)
        edit_personal_information.pack(side="left", padx=5)

        # content on main frame
        account_info = self.get_personal_info(id_entry)
        account_info_text = tk.Text(main_frame, height=10, width=50, wrap=tk.NONE)
        account_info_text.insert(tk.END, account_info)
        account_info_text.config(state="disabled")
        account_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # scrollbars for the table if it has many content
        vertical_scrollbar = tk.Scrollbar(main_frame, command=account_info_text.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        account_info_text.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=account_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
        account_info_text.config(xscrollcommand=horizontal_scrollbar.set)

        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

test_instance = Customer()
test_instance.test()
# print(test_instance.get_transactions())
test_instance.login_page()
