from BankingMethods import BankingMethods
from tkinter import messagebox
from tabulate import tabulate
import tkinter as tk


class Test(BankingMethods):
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
    
    def get_customer_info(self):
        cursor = self.connection.cursor()
        get_info_query = f"SELECT * FROM customer_information JOIN checkings_account ON customer_information.customer_id = checkings_account.customer_id;"
        cursor.execute(get_info_query)

        account_info_rows = cursor.fetchall()

        column_names = ["Customer ID", "Password", "First Name", "Last Name", 
                        "Email", "Address", "ID Type", "Occupation", 
                        "Annual Gross Income", "Checkings ID", "Balance"]
        
        accoount_info = tabulate(account_info_rows, headers=column_names,tablefmt="grid")
        
        return accoount_info
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

        login_frame = tk.Frame(login_root, width = 300, height = 200)
        login_frame.pack(expand=True)

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

    def main_page(self, id_entry):
        main_root = tk.Tk()
        main_root.geometry("1400x500")

        # frames
        side_frame = tk.Frame(main_root, width = 300, height = 500)
        main_frame = tk.Frame(main_root, width = 700, height = 500)

        # content on side frame (Employee Name and Buttons)
        first_name, last_name = self.get_name(id_entry, 1)
        employee_name_label = tk.Label(side_frame, text=f"Welcome {first_name} {last_name}!")
        employee_name_label.pack(side="top", pady=10)

        side_frame.pack(side="left", fill="y")

        # content on main frame (Transaction Tables)
        transactions = self.get_customer_info()
        transactions_text = tk.Text(main_frame, height=10, width=50)
        transactions_text.insert(tk.END, transactions)
        transactions_text.config(state="disabled")
        transactions_text.pack(side="left", fill="both", padx=40, expand=True)

        # scrollbar for the table if it has many content
        scrollbar = tk.Scrollbar(main_frame, command=transactions_text.yview)
        scrollbar.pack(side="right", fill="y")
        transactions_text.config(yscrollcommand=scrollbar.set)

        main_frame.pack(side="left", fill="both", expand=True)

        #---------------------------
        main_root.mainloop()

test_instance = Test()
test_instance.test()
# print(test_instance.get_transactions())
test_instance.login_page()
