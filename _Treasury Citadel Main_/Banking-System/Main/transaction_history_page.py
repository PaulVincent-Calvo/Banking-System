import tkinter as tk
from tkinter import Frame, Toplevel, ttk
from tkinter import messagebox
from turtle import width
import mysql.connector
from raw_main import Employee


class Session_Transaction_Histories:
    def __init__(self):
         self.employee = Employee()

    def connect_to_database(self):
        connection = None
        try:
            host = "localhost"
            username = "root"
            password = ""
            database = "treasury_citadel_database"

            connection = mysql.connector.connect(
                host=host,
                user=username,
                password=password,
                database=database
            )

            print("Database Initialization Successful...")

        except mysql.connector.Error as error:
            print(error)

        return connection

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=34,
                        fieldbackground="white",
                        font=("Arial", 10))

        style.configure("Treeview.Heading",
                        font=("Helvetica Bold", 11),
                        background="#3498db",
                        foreground="white")

        style.map("Treeview",
                    background=[('selected', '#3498db')])

    def create_treeview_with_scrollbar(self, window, columns, headings, access_as):
        table_frame = Frame(window)
        
        if access_as == "Session Log":
            table_frame.grid(row=1, column=0, padx=0, pady=0)
            
        elif access_as == "Customer Transactions":
            table_frame.grid(row=1, column=0, padx=580, pady=355)
            
        elif access_as == "Users Transaction":
            table_frame.grid(row=1, column=0, padx=80, pady=20)

        elif access_as == "Customer All Records":
            table_frame.grid(row=1, column=0, padx=20, pady=416)
            
        if access_as == "Search User":
            table_frame.grid(row=1, column=0, pady=40)

        elif access_as == "Edit User" or access_as == "Add User":
            table_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nw')


        treeview = ttk.Treeview(table_frame, height=9, columns=columns, show="headings")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)

        for col, head in zip(columns, headings):
            # width = 180 if access_as == "Customer Transactions" elif (116 if access_as == "Session Log" else None) else (100 if access_as == "Customer All Records" else None)
            width = (
                180 if access_as == "Customer Transactions" or access_as == "Search User" or access_as == "Edit User" or access_as == "Add User"
                else (130 if access_as == "Session Log" or access_as == "Users Transaction" else None)
                if access_as == "Session Log" or access_as == "Users Transaction"
                else (133 if access_as == "Customer All Records" else None))

            treeview.column(col, width=width, anchor="center")
            treeview.heading(col, text=head)

        treeview.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")

        return treeview

    def populate_treeview(self, treeview, query, account_id, column_count):
        
        connection = self.connect_to_database()
        cursor = connection.cursor()
        if account_id == None:
            cursor.execute(query)

        elif account_id != None:
            cursor.execute(query, (account_id, ))
            
        rows = cursor.fetchall()
        for row in rows:
            treeview.insert("", 'end', values=row[:column_count])



    def transactions_admin(self):
        window = Toplevel()

        window.title("Transaction Records")
        access_as = "Users Transaction"
        self.configure_style()

        columns = ("transactions_id", "checkings_id", "transaction_type", "receiving_account", "transaction_date", "amount")
        headings = ("Transaction ID", "Checkings ID", "Transaction Type", "Receiving Account", "Transaction Date", "Amount")

        trv = self.create_treeview_with_scrollbar(window, columns, headings, access_as)
        query = "SELECT transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount FROM transactions"
        self.populate_treeview(trv, query, None, len(columns))

    def transactions_customer(self, parent_window, account_id):
        access_as = "Customer Transactions"
        self.configure_style()
        columns = ("transactions_id", "transaction_type", "receiving_account", "transaction_date", "amount")
        headings = ("Transaction ID", "Transaction Type", "Receiving Account", "Transaction Date", "Amount")

        trv = self.create_treeview_with_scrollbar(parent_window, columns, headings, access_as)
        query = "SELECT transactions_id, transaction_type, receiving_account, transaction_date, amount FROM transactions WHERE checkings_id = %s ORDER BY transaction_date DESC"
        self.populate_treeview(trv, query, account_id, len(columns))

    def session_log(self, account_id):
        access_as = "Session Log"
        window = Toplevel()
        window.geometry('1300x350')
        window.title("Session Logs")
        self.configure_style()
        
        columns = ("session_log_id", "employee_id", "session_date", "session_type", "table_involved", "column_involved", "modified_value", "stored_value", "status", "last_modified", "version")
        headings = ("Session ID", "Employee ID", "Session Date", "Session Type", "Table Involved", "Column Involved", "Modified Value", "Stored Value", "Status", "Last Modified", "Version")

        trv = self.create_treeview_with_scrollbar(window, columns, headings, access_as)
        query = "SELECT session_log_id, employee_id, session_date, session_type, table_involved, column_involved, modified_value, stored_value, status, last_modified, version FROM session_log WHERE employee_id = %s"
        self.populate_treeview(trv, query, account_id, len(columns))
       

    def customer_checkings_view(self, connection, parent_window, employee_id):
        access_as = "Customer All Records"
        self.configure_style()
        columns = ("customer_id", "customer_name", "email", "address", "id_type", "occupation", "annual_gross_income", "checkings_id", "account_password", "balance", "account_status")
        headings = ("CustomerID", "CustomerName", "Email", "Address", "IDType", "Occupation", "AnnualGrossIncome", "CheckingsID", "AccountPassword", "Balance", "AccountStatus")
        trv = self.create_treeview_with_scrollbar(parent_window, columns, headings, access_as)
        query = "SELECT * FROM customer_checkings_view"
        self.populate_treeview(trv, query, None, len(columns))
        self.employee.add_transaction_log(connection, employee_id, "View User", "customer_information", None, None, None)
    
