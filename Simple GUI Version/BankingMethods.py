from abc import ABC, abstractmethod
from DatabaseConnector import DatabaseConnector
from tkinter import messagebox
from tabulate import tabulate
import tkinter as tk

class BankingMethods(ABC, DatabaseConnector):
    def check_database_connection(self):
        if self.connection is not None:
            return True
        else:
            return False
    
    def login(self, login_page_root, id_entry, password_entry, type):
        id_entry = id_entry.get()
        password_entry = password_entry.get()

        cursor = self.connection.cursor()

        if type == 1:
            employee_login_query = "SELECT employee_id, employee_password FROM employees WHERE employee_id = %s"
            cursor.execute(employee_login_query, (id_entry,))
        else:
            customer_login_query = "SELECT customer_id, customer_password FROM customer_information WHERE customer_id = %s"
            cursor.execute(customer_login_query, (id_entry,))

        login_query_result = cursor.fetchone() 

        if login_query_result:
            stored_user_id, stored_user_password = login_query_result
            if password_entry == stored_user_password:
                cursor.close()
                if type == 1:                    
                    login_page_root.destroy()                     
                    messagebox.showinfo("Login Successful", "Login Successful")
                    self.customer_accounts_page(id_entry)

                elif type == 2:
                    login_page_root.destroy()                     
                    messagebox.showinfo("Login Successful", "Login Successful")
                    self.personal_transaction_page(id_entry)

            else:
                cursor.close()
                messagebox.showerror("Login Failed", "Incorrect ID/Password")
        else:
            cursor.close()
            messagebox.showerror("Login Failed", "Incorrect ID/Password")

    def get_name(self, id_entry, type):
        cursor = self.connection.cursor()

        if type == 1:
            employee_name_query = "SELECT first_name, last_name FROM employees WHERE employee_id = %s"
            cursor.execute(employee_name_query, (id_entry,))
            
            name_query_result = cursor.fetchone()

            if name_query_result:
                first_name, last_name = name_query_result
                return first_name, last_name

            else: # for instances where there is an employee id and password in the database but the name isn't added
                first_name, last_name = "N/A"
                return first_name, last_name

        else:
            customer_name_balance_query = """
                    SELECT customer_information.first_name, customer_information.last_name, checkings_account.balance
                    FROM customer_information 
                    LEFT JOIN checkings_account ON customer_information.customer_id = checkings_account.customer_id
                    WHERE customer_information.customer_id = %s
                    """
            cursor.execute(customer_name_balance_query, (id_entry,))

            cb_query_result = cursor.fetchone()

            if cb_query_result:
                first_name, last_name, balance = cb_query_result

                if balance is not None:
                    return first_name, last_name, balance
                else:
                    balance = "Balance Not Found"
                    return first_name, last_name, balance

            else: # for instances where there is an employee id and password in the database but the name isn't added
                first_name, last_name = "N/A"
                return first_name, last_name, balance

    def search_transactions(self, id_entry, type):
        cursor = self.connection.cursor()

        if type == 1:
            search_transactions_query = "SELECT * FROM transactions WHERE transaction_id = %s"

            cursor.execute(search_transactions_query, (id_entry,))
            transaction_row = cursor.fetchone() 

            if transaction_row:
                column_names = ["Transaction ID", "Checkings ID", "Date", "Time", "Amount", "Transaction Type"]
                transactions = tabulate([transaction_row], headers=column_names, tablefmt='grid')
                cursor.close()
                return transactions
            
            else:
                cursor.close()
                messagebox.showerror("Search Failed", "No Transactions with that ID")

        else: 
            search_transactions_query = "SELECT * FROM transactions WHERE checkings_id = %s"

            cursor.execute(search_transactions_query, (id_entry,))
            transactions_rows = cursor.fetchall() 

            column_names = ["Transaction ID", "Checkings ID", "Date", "Time", "Amount", "Transaction Type"]
            transactions = tabulate(transactions_rows, headers=column_names, tablefmt='grid')
            cursor.close()
            return transactions
        
    def search_accounts(self, id_entry, type):
        cursor = self.connection.cursor()

        if type == 1:
            search_accounts_query = """
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
                    customer_information.customer_id = %s;
            """

            cursor.execute(search_accounts_query, (id_entry,))
            account_row = cursor.fetchone() 

            if account_row:
                column_names = ["Customer ID", "Password", "First Name", "Last Name", 
                                "Email", "Address", "ID Type", "Occupation", 
                                "Annual Gross Income", "Checkings ID", "Balance"]
                account_info = tabulate([account_row], headers=column_names, tablefmt='grid')
                cursor.close()
                return account_info
            
            else:
                cursor.close()
                messagebox.showerror("Search Failed", "No Accounts with that ID")

        else: 
            search_accounts_query = """
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
                    checkings_account.checkings_id
                FROM 
                    customer_information 
                JOIN 
                    checkings_account 
                ON 
                    customer_information.customer_id = checkings_account.customer_id
                WHERE
                    customer_information.customer_id = %s;
            """

            cursor.execute(search_accounts_query, (id_entry,))
            account_rows = cursor.fetchall() 

            column_names = ["Customer ID", "Password", "First Name", "Last Name", 
                            "Email", "Address", "ID Type", "Occupation", 
                            "Annual Gross Income", "Checkings ID"]
            
            account_info = tabulate(account_rows, headers=column_names, tablefmt='grid')
            cursor.close()
            return account_info
