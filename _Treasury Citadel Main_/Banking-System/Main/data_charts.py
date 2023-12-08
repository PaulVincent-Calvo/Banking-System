import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector
from raw_main import Employee


class Data_Charts:

    def __init__(self):
        self.employee = Employee()

    def transac_type_values(self, connection, transac_type, access_as, account_id):
        cursor = connection.cursor()
        result = None
        
        if access_as == "Employee" and account_id == None:
            query = '''
            SELECT COUNT(transaction_type) AS occurrence_count
            FROM transactions WHERE transaction_type = %s'''
            cursor.execute(query, (transac_type,))
            result = cursor.fetchone()
            
        elif access_as == "Customer" and account_id != None:
            query = '''
            SELECT COUNT(transaction_type) AS occurrence_count
            FROM transactions WHERE transaction_type = %s and checkings_id = %s'''
            cursor.execute(query, (transac_type, account_id,))
            result = cursor.fetchone()

        if result is not None:
            count_transac = result[0]
        else:
            count_transac = 0

        return count_transac
    

    def account_status_values(self, connection, account_status):
        cursor = connection.cursor()
        result = None
        try:
            query = '''
            SELECT COUNT(account_status) AS occurrence_count
            FROM checkings_account WHERE account_status = %s'''
            cursor.execute(query, (account_status,))
            result = cursor.fetchone()
            count_transac = result[0] if result is not None else 0
            
        except mysql.connector.Error as error:
            messagebox.showerror("MySQL", error)

        return count_transac

    def display_charts(self, chart_title, labels, size_per_label):
        root = tk.Tk()
        root.title(chart_title)

        fig, ax = plt.subplots()
        ax.pie(size_per_label, labels=labels, autopct='%1.1f%%', startangle=90)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = ttk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar_button = ttk.Button(toolbar, text="Quit", command=root.destroy)
        toolbar_button.pack(side=tk.RIGHT)

        root.mainloop()
        
    def run_transaction_chart(self, access_as, account_id):
        connection = self.employee.connect_database()
        count_withdraw = self.transac_type_values(connection, "Withdraw", access_as, account_id)
        count_deposit = self.transac_type_values(connection, "Deposit", access_as, account_id)
        count_transfer = self.transac_type_values(connection, "Transfer", access_as, account_id)
        self. display_charts("Transaction Charts", ["Withdraw", "Deposit", "Transfer"], [count_withdraw, count_deposit, count_transfer])

    def run_account_status_chart(self):
        connection = self.employee.connect_database()
        count_active = self.account_status_values(connection, "Active")
        count_inactive = self.account_status_values(connection, "Inactive")
        self.display_charts("Account Status Charts", ["Active", "Inactive"], [count_active, count_inactive])

