import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector

def connect_database():
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

def fetch_active(connection, account_status):
    cursor = connection.cursor()
    query = '''
    SELECT COUNT(account_status) AS occurrence_count
    FROM checkings_account
    WHERE account_status = %s 
    '''

    cursor.execute(query, (account_status,))
    result = cursor.fetchone()

    # If there are no results, set default values
    if result:
        count_active = result[0]
    else:
        count_active = 0

    return count_active

def fetch_count(connection, transac_type):
    cursor = connection.cursor()
    query = '''
    SELECT COUNT(transaction_type) AS occurrence_count
    FROM transactions
    WHERE transaction_type = %s
    '''

    cursor.execute(query, (transac_type,))
    result = cursor.fetchone()

    # If there are no results, set default values
    if result:
        count_transac = result[0]
    else:
        count_transac = 0

    return count_transac

def display_pie_chart(title, labels, sizes):
    root = tk.Tk()
    root.title(title)

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = ttk.Frame(root)
    toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar_button = ttk.Button(toolbar, text="Quit", command=root.destroy)
    toolbar_button.pack(side=tk.RIGHT)

    root.mainloop()

# Connect to the database
connection = connect_database()

# Fetch data
count_activeness = fetch_active(connection, "Active")
count_inactive = fetch_active(connection, "Inactive")

count_withdraw = fetch_count(connection, "Withdraw")
count_deposit = fetch_count(connection, "Deposit")
count_transfer = fetch_count(connection, "Transfer")

# Let the user choose which pie chart to display
choice = input("Enter 'A' for Active/Inactive or 'T' for Transaction types: ").upper()

if choice == 'A':
    display_pie_chart("Active/Inactive Pie Chart", ["Active", "Inactive"], [count_activeness, count_inactive])
elif choice == 'T':
    display_pie_chart("Transaction Types Pie Chart", ["Withdraw", "Deposit", "Transfer"], [count_withdraw, count_deposit, count_transfer])
else:
    print("Invalid choice.")
