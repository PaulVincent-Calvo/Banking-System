from DatabaseConnector import DatabaseConnector
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess

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

    def submit_login(self, username, password):
        try:
             connection = self.connect_database()
             cursor = connection.cursor()
             
             query = "SELECT * FROM employees WHERE employee_id = %s AND employee_password = %s"
             cursor.execute(query, (username, password)) 
             result = cursor.fetchone()
             if result:
                return True
             else:
                print("User does not exist in the database")
                return False
             
        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:

            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()


        
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

        # def deposit_money():
        #     user_id = id_entry.get()

        #     cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        #     user = cursor.fetchone()

        #     if user:
        #         amount = float(deposit_entry.get())

        #         if amount > 0:
        #             updated_balance = user[3] + amount
        #             cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (updated_balance, user_id))
        #             conn.commit()
        #             status_label.config(text=f"${amount:.2f} deposited successfully! New balance: ${updated_balance:.2f}")
        #         else:
        #             status_label.config(text="Please enter a valid deposit amount.")
        #     else:
        #         status_label.config(text="User not found.")

        # def withdraw_money():
        #     user_id = id_entry.get()

        #     cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        #     user = cursor.fetchone()

        #     if user:
        #         amount = float(withdraw_entry.get())

        #         if amount > 0 and user[3] >= amount:
        #             updated_balance = user[3] - amount
        #             cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (updated_balance, user_id))
        #             conn.commit()
        #             status_label.config(text=f"${amount:.2f} withdrawn successfully! New balance: ${updated_balance:.2f}")
        #         else:
        #             status_label.config(text="Withdrawal failed. Please check the amount or balance.")
        #     else:
        #         status_label.config(text="User not found.")

        # def transfer_balance():
        #     sender_id = sender_entry.get()
        #     receiver_id = receiver_entry.get()

        #     sender_cursor = conn.cursor()
        #     sender_cursor.execute("SELECT * FROM users WHERE id = ?", (sender_id,))
        #     sender = sender_cursor.fetchone()
        
        #     receiver_cursor = conn.cursor()
        #     receiver_cursor.execute("SELECT * FROM users WHERE id = ?", (receiver_id,))
        #     receiver = receiver_cursor.fetchone()
        
        #     transfer_amount = float(transfer_entry.get())
        
        #     if sender and receiver and transfer_amount > 0 and sender[3] >= transfer_amount:
        #         sender_updated_balance = sender[3] - transfer_amount
        #         receiver_updated_balance = receiver[3] + transfer_amount
        
        #         sender_cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (sender_updated_balance, sender_id))
        #         receiver_cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (receiver_updated_balance, receiver_id))
        
        #         conn.commit()
        #         status_label.config(text=f"${transfer_amount:.2f} transferred from User {sender_id} to User {receiver_id}.")
        #     else:
        #         status_label.config(text="Transfer failed. Please check IDs and ensure sufficient balance.")

        main_root.mainloop()
        
        
customer = Customer()
customer.show_connection_status()
