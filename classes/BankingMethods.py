from abc import ABC, abstractmethod
from DatabaseConnector import DatabaseConnector
from tkinter import messagebox
import tkinter as tk

class BankingMethods(ABC, DatabaseConnector):

    def check_database_connection(self):
        if self.connection is not None:
            return True
        else:
            return False
    
    def login(self, login_root, id_entry, password_entry, type):
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
                messagebox.showinfo("Login Successful", "Login Successful")
                login_root.destroy() # closes login page
                self.main_page(id_entry)
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

    @abstractmethod
    def get_transactions(self):
        pass
