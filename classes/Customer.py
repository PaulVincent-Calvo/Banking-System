from BankingMethods import BankingMethods
from tkinter import messagebox
from tabulate import tabulate
from datetime import datetime
import tkinter as tk

class Customer(BankingMethods):
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
    
    # functions used in personal transaction page
    def search_button_clicked(self, transaction_id_entry, search_transactions_page_root, customer_id):
        transaction_id_entry = transaction_id_entry.get()

        transaction_info = self.search_transactions(transaction_id_entry, 1)

        if transaction_info:
            checkings_id_from_transaction = int(transaction_info.split()[21])
            # print(checkings_id_from_transaction)

            cursor = self.connection.cursor()
            get_checkings_id_query = "SELECT checkings_id FROM checkings_account WHERE customer_id = %s"

            cursor.execute(get_checkings_id_query, (customer_id,))
            customer_checkings_id = int(cursor.fetchone()[0])
            # print(customer_checkings_id)

            cursor.close()  
        
            if checkings_id_from_transaction == customer_checkings_id:
                search_transactions_page_root.destroy()
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

    def open_search_transactions_page(self, customer_id):
        search_transactions_page_root = tk.Tk()
        search_transactions_page_root.geometry("300x200")
        search_transactions_page_root.title("Search Transactions Page")
        search_frame = tk.Frame(search_transactions_page_root, width=300,)

        search_transaction_id_label = tk.Label(search_frame, text="Transaction ID:")
        search_transaction_id_entry = tk.Entry(search_frame)

        search_transaction_button = tk.Button(search_frame, text="Search", command=lambda: self.search_button_clicked(search_transaction_id_entry, search_transactions_page_root, customer_id))

        search_frame.pack(expand=True, fill="none", side="top")
        search_transaction_id_label.pack()
        search_transaction_id_entry.pack()
        search_transaction_button.pack(pady=10)

        search_transactions_page_root.mainloop()
    
    def withdraw_button_clicked(self, withdrawal_amount_entry, withdrawal_page_root, customer_id, personal_transaction_page_root):
        try:
            withdrawal_amount = float(withdrawal_amount_entry.get())
            formatted_withdrawal_amount = "{:.2f}".format(withdrawal_amount) # format as float w/ 2 decimals
            # print(formatted_withdrawal_amount)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid withdrawal amount. Please enter a valid number.")
            return

        cursor = self.connection.cursor()
        get_checkings_id_query = "SELECT checkings_id FROM checkings_account WHERE customer_id = %s"

        cursor.execute(get_checkings_id_query, (customer_id,))
        customer_checkings_id = int(cursor.fetchone()[0])

        get_balance_query = "SELECT balance FROM checkings_account WHERE checkings_id = %s"

        cursor.execute(get_balance_query, (customer_checkings_id,))
        customer_balance = cursor.fetchone()[0]

        formatted_customer_balance = "{:.2f}".format(customer_balance)
        # print(formatted_customer_balance)
        
        float_formatted_withdrawal_amount = float(formatted_withdrawal_amount)
        float_formatted_customer_balance = float(formatted_customer_balance)

        if float_formatted_withdrawal_amount < float_formatted_customer_balance:
            # print("Withdrawal amount is lower than the balance. Transaction complete")
            new_balance = float_formatted_customer_balance - float_formatted_withdrawal_amount

            update_balance_query = "UPDATE checkings_account SET balance = %s WHERE checkings_id = %s"
            cursor.execute(update_balance_query, (new_balance, customer_checkings_id))
            self.connection.commit()
            
            add_transaction_query = """INSERT INTO transactions(checkings_id, transaction_date, transaction_time, amount, transaction_type)
                                 VALUES (%s, %s, %s, %s, %s)"""
            current_datetime = datetime.now()
            cursor.execute(add_transaction_query, (customer_checkings_id, current_datetime.date(), current_datetime.time(), float_formatted_withdrawal_amount, "Withdrawal"))
            self.connection.commit()

            cursor.close()
            personal_transaction_page_root.destroy()
            messagebox.showinfo("Withdrawal Successful!", "${:.2f} successfully withdrawn from your account!".format(float_formatted_withdrawal_amount))
            self.personal_transaction_page(customer_id)
        else:
            messagebox.showerror("Error: Broke homie alert!", "Insufficient funds for this withdrawal")

    def open_withdrawal_page(self, customer_id, personal_transaction_page_root):
        withdraw_page_root = tk.Tk()
        withdraw_page_root.geometry("300x200")
        withdraw_page_root.title("Withdrawal Page")
        withdraw_frame = tk.Frame(withdraw_page_root, width=300,)

        withdraw_amount_label = tk.Label(withdraw_frame, text="Enter the amount you'd like to withdraw:")
        withdawal_amount_entry = tk.Entry(withdraw_frame)

        withdraw_button = tk.Button(withdraw_frame, text="Withdraw", command=lambda: self.withdraw_button_clicked(withdawal_amount_entry, withdraw_page_root, customer_id, personal_transaction_page_root))

        withdraw_frame.pack(expand=True, fill="none", side="top")
        withdraw_amount_label.pack()
        withdawal_amount_entry.pack()
        withdraw_button.pack(pady=10)

        withdraw_page_root.mainloop()
    
    def deposit_button_clicked(self, deposit_amount_entry, deposit_page_root, customer_id, personal_transaction_page_root):
        try:
            deposit_amount = float(deposit_amount_entry.get())
            formatted_deposit_amount = "{:.2f}".format(deposit_amount) # format as float w/ 2 decimals
            # print(formatted_deposit_amount)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return

        cursor = self.connection.cursor()
        get_checkings_id_query = "SELECT checkings_id FROM checkings_account WHERE customer_id = %s"

        cursor.execute(get_checkings_id_query, (customer_id,))
        customer_checkings_id = int(cursor.fetchone()[0])
        # print(customer_checkings_id)
        get_balance_query = "SELECT balance FROM checkings_account WHERE checkings_id = %s"

        cursor.execute(get_balance_query, (customer_checkings_id,))
        customer_balance = cursor.fetchone()[0]

        formatted_customer_balance = "{:.2f}".format(customer_balance)
        # print(formatted_customer_balance)
        
        float_formatted_deposit_amount = float(formatted_deposit_amount)
        float_formatted_customer_balance = float(formatted_customer_balance)

        if float_formatted_deposit_amount > 0:
            # print("Deposit amount is not negative. Transaction complete")
            new_balance = float_formatted_customer_balance + float_formatted_deposit_amount

            update_balance_query = "UPDATE checkings_account SET balance = %s WHERE checkings_id = %s"
            cursor.execute(update_balance_query, (new_balance, customer_checkings_id))
            self.connection.commit()
            
            add_transaction_query = """INSERT INTO transactions(checkings_id, transaction_date, transaction_time, amount, transaction_type)
                                 VALUES (%s, %s, %s, %s, %s)"""
            current_datetime = datetime.now()
            cursor.execute(add_transaction_query, (customer_checkings_id, current_datetime.date(), current_datetime.time(), float_formatted_deposit_amount, "Deposit"))
            self.connection.commit()

            cursor.close()
            personal_transaction_page_root.destroy()
            messagebox.showinfo("Deposit Successful!", "${:.2f} successfully added to your account!".format(float_formatted_deposit_amount))
            self.personal_transaction_page(customer_id)
        else:
            messagebox.showerror("Error", "The amount you entered is negative.")

    def open_deposit_page(self, customer_id, personal_transaction_page_root):
        deposit_page_root = tk.Tk()
        deposit_page_root.geometry("300x200")
        deposit_page_root.title("Deposit Page")
        deposit_frame = tk.Frame(deposit_page_root, width=300,)

        deposit_amount_label = tk.Label(deposit_frame, text="Enter the amount you'd like to deposit:")
        deposit_amount_entry = tk.Entry(deposit_frame)

        deposit_button = tk.Button(deposit_frame, text="Deposit", command=lambda: self.deposit_button_clicked(deposit_amount_entry, deposit_page_root, customer_id, personal_transaction_page_root))

        deposit_frame.pack(expand=True, fill="none", side="top")
        deposit_amount_label.pack()
        deposit_amount_entry.pack()
        deposit_button.pack(pady=10)

        deposit_page_root.mainloop()
    
    # functions used in personal info page
    def edit_button_clicked(self, customer_id, password, first_name, last_name, email, address, id_type, occupation, annual_gross_income, edit_personal_info_page_root,personal_info_page_root):
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
            personal_info_page_root.destroy()
            messagebox.showinfo("Personal Information Edit Successful!", "Your personal information was updated successfully!")
            self.personal_info_page(customer_id)

    def open_edit_personal_info_page(self, customer_id, personal_info_page_root):
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
        edit_buttton = tk.Button(epi_page_secondary_frame, text="Edit", command=lambda: self.edit_button_clicked(customer_id, password_entry, first_name_entry, last_name_entry, email_entry, address_entry, id_type_entry, occupation_entry, annual_gross_income_entry, edit_personal_info_page_root, personal_info_page_root), width=10, height=2)
        edit_buttton.pack(side="top", padx=25, pady=10)

        epi_page_main_frame.pack(side="top")
        epi_page_secondary_frame.pack(side="top")
        edit_personal_info_page_root.mainloop()
        
    # personal transaction page and personal info page navigation
    def transaction_page_button_clicked(self, customer_id, personal_info_page_root):
        personal_info_page_root.destroy()
        self.personal_transaction_page(customer_id)

    def personal_information_page_button_clicked(self, customer_id, personal_transaction_page_root):
        personal_transaction_page_root.destroy()
        self.personal_info_page(customer_id)

    def logout_button_clicked(self, page_root):
        page_root.destroy()
        messagebox.showinfo("Logout Successful", "Account was logged out successfully.")        
        self.login_page()        

    # main pages
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

    def personal_transaction_page(self, customer_id):
        personal_transaction_page_root = tk.Tk()
        personal_transaction_page_root.geometry("900x500")
        personal_transaction_page_root.title("Transactions Page")

        # frames
        pt_page_secondary_frame = tk.Frame(personal_transaction_page_root, width = 300, height = 500)
        pt_page_main_frame = tk.Frame(personal_transaction_page_root, width = 700, height = 500)

        # content on secondary frame (Customer Name, Balance, and Buttons)
        first_name, last_name, balance = self.get_name(customer_id, 2)
        customer_name_label = tk.Label(pt_page_secondary_frame, text=f"Welcome {first_name} {last_name}!")
        customer_balance_label = tk.Label(pt_page_secondary_frame, text=f"Balance: ${balance}")
        customer_name_label.pack(side="top", pady=10)
        customer_balance_label.pack(side="top", padx=10, pady=10)

        search_transaction_button = tk.Button(pt_page_secondary_frame, text="Search Transaction", command=lambda: self.open_search_transactions_page(customer_id))
        view_personal_info_button = tk.Button(pt_page_secondary_frame, text="Personal Information Page", command=lambda: self.personal_information_page_button_clicked(customer_id, personal_transaction_page_root))
        withdraw_button = tk.Button(pt_page_secondary_frame, text="Withdraw", command=lambda: self.open_withdrawal_page(customer_id, personal_transaction_page_root))
        deposit_button = tk.Button(pt_page_secondary_frame, text="Deposit", command=lambda: self.open_deposit_page(customer_id, personal_transaction_page_root))
        logout_button =  tk.Button(pt_page_secondary_frame, text="Log Out", command=lambda: self.logout_button_clicked(personal_transaction_page_root))

        search_transaction_button.pack(side="left", padx=5)
        view_personal_info_button.pack(side="left", padx=5)
        withdraw_button.pack(side="left", padx=5)
        deposit_button.pack(side="left", padx=5)
        logout_button.pack(side="left", padx=5)

        pt_page_secondary_frame.pack(side="top", fill="y")

        cursor = self.connection.cursor()
        get_checkings_id_query = "SELECT checkings_id FROM checkings_account WHERE customer_id = %s"

        cursor.execute(get_checkings_id_query, (customer_id,))
        customer_checkings_id = int(cursor.fetchone()[0])

        # content on main frame
        transaction_info = self.search_transactions(customer_checkings_id, 2)
        transaction_info_text = tk.Text(pt_page_main_frame, height=10, width=93, wrap=tk.NONE)
        transaction_info_text.insert(tk.END, transaction_info)
        transaction_info_text.config(state="disabled")
        transaction_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # scrollbars for the table if it has many content
        vertical_scrollbar = tk.Scrollbar(pt_page_main_frame, command=transaction_info_text.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        transaction_info_text.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(pt_page_main_frame, orient=tk.HORIZONTAL, command=transaction_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")  
        transaction_info_text.config(xscrollcommand=horizontal_scrollbar.set)

        pt_page_main_frame.pack(side="top", fill="y", expand=True)
        pt_page_main_frame.grid_rowconfigure(0, weight=1)
        pt_page_main_frame.grid_columnconfigure(0, weight=1)

        personal_transaction_page_root.mainloop()
    
    def personal_info_page(self, customer_id):
        personal_info_page_root = tk.Tk()
        personal_info_page_root.geometry("900x500") 
        personal_info_page_root.title("Personal Information Page")

        # frames
        pi_page_secondary_frame = tk.Frame(personal_info_page_root, width = 300, height = 100)
        pi_page_main_frame = tk.Frame(personal_info_page_root, width = 700, height = 500) 

        # content on secondary frame (Customer Name and Buttons)
        first_name, last_name, balance = self.get_name(customer_id, 2)
        customer_name_label = tk.Label(pi_page_secondary_frame, text=f"Welcome {first_name} {last_name}!")
        customer_name_label.pack(side="top", pady=10)

        view_transactions_button = tk.Button(pi_page_secondary_frame, text="Transaction Page", command=lambda: self.transaction_page_button_clicked(customer_id, personal_info_page_root))
        edit_personal_information = tk.Button(pi_page_secondary_frame, text="Edit Personal Information", command=lambda: self.open_edit_personal_info_page(customer_id, personal_info_page_root))
        logout_button = tk.Button(pi_page_secondary_frame, text="Log Out", command=lambda: self.logout_button_clicked(personal_info_page_root))

        view_transactions_button.pack(side="left", padx=5)
        edit_personal_information.pack(side="left", padx=5)
        logout_button.pack(side="left", padx=5)

        pi_page_secondary_frame.pack(side="top", pady=7)  

        # content on main frame
        account_info = self.search_accounts(customer_id, 2)
        account_info_text = tk.Text(pi_page_main_frame, height=1, width=93, wrap=tk.NONE)
        account_info_text.insert(tk.END, account_info)
        account_info_text.config(state="disabled")
        account_info_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  

        # scrollbar for the table if it has many content
        horizontal_scrollbar = tk.Scrollbar(pi_page_main_frame, orient=tk.HORIZONTAL, command=account_info_text.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew") 
        account_info_text.config(xscrollcommand=horizontal_scrollbar.set)

        pi_page_main_frame.pack(side="top", fill="y", expand=True)
        pi_page_main_frame.grid_rowconfigure(0, weight=1)
        pi_page_main_frame.grid_columnconfigure(0, weight=1)

        personal_info_page_root.mainloop()


# testing
# personal_info_page_root = tk.Tk()
# instance = Customer()
# instance.connect()
# # instance.open_edit_personal_info_page(1, personal_info_page_root)
# instance.login_page()
