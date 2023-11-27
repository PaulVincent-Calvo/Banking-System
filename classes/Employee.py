from BankingMethods import BankingMethods
from tkinter import messagebox
from tabulate import tabulate
import tkinter as tk

class Employee(BankingMethods):
    def __init__(self):
        super().__init__()  

    def get_transactions(self):
        cursor = self.connection.cursor()
        get_transactions_query = f"SELECT * from transactions"
        cursor.execute(get_transactions_query)

        transactions_rows = cursor.fetchall()

        column_names = ["Transaction ID", "Checkings ID", "Date", "Time", "Amount", "Transaction Type"]

        transactions = tabulate(transactions_rows, headers=column_names, tablefmt='grid')

        cursor.close()

        return transactions

    def emp_search_transaction(self):
        search_transactions_root = tk.Tk()
        search_transactions_root.geometry("300x200")
        search_transactions_root.title("Search Transactions Page")

        search_frame = tk.Frame(search_transactions_root, width=300,)

        search_transaction_id_label = tk.Label(search_frame, text="Transaction ID:")
        search_transaction_id_entry = tk.Entry(search_frame)

        search_transaction_button = tk.Button(search_frame, text="Search", command=lambda: self.search_transaction_button_clicked(search_transaction_id_entry, search_transactions_root))

        search_frame.pack(expand=True, fill="none", side="top")
        search_transaction_id_label.pack()
        search_transaction_id_entry.pack()
        search_transaction_button.pack(pady=10)

        search_transactions_root.mainloop()

    def search_transaction_button_clicked(self, transaction_id ,root):
        transaction_id = transaction_id.get()
        
        if self.search_transactions(transaction_id, 1):
            root.destroy()            
            # print (transaction)
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
            transaction_info = self.search_transactions(transaction_id, 1) 
            transaction_info_text = tk.Text(main_frame, height=5.2, width=93, wrap=tk.NONE)
            transaction_info_text.insert(tk.END, transaction_info)
            transaction_info_text.config(state="disabled")
            transaction_info_text.pack(side="top", padx=10, pady=10) 

            # horizontal scrollbar 
            horizontal_scrollbar = tk.Scrollbar(main_frame, orient="horizontal", command=transaction_info_text.xview)
            horizontal_scrollbar.pack(side="bottom", fill="x")
            
            main_frame.pack(side="top", fill="y")

            transaction_found_root.mainloop()

    def transaction_button_clicked(self, id_entry, root):
        root.destroy()
        self.transaction_page(id_entry)

    def get_customer_info(self):
        cursor = self.connection.cursor()

        # query too long so changed its fromat to this
        get_info_query = """
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
                customer_information.customer_id = checkings_account.customer_id;"""
        
        cursor.execute(get_info_query)

        account_info_rows = cursor.fetchall()

        column_names = ["Customer ID", "Password", "First Name", "Last Name", 
                        "Email", "Address", "ID Type", "Occupation", 
                        "Annual Gross Income", "Checkings ID", "Balance"]
        
        accoount_info = tabulate(account_info_rows, headers=column_names,tablefmt="grid")
        
        return accoount_info
    
    def customer_accounts_button_clicked(self, id_entry, root):
        root.destroy()
        self.customer_accounts_page(id_entry)

    def emp_search_account(self):
        search_account_root = tk.Tk()
        search_account_root.geometry("300x200")
        search_account_root.title("Search Accounts Page")

        search_frame = tk.Frame(search_account_root, width=300,)

        search_account_id_label = tk.Label(search_frame, text="Account ID:")
        search_account_id_entry = tk.Entry(search_frame)

        search_account_button = tk.Button(search_frame, text="Search", command=lambda: self.search_account_button_clicked(search_account_id_entry, search_account_root))

        search_frame.pack(expand=True, fill="none", side="top")
        search_account_id_label.pack()
        search_account_id_entry.pack()
        search_account_button.pack(pady=10)

        search_account_root.mainloop()

    def search_account_button_clicked(self, customer_id ,root):
        customer_id = customer_id.get()
        
        if self.search_accounts(customer_id, 1):
            root.destroy() 

            account_found_root = tk.Tk()
            account_found_root.geometry("900x170")
            account_found_root.title("Account Search Result Page")

            secondary_frame = tk.Frame(account_found_root, width = 300, height = 50)
            main_frame = tk.Frame(account_found_root, width = 700, height = 100)

            # content on secondary frame (Transaction Found Label)
            account_found_label = tk.Label(secondary_frame, text="Account Found!")
            account_found_label.pack(side="top", pady=10)

            secondary_frame.pack(side="top", fill="y")

            # content on main frame (Transaction Table)
            account_info = self.search_accounts(customer_id, 1) 
            account_info_text = tk.Text(main_frame, height=5.2, width=140, wrap=tk.NONE)
            account_info_text.insert(tk.END, account_info)
            account_info_text.config(state="disabled")
            account_info_text.pack(side="top", padx=10, pady=10) 

            # horizontal scrollbar 
            horizontal_scrollbar = tk.Scrollbar(main_frame, orient="horizontal", command=account_info_text.xview)
            horizontal_scrollbar.pack(side="bottom", fill="x")
            
            main_frame.pack(side="top", fill="y")

            account_found_root.mainloop()

    def delete_account(self, customer_id, delete_account_root, emp_id_entry, main_root):
        cursor = self.connection.cursor()
        successful = False

        try:
            customer_id = customer_id.get()

            # done this way because of the constraint in customer_information table as a parent table
            delete_bank_asset_row_query = f"""
                DELETE FROM bank_assets
                WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = {customer_id});
            """
            cursor.execute(delete_bank_asset_row_query)

            delete_checkings_account_row_query = f"""
                DELETE FROM checkings_account
                WHERE customer_id = {customer_id};
            """
            cursor.execute(delete_checkings_account_row_query)

            delete_customer_information_row_query = f"""
                DELETE FROM customer_information
                WHERE customer_id = {customer_id};
            """
            cursor.execute(delete_customer_information_row_query)

            self.connection.commit()

            messagebox.showinfo("Success", "Account deleted successfully!")

            cursor.close()
            successful = True

        except Exception as e:
            # Display error messagebox
            messagebox.showerror("Error", f"Unable to delete account. Error: {str(e)}")
            print(e)

        if successful:
            delete_account_root.destroy()
            main_root.destroy()
            self.customer_accounts_page(emp_id_entry)

    def emp_delete_account(self, emp_id_entry, main_root):
        delete_account_root = tk.Tk()
        delete_account_root.geometry("300x200")
        delete_account_root.title("Delete Accounts Page")

        delete_frame = tk.Frame(delete_account_root, width=300,)

        delete_account_id_label = tk.Label(delete_frame, text="Account ID:")
        delete_account_id_entry = tk.Entry(delete_frame)

        delete_account_button = tk.Button(delete_frame, text="Delete", command=lambda: self.delete_account(delete_account_id_entry, delete_account_root, emp_id_entry, main_root))

        delete_frame.pack(expand=True, fill="none", side="top")
        delete_account_id_label.pack()
        delete_account_id_entry.pack()
        delete_account_button.pack(pady=10)

        delete_account_root.mainloop()

    def test(self):
        try:
            self.connect_database()
            if self.check_database_connection():
                pass

        except Exception as e:
            messagebox.showerror("Database Connection Error", str(e))

    def login_page(self):
        login_root = tk.Tk()
        login_root.geometry("300x200")
        login_root.title("Login Page")

        login_frame = tk.Frame(login_root, width = 300, height = 200)

        label_id = tk.Label(login_frame, text="ID:")
        label_password = tk.Label(login_frame, text="Password:")

        employee_id_entry = tk.Entry(login_frame)
        employee_password_entry = tk.Entry(login_frame, show="*")  # replaces input with "*"s for security

        login_button = tk.Button(login_frame, text="Login", command=lambda: self.login(login_root, employee_id_entry, employee_password_entry, 1))

        # layout 
        login_frame.pack(expand=True, fill="none", side="top")
        label_id.pack()
        employee_id_entry.pack()
        label_password.pack()
        employee_password_entry.pack()
        login_button.pack(pady=20)

        login_root.mainloop()

    def customer_accounts_page(self, id_entry):
        main_root = tk.Tk()
        main_root.geometry("900x500")
        main_root.title("Customer Accounts Page")

        # frames
        secondary_frame = tk.Frame(main_root, width = 300, height = 500)
        main_frame = tk.Frame(main_root, width = 700, height = 500)

        # content on secondary frame (Employee Name and Buttons)
        first_name, last_name = self.get_name(id_entry, 1)
        employee_name_label = tk.Label(secondary_frame, text=f"Welcome {first_name} {last_name}!")
        employee_name_label.pack(side="top", pady=10)

        secondary_frame.pack(side="top", fill="y")

        search_button = tk.Button(secondary_frame, text="Search", command=lambda: self.emp_search_account())
        view_transactions_button = tk.Button(secondary_frame, text="Transactions", command=lambda: self.transaction_button_clicked(id_entry, main_root))
        create_customer_accounts = tk.Button(secondary_frame, text="Create Accounts")
        delete_accounts = tk.Button(secondary_frame, text="Delete Accounts", command=lambda: self.emp_delete_account(id_entry))
        edit_customer_information = tk.Button(secondary_frame, text="Edit Customer Information")

        search_button.pack(side="left", padx=5)
        view_transactions_button.pack(side="left", padx=5)
        create_customer_accounts.pack(side="left", padx=5)
        delete_accounts.pack(side="left", padx=5)
        edit_customer_information.pack(side="left", padx=5)

        # content on main frame
        account_info = self.get_customer_info()
        account_info_text = tk.Text(main_frame, height=10, width=50, wrap=tk.NONE)
        account_info_text.insert(tk.END, account_info)
        account_info_text.config(state="disabled")
        account_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # scrollbars for the table if it has many content
        vertical_scrollbar = tk.Scrollbar(main_frame, command=account_info_text.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        account_info_text.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=account_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")  # Place it at the top
        account_info_text.config(xscrollcommand=horizontal_scrollbar.set)

        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def transaction_page(self, id_entry):
        transaction_root = tk.Tk()
        transaction_root.geometry("900x500")
        transaction_root.title("Customer Transactions Page")

        secondary_frame = tk.Frame(transaction_root, width = 300, height = 500)
        main_frame = tk.Frame(transaction_root, width = 900, height = 300)

        # content on secondary frame (Employee Name and Buttons)
        first_name, last_name = self.get_name(id_entry, 1)
        employee_name_label = tk.Label(secondary_frame, text=f"Welcome {first_name} {last_name}!")
        employee_name_label.pack(side="top", pady=10)

        secondary_frame.pack(side="top", fill="y")

        search_button = tk.Button(secondary_frame, text="Search", command=lambda: self.emp_search_transaction())
        customer_accounts_button = tk.Button(secondary_frame, text="Customer Accounts", command=lambda: self.customer_accounts_button_clicked(id_entry, transaction_root))

        search_button.pack(side="left", padx=5)
        customer_accounts_button.pack(side="left", padx=5)

        # content on main frame
        transaction_info = self.get_transactions()
        transaction_info_text = tk.Text(main_frame, height=10, width=93, wrap=tk.NONE)
        transaction_info_text.insert(tk.END, transaction_info)
        transaction_info_text.config(state="disabled")
        transaction_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # scrollbar for the table if it has many contents
        vertical_scrollbar = tk.Scrollbar(main_frame, command=transaction_info_text.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        transaction_info_text.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=transaction_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")  # Place it at the top
        transaction_info_text.config(xscrollcommand=horizontal_scrollbar.set)
        
        main_frame.pack(side="top", fill="y", expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        transaction_root.mainloop()

test_instance = Employee()
test_instance.test()
# print(test_instance.get_transactions())
test_instance.login_page()
