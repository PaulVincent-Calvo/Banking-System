import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_to_database():
    connection = None
    try:
        host = "192.168.1.134"
        username = "user_treasury_citadel"
        password = "tC23_oop_dbms_pRoj2023"
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

def configure_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white",
                    font=("Arial", 10))

    style.configure("Treeview.Heading",
                    font=("Helvetica Bold", 12),
                    background="#3498db",
                    foreground="white")

    style.map("Treeview",
              background=[('selected', '#3498db')])

def create_treeview_with_scrollbar(window, columns, headings):
    frame = ttk.Frame(window)
    frame.grid(row=1, column=0, padx=20, pady=20)

    treeview = ttk.Treeview(frame, columns=columns, show="headings")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)

    for col, head in zip(columns, headings):
        treeview.column(col, width=150, anchor="center")
        treeview.heading(col, text=head)

    treeview.pack(side="left", fill="y")
    scrollbar.pack(side="right", fill="y")

    return treeview

def populate_treeview(treeview, query, column_count):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        treeview.insert("", 'end', values=row[:column_count])

def transactions():
    window = tk.Tk()
    window.geometry('950x350')
    window.title("Transaction Records")

    configure_style()

    columns = ("transactions_id", "checkings_id", "transaction_type", "receiving_account", "transaction_date", "amount")
    headings = ("Transaction ID", "Checkings ID", "Transaction Type", "Receiving Account", "Transaction Date", "Amount")

    trv = create_treeview_with_scrollbar(window, columns, headings)
    query = "SELECT transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount FROM transactions"
    populate_treeview(trv, query, len(columns))

    window.mainloop()

def customer_account_records():
    window = tk.Tk()
    window.geometry('1200x600')
    window.title("Customer Records")

    configure_style()

    columns = ("customer_id", "customer_name", "email", "address", "id_type", "occupation",
               "annual_gross_income", "checkings_id", "account_password", "balance", "account_status")
    headings = ("Customer ID", "Customer Name", "Email", "Address", "ID Type", "Occupation",
                "Annual Gross Income", "Checkings ID", "Account Password", "Balance", "Account Status")

    trv = create_treeview_with_scrollbar(window, columns, headings)
    query = '''
        SELECT
            c.customer_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name, c.email, c.address,
            c.id_type, c.occupation, c.annual_gross_income, ca.checkings_id, ca.account_password,
            ca.balance, ca.account_status
        FROM
            customer_information c
        JOIN
            checkings_account ca ON c.customer_id = ca.customer_id
    '''
    populate_treeview(trv, query, len(columns))

    window.mainloop()


transactions()
# customer_account_records()
