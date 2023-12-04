from BankingMethods import BankingMethods
from tkinter import messagebox
from tabulate import tabulate
import tkinter as tk

class Employee(BankingMethods):
    def __init__(self):
        super().__init__()
        self.connection = self.connect()
        
    def connect(self):
        try:
            self.connect_database()
            if self.check_database_connection():
                pass

        except Exception as e:
            messagebox.showerror("Database Connection Error", str(e))
    
    def logout_button_clicked(self, page_root):
        page_root.destroy()
        messagebox.showinfo("Logout Successful", "Account was logged out successfully.")        
        self.login_page()

    # functions used in customer accounts page     
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
    
    def open_search_account_page(self):
        search_account_page_root = tk.Tk()
        search_account_page_root.geometry("300x200")
        search_account_page_root.title("Search Accounts Page")

        search_account_page_frame = tk.Frame(search_account_page_root, width=300,)

        search_account_id_label = tk.Label(search_account_page_frame, text="Account ID:")
        search_account_id_entry = tk.Entry(search_account_page_frame)

        search_account_button = tk.Button(search_account_page_frame, text="Search", command=lambda: self.search_account_button_clicked(search_account_id_entry, search_account_page_root))

        search_account_page_frame.pack(expand=True, fill="none", side="top")
        search_account_id_label.pack()
        search_account_id_entry.pack()
        search_account_button.pack(pady=10)

        search_account_page_root.mainloop()
    
    def transactions_button_clicked(self, customer_page_root, customer_id):
        customer_page_root.destroy()
        self.customer_transactions_page(customer_id)
    
    def create_button_clicked(self, password, first_name, last_name, email, address, id_type,occupation, annual_gross_income, balance, create_account_page_root, employee_id, customer_accounts_page_root):

        password_entry = password.get()
        first_name_entry = first_name.get()
        last_name_entry = last_name.get()
        email_entry = email.get()
        address_entry = address.get()
        id_type_entry = id_type.get()
        occupation_entry = occupation.get()

        try:
            annual_gross_income_entry = float(annual_gross_income.get())
            if annual_gross_income_entry < 0:
                raise ValueError("Annual Gross Income must be a positive number.")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid Annual Gross Income. Please enter a valid number.")
            return

        try:
            balance_entry = float(balance.get())
            if balance_entry < 0:
                raise ValueError("Balance must be a positive number.")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid Balance. Please enter a valid number.")
            return

        if not all([password, first_name, last_name, email, address, id_type, occupation]):
            tk.messagebox.showerror("Error", "Please fill in all fields.")
            return
        

        create_customer_query = """INSERT INTO customer_information (customer_password, first_name, last_name, email, address, id_type, occupation, annual_gross_income)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        
        cursor = self.connection.cursor()
        cursor.execute(create_customer_query, (password_entry, first_name_entry, last_name_entry, email_entry, address_entry, id_type_entry, occupation_entry,  annual_gross_income_entry))
        
        self.connection.commit()

        cursor.execute("SELECT LAST_INSERT_ID();")
        customer_id = int(cursor.fetchone()[0])

        create_checkings_query = """INSERT INTO checkings_account (customer_id, balance)
                                    VALUES (%s, %s);"""

        cursor.execute(create_checkings_query, (customer_id, balance_entry))
        self.connection.commit()

        cursor.execute("SELECT LAST_INSERT_ID();")
        checkings_id = int(cursor.fetchone()[0])

        create_bank_asset_query = """INSERT INTO bank_assets (checkings_id)
                                     VALUES (%s);"""

        cursor.execute(create_bank_asset_query, (checkings_id,))
        self.connection.commit()

        create_account_page_root.destroy()
        customer_accounts_page_root.destroy()
        messagebox.showinfo("Success", "New account created successfully!")
        self.customer_accounts_page(employee_id)

    def open_create_account_page(self, customer_accounts_page_root, employee_id):
        create_account_page_root = tk.Tk()
        create_account_page_root.geometry("480x270")
        create_account_page_root.title("Account Creation Page")

        create_acc_frame_left = tk.Frame(create_account_page_root)
        create_acc_frame_right = tk.Frame(create_account_page_root)

        # Content for left frame
        password_label = tk.Label(create_acc_frame_left, text="Password")
        password_label.pack(side="top", pady=2)
        password_entry = tk.Entry(create_acc_frame_left, width=20)
        password_entry.pack(side="top", pady=2)

        first_name_label = tk.Label(create_acc_frame_left, text="First Name")
        first_name_label.pack(side="top", pady=2)
        first_name_entry = tk.Entry(create_acc_frame_left, width=20)
        first_name_entry.pack(side="top", pady=2)

        last_name_label = tk.Label(create_acc_frame_left, text="Last Name")
        last_name_label.pack(side="top", pady=2)
        last_name_entry = tk.Entry(create_acc_frame_left, width=20)
        last_name_entry.pack(side="top", pady=2)

        email_label = tk.Label(create_acc_frame_left, text="Email")
        email_label.pack(side="top", pady=2)
        email_entry = tk.Entry(create_acc_frame_left, width=20)
        email_entry.pack(side="top", pady=2)

        address_label = tk.Label(create_acc_frame_left, text="Address")
        address_label.pack(side="top", pady=2)
        address_entry = tk.Entry(create_acc_frame_left, width=20)
        address_entry.pack(side="top", pady=2)
        
        create_acc_frame_left.pack(side="left", padx=10, fill="both", expand=True)

        # Content for right frame
        id_type_label = tk.Label(create_acc_frame_right, text="ID Type")
        id_type_label.pack(side="top", pady=2)
        id_type_entry = tk.Entry(create_acc_frame_right, width=20)
        id_type_entry.pack(side="top", pady=2)

        occupation_label = tk.Label(create_acc_frame_right, text="Occupation")
        occupation_label.pack(side="top", pady=2)
        occupation_entry = tk.Entry(create_acc_frame_right, width=20)
        occupation_entry.pack(side="top", pady=2)

        annual_gross_income_label = tk.Label(create_acc_frame_right, text="Annual gross Income")
        annual_gross_income_label.pack(side="top", pady=2)
        annual_gross_income_entry = tk.Entry(create_acc_frame_right, width=20)
        annual_gross_income_entry.pack(side="top", pady=2)

        balance_label = tk.Label(create_acc_frame_right, text="Balance")
        balance_label.pack(side="top", pady=2)
        balance_entry = tk.Entry(create_acc_frame_right, width=20)
        balance_entry.pack(side="top", pady=2)

        create_button = tk.Button(create_acc_frame_right, text="Create", command=lambda: self.create_button_clicked(password_entry, first_name_entry, last_name_entry, email_entry, address_entry, id_type_entry, occupation_entry, annual_gross_income_entry, balance_entry, create_account_page_root, employee_id, customer_accounts_page_root))
        create_button.pack(side="top", pady=26)
        
        create_acc_frame_right.pack(side="left", padx=10, fill="both", expand=True)

        create_account_page_root.mainloop()

    def delete_button_clicked(self, customer_id, delete_accounts_page_root, employee_id, customer_accounts_page_root):
        cursor = self.connection.cursor()
        successful = False

        try:
            customer_id = int(customer_id.get())

            # Delete bank_assets
            delete_bank_asset_row_query = """
                DELETE FROM bank_assets
                WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s);
            """
            cursor.execute(delete_bank_asset_row_query, (customer_id,))

            # Delete checkings_account
            delete_checkings_account_row_query = """
                DELETE FROM checkings_account
                WHERE customer_id = %s;
            """
            cursor.execute(delete_checkings_account_row_query, (customer_id,))

            # Delete customer_information
            delete_customer_information_row_query = """
                DELETE FROM customer_information
                WHERE customer_id = %s;
            """
            cursor.execute(delete_customer_information_row_query, (customer_id,))

            if cursor.rowcount > 0:
                self.connection.commit()
                successful = True
            else:
                raise Exception("No rows were deleted.")

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Unable to delete account. Error: {str(e)}")
            print(e)

        if successful:
            delete_accounts_page_root.destroy()            
            customer_accounts_page_root.destroy()            
            messagebox.showinfo("Success", "Account deleted successfully!")
            self.customer_accounts_page(employee_id)

    def open_delete_accounts_page(self, employee_id, customer_accounts_page_root):
        delete_accounts_page_root = tk.Tk()
        delete_accounts_page_root.geometry("300x200")
        delete_accounts_page_root.title("Delete Accounts Page")

        delete_account_page_frame = tk.Frame(delete_accounts_page_root, width=300,)

        delete_account_id_label = tk.Label(delete_account_page_frame, text="Account ID:")
        delete_account_id_entry = tk.Entry(delete_account_page_frame)

        delete_account_button = tk.Button(delete_account_page_frame, text="Delete", command=lambda: self.delete_button_clicked(delete_account_id_entry, delete_accounts_page_root, employee_id, customer_accounts_page_root))

        delete_account_page_frame.pack(expand=True, fill="none", side="top")
        delete_account_id_label.pack()
        delete_account_id_entry.pack()
        delete_account_button.pack(pady=10)

        delete_accounts_page_root.mainloop()

    def ecip_edit_button_clicked(self, customer_id, password, first_name, last_name, email, address, id_type, occupation, annual_gross_income, edit_personal_info_page_root, customer_accounts_page_root, employee_id):
        password_entry = password.get()
        first_name_entry = first_name.get()
        last_name_entry = last_name.get()
        email_entry = email.get()
        address_entry = address.get()
        id_type_entry = id_type.get()
        occupation_entry = occupation.get()
        annual_gross_income_entry = annual_gross_income.get()

        fields = {
            "customer_password": password_entry,
            "first_name": first_name_entry,
            "last_name": last_name_entry,
            "email": email_entry,
            "address": address_entry,
            "id_type": id_type_entry,
            "occupation": occupation_entry,
            "annual_gross_income": annual_gross_income_entry
        }

        # looks at the entries to see if it is empty or not, if it is not, it is added into the dictionary
        non_empty_fields = {key: value for key, value in fields.items() if value}

        if 'annual_gross_income' in non_empty_fields:
            try:
                annual_gross_income_float = float(non_empty_fields['annual_gross_income'])
                if annual_gross_income_float <= 0:
                    messagebox.showerror("Error", "Please input a positive number.")
                    return  
            except ValueError:
                messagebox.showerror("Error", "Annual Gross Income must be a valid number.")
                return 

        if non_empty_fields:
            edit_personal_info_query = f"""
                UPDATE customer_information
                SET {', '.join(f'{key} = %s' for key in non_empty_fields)}
                WHERE customer_id = %s
            """
            values = list(non_empty_fields.values()) + [customer_id]

            cursor = self.connection.cursor()
            cursor.execute(edit_personal_info_query, values)
            self.connection.commit()
            cursor.close()

            edit_personal_info_page_root.destroy()
            customer_accounts_page_root.destroy()
            messagebox.showinfo("Personal Information Edit Successful!", "Customer's information was updated successfully!")
            self.customer_accounts_page(employee_id)
            
    def edit_customer_info_page(self, customer_id, employee_id, customer_accounts_page_root):
        edit_personal_info_page_root = tk.Tk()
        edit_personal_info_page_root.geometry("400x400")
        edit_personal_info_page_root.title("Edit Personal Information Page")
        
        epi_page_main_frame = tk.Frame(edit_personal_info_page_root, width = 400, height = 300)
        main_page_frame1 = tk.Frame(epi_page_main_frame, width = 200, height = 300)
        main_page_frame2 = tk.Frame(epi_page_main_frame, width = 200, height = 300)
        epi_page_secondary_frame = tk.Frame(edit_personal_info_page_root, width = 400, height = 100)

        # content on frame 1 (Entry fields and labels for Password, first name, last name, email)
        password_label = tk.Label(main_page_frame1, text="Password")
        password_entry = tk.Entry(main_page_frame1)
        first_name_label = tk.Label(main_page_frame1, text="First Name")
        first_name_entry = tk.Entry(main_page_frame1)
        last_name_label = tk.Label(main_page_frame1, text="Last Name")
        last_name_entry = tk.Entry(main_page_frame1)
        email_label = tk.Label(main_page_frame1, text="Email")
        email_entry = tk.Entry(main_page_frame1)

        password_label.pack(side="top", padx=25, pady=10)
        password_entry.pack(side="top", padx=25, pady=10)
        first_name_label.pack(side="top", padx=25, pady=10)
        first_name_entry.pack(side="top", padx=25, pady=10)
        last_name_label.pack(side="top", padx=25, pady=10)
        last_name_entry.pack(side="top", padx=25, pady=10)
        email_label.pack(side="top", padx=25, pady=10)
        email_entry.pack(side="top", padx=25, pady=10)
        
        main_page_frame1.pack(side="left")

        # content on frame 2(Address, id type, occupation, annual gross income)
        address_label = tk.Label(main_page_frame2, text="Address")
        address_entry = tk.Entry(main_page_frame2)
        id_type_label = tk.Label(main_page_frame2, text="ID Type")
        id_type_entry = tk.Entry(main_page_frame2)
        occupation_label = tk.Label(main_page_frame2, text="Occupation")
        occupation_entry = tk.Entry(main_page_frame2)
        annual_gross_income_label = tk.Label(main_page_frame2, text="Annual Gross Income")
        annual_gross_income_entry = tk.Entry(main_page_frame2)

        address_label.pack(side="top", padx=25, pady=10)
        address_entry.pack(side="top", padx=25, pady=10)
        id_type_label.pack(side="top", padx=25, pady=10)
        id_type_entry.pack(side="top", padx=25, pady=10)
        occupation_label.pack(side="top", padx=25, pady=10)
        occupation_entry.pack(side="top", padx=25, pady=10)
        annual_gross_income_label.pack(side="top", padx=25, pady=10)
        annual_gross_income_entry.pack(side="top", padx=25, pady=10)

        main_page_frame2.pack(side="left")

        # content on secondary frame (Edit button)
        edit_buttton = tk.Button(epi_page_secondary_frame, text="Edit", command=lambda: self.ecip_edit_button_clicked(customer_id, password_entry, first_name_entry, last_name_entry, email_entry, address_entry, id_type_entry, occupation_entry, annual_gross_income_entry, edit_personal_info_page_root, customer_accounts_page_root, employee_id), width=10, height=2)
        edit_buttton.pack(side="top", padx=25, pady=10)

        epi_page_main_frame.pack(side="top")
        epi_page_secondary_frame.pack(side="top")
        edit_personal_info_page_root.mainloop()

    def oecip_edit_button_clicked(self, employee_id, edit_customer_info_page_root, customer_accounts_page_root, customer_id_entry):
        customer_id = customer_id_entry.get()
        cusrsor = self.connection.cursor()
        check_customer_id_query = "SELECT * FROM customer_information WHERE customer_id = %s"

        cusrsor.execute(check_customer_id_query, (customer_id,))
        result = cusrsor.fetchone()

        if result:
            edit_customer_info_page_root.destroy()
            self.edit_customer_info_page(customer_id, employee_id, customer_accounts_page_root)
        else:
            messagebox.showerror("Error!", "Customer ID does not exist.")
            return

    def open_edit_customer_info_page(self, employee_id, customer_accounts_page_root):
        edit_customer_info_page_root = tk.Tk()
        edit_customer_info_page_root.geometry("300x200")
        edit_customer_info_page_root.title("Edit Accounts Page")

        edit_customer_info_page_frame = tk.Frame(edit_customer_info_page_root, width=300,)

        edit_customer_id_label = tk.Label(edit_customer_info_page_frame, text="Custmer ID:")
        edit_customer_id_entry = tk.Entry(edit_customer_info_page_frame)

        delete_account_button = tk.Button(edit_customer_info_page_frame, text="Edit", command=lambda: self.oecip_edit_button_clicked(employee_id, edit_customer_info_page_root, customer_accounts_page_root, edit_customer_id_entry))

        edit_customer_info_page_frame.pack(expand=True, fill="none", side="top")
        edit_customer_id_label.pack()
        edit_customer_id_entry.pack()
        delete_account_button.pack(pady=10)

        edit_customer_info_page_root.mainloop()

    # functions used in customer transactions page
    def get_transactions(self):
        cursor = self.connection.cursor()
        get_transactions_query = "SELECT * from transactions"
        cursor.execute(get_transactions_query)

        transactions_rows = cursor.fetchall()

        column_names = ["Transaction ID", "Checkings ID", "Date", "Time", "Amount", "Transaction Type"]

        transactions = tabulate(transactions_rows, headers=column_names, tablefmt='grid')

        cursor.close()

        return transactions
    
    def customer_accounts_button_clicked(self, transaction_page_root, customer_id):
        transaction_page_root.destroy()
        self.customer_accounts_page(customer_id)

    def open_search_transactions_page(self):
        search_transactions_page_root = tk.Tk()
        search_transactions_page_root.geometry("300x200")
        search_transactions_page_root.title("Search Transactions Page")

        search_frame = tk.Frame(search_transactions_page_root, width=300,)

        search_transaction_id_label = tk.Label(search_frame, text="Transaction ID:")
        search_transaction_id_entry = tk.Entry(search_frame)

        search_transaction_button = tk.Button(search_frame, text="Search", command=lambda: self.search_transaction_button_clicked(search_transaction_id_entry, search_transactions_page_root))

        search_frame.pack(expand=True, fill="none", side="top")
        search_transaction_id_label.pack()
        search_transaction_id_entry.pack()
        search_transaction_button.pack(pady=10)

        search_transactions_page_root.mainloop()

    # search accounts page and search transactions page navigation
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

    def search_transaction_button_clicked(self, transaction_id ,search_transactions_page):
        transaction_id = transaction_id.get()
        
        if self.search_transactions(transaction_id, 1):
            search_transactions_page.destroy()            
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

    # main pages
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

    def customer_accounts_page(self, employee_id):
        customer_accounts_page_root = tk.Tk()
        customer_accounts_page_root.geometry("900x500")
        customer_accounts_page_root.title("Customer Accounts Page")

        # frames
        ca_page_secondary_frame = tk.Frame(customer_accounts_page_root, width = 300, height = 500)
        ca_page_main_frame = tk.Frame(customer_accounts_page_root, width = 700, height = 500)

        # content on secondary frame (Employee Name and Buttons)
        first_name, last_name = self.get_name(employee_id, 1)
        employee_name_label = tk.Label(ca_page_secondary_frame, text=f"Welcome {first_name} {last_name}!")
        employee_name_label.pack(side="top", pady=10)

        ca_page_secondary_frame.pack(side="top", fill="y")

        search_button = tk.Button(ca_page_secondary_frame, text="Search", command=lambda: self.open_search_account_page())
        view_transactions_button = tk.Button(ca_page_secondary_frame, text="Transactions", command=lambda: self.transactions_button_clicked(customer_accounts_page_root, employee_id))
        create_customer_accounts = tk.Button(ca_page_secondary_frame, text="Create Accounts", command=lambda: self.open_create_account_page(customer_accounts_page_root, employee_id))
        delete_accounts = tk.Button(ca_page_secondary_frame, text="Delete Accounts", command=lambda: self.open_delete_accounts_page(employee_id, customer_accounts_page_root))
        edit_customer_information = tk.Button(ca_page_secondary_frame, text="Edit Customer Information", command=lambda: self.open_edit_customer_info_page(employee_id, customer_accounts_page_root))
        logout_button = tk.Button(ca_page_secondary_frame, text="Log Out", command=lambda: self.logout_button_clicked(customer_accounts_page_root))

        search_button.pack(side="left", padx=5)
        view_transactions_button.pack(side="left", padx=5)
        create_customer_accounts.pack(side="left", padx=5)
        delete_accounts.pack(side="left", padx=5)
        edit_customer_information.pack(side="left", padx=5)
        logout_button.pack(side="left", pady=10)

        # content on main frame
        account_info = self.get_customer_info()
        account_info_text = tk.Text(ca_page_main_frame, height=10, width=50, wrap=tk.NONE)
        account_info_text.insert(tk.END, account_info)
        account_info_text.config(state="disabled")
        account_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # scrollbars for the table if it has many content
        vertical_scrollbar = tk.Scrollbar(ca_page_main_frame, command=account_info_text.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        account_info_text.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(ca_page_main_frame, orient=tk.HORIZONTAL, command=account_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")  # Place it at the top
        account_info_text.config(xscrollcommand=horizontal_scrollbar.set)

        ca_page_main_frame.pack(side="top", fill="both", expand=True)
        ca_page_main_frame.grid_rowconfigure(0, weight=1)
        ca_page_main_frame.grid_columnconfigure(0, weight=1)

    def customer_transactions_page(self, employee_id):
        customer_transactions_page_root = tk.Tk()
        customer_transactions_page_root.geometry("900x500")
        customer_transactions_page_root.title("Customer Transactions Page")

        ct_page_secondary_frame = tk.Frame(customer_transactions_page_root, width = 300, height = 500)
        ct_page_main_frame = tk.Frame(customer_transactions_page_root, width = 900, height = 300)

        # content on secondary frame (Employee Name and Buttons)
        first_name, last_name = self.get_name(employee_id, 1)
        employee_name_label = tk.Label(ct_page_secondary_frame, text=f"Welcome {first_name} {last_name}!")
        employee_name_label.pack(side="top", pady=10)

        ct_page_secondary_frame.pack(side="top", fill="y")

        search_button = tk.Button(ct_page_secondary_frame, text="Search", command=lambda: self.open_search_transactions_page())
        customer_accounts_button = tk.Button(ct_page_secondary_frame, text="Customer Accounts", command=lambda: self.customer_accounts_button_clicked(customer_transactions_page_root, employee_id))
        logout_button = tk.Button(ct_page_secondary_frame, text="Log Out", command=lambda: self.logout_button_clicked(customer_transactions_page_root))

        search_button.pack(side="left", padx=5)
        customer_accounts_button.pack(side="left", padx=5)
        logout_button.pack(side="left", pady=10)
        
        # content on main frame
        transaction_info = self.get_transactions()
        transaction_info_text = tk.Text(ct_page_main_frame, height=10, width=93, wrap=tk.NONE)
        transaction_info_text.insert(tk.END, transaction_info)
        transaction_info_text.config(state="disabled")
        transaction_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # scrollbar for the table if it has many contents
        vertical_scrollbar = tk.Scrollbar(ct_page_main_frame, command=transaction_info_text.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        transaction_info_text.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(ct_page_main_frame, orient=tk.HORIZONTAL, command=transaction_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")  # Place it at the top
        transaction_info_text.config(xscrollcommand=horizontal_scrollbar.set)
        
        ct_page_main_frame.pack(side="top", fill="y", expand=True)

        ct_page_main_frame.columnconfigure(0, weight=1)
        ct_page_main_frame.rowconfigure(0, weight=1)
        
        customer_transactions_page_root.mainloop()

# testing        
# create_instance = Employee()
# create_instance.connect()
# create_instance.login_page()

        
