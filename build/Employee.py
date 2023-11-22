from DatabaseConnector import DatabaseConnector
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Employee(DatabaseConnector):
    def __init__(self):
        super().__init__()  # Initialize the parent class

    def check_database_connection(self):
        if self.connection is not None:
            return True
        else:
            return False

    def show_connection_status(self):
        login_root = tk.Tk()
        login_root.title("Employee Login Page")
        try:
            self.connect_database()
            if self.check_database_connection():
                self.login_page(login_root)

        except Exception as e:
            messagebox.showerror("Database Connection Error", str(e))

        login_root.mainloop()

    def submit_login(self, login_root, employee_id_entry, employee_password_entry):
        employee_id_entry = employee_id_entry.get()
        employee_password_entry = employee_password_entry.get()

        cursor = self.connection.cursor()
        employee_login_query = "SELECT employee_id, employee_password FROM employees WHERE employee_id = %s"
        cursor.execute(employee_login_query, (employee_id_entry,))

        el_query_result = cursor.fetchone() 

        if el_query_result:
            stored_user_id, stored_user_password = el_query_result
            if employee_password_entry == stored_user_password:
                cursor.close()
                messagebox.showinfo("Login Successful", "Login Successful")
                login_root.destroy() 
                self.main_page(employee_id_entry)
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

        employee_id_entry = tk.Entry(login_frame)
        employee_password_entry = tk.Entry(login_frame, show="*")  # replaces input with "*"s for security

        login_button = tk.Button(login_frame, text="Login", command=lambda: self.submit_login(login_root, employee_id_entry, employee_password_entry))

        # layout 
        login_frame.pack(expand=True, fill="none", side="top")
        label_id.pack()
        employee_id_entry.pack()
        label_password.pack()
        employee_password_entry.pack()

        login_button.pack(pady=20)

    def main_page(self, employee_id_entry):
        main_root = tk.Tk()
        main_root.title("Employee Main Page")
        main_root.geometry("500x400")

        cursor = self.connection.cursor()
        employee_name_query = "SELECT first_name, last_name FROM employees WHERE employee_id = %s"
        cursor.execute(employee_name_query, (employee_id_entry,))

        en_query_result = cursor.fetchone()

        if en_query_result:
            first_name, last_name = en_query_result
            employee_name_label = tk.Label(main_root, text=f"Welcome {first_name} {last_name}!")
            employee_name_label.pack()

        else: # for instances where there is an employee id and password in the database but the name isn't added
            employee_name_label = tk.Label(main_root, text="Employee Name not found")
            employee_name_label.pack()

        main_root.mainloop()
        

employee = Employee()
employee.show_connection_status()