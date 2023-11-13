from DatabaseConnector import DatabaseConnector
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Customer(DatabaseConnector):
    def __init__(self):
        super().__init__()  # Initialize the parent class

    def check_database_connection(self):
        if self.connection is not None:
            return True
        else:
            return False

    def show_connection_status(self):
        login_root = tk.Tk()
        login_root.title("Customer Login Page")
        try:
            self.connect_database()
            if self.check_database_connection():
                self.login_page(login_root)

        except Exception as e:
            messagebox.showerror("Database Connection Error", str(e))

        login_root.mainloop()

    def submit_login(self, login_root, customer_id_entry, customer_password_entry):
        customer_id_entry = customer_id_entry.get()
        customer_password_entry = customer_password_entry.get()

        cursor = self.connection.cursor()
        customer_login_query = "SELECT customer_id, customer_password FROM customer_information WHERE customer_id = %s"
        cursor.execute(customer_login_query, (customer_id_entry,))

        cl_query_result = cursor.fetchone() 

        if cl_query_result:
            stored_user_id, stored_user_password = cl_query_result
            if customer_password_entry == stored_user_password:
                cursor.close()
                messagebox.showinfo("Login Successful", "Login Successful")
                login_root.destroy() 
                self.main_page(customer_id_entry)
            else:
                cursor.close()
                messagebox.showerror("Login Failed", "Incorrect ID/Password")
        else:
            cursor.close()
            messagebox.showerror("Login Failed", "Incorrect ID/Password")

    def login_page(self, login_root):
        login_root.geometry("300x200")

        login_frame = tk.Frame(login_root, width = 300, height = 200)
        login_frame.pack(expand=True)

        label_id = tk.Label(login_frame, text="ID:")
        label_password = tk.Label(login_frame, text="Password:")

        customer_id_entry = tk.Entry(login_frame)
        customer_password_entry = tk.Entry(login_frame, show="*")  # replaces input with "*"s for security

        login_button = tk.Button(login_frame, text="Login", command=lambda: self.submit_login(login_root, customer_id_entry, customer_password_entry))

        # layout 
        login_frame.pack(expand=True, fill="none", side="top")
        label_id.pack()
        customer_id_entry.pack()
        label_password.pack()
        customer_password_entry.pack()

        login_button.pack(pady=20)

    def main_page(self, customer_id_entry):
        main_root = tk.Tk()
        main_root.title("Employee Main Page")
        main_root.geometry("500x400")

        cursor = self.connection.cursor()
        customer_name_balance_query = """
                SELECT customer_information.first_name, customer_information.last_name, checkings_account.balance
                FROM customer_information 
                LEFT JOIN checkings_account ON customer_information.customer_id = checkings_account.customer_id
                WHERE customer_information.customer_id = %s
                """

        cursor.execute(customer_name_balance_query, (customer_id_entry,))
        cb_query_result = cursor.fetchone()

        if cb_query_result:
            first_name, last_name, balance = cb_query_result
            customer_name_label = tk.Label(main_root, text=f"Welcome {first_name} {last_name}!")
            customer_name_label.pack()

            if balance is not None:
                balance_label = tk.Label(main_root, text=f"Your Balance: {balance:.2f}")
                balance_label.pack()
            else:
                balance_label = tk.Label(main_root, text="Balance Information not found")
                balance_label.pack()

        else: # for instances where there is an employee id and password in the database but the name isn't added
            customer_name_label = tk.Label(main_root, text="Employee Name not found")
            customer_name_label.pack()

        main_root.mainloop()
        
        
customer = Customer()
customer.show_connection_status()