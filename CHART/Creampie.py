import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector

def connect_database():
    try:
        host = "192.168.1.19"
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

connection = connect_database()
cursor = connection.cursor()

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

count_withdraw = fetch_count(connection, "Withdraw")
count_deposit = fetch_count(connection, "Deposit")
count_transfer = fetch_count(connection, "Transfer")
print(count_withdraw)

# Tkinter window
root = tk.Tk()
root.title("Pie Chart")

# Create a Figure and a set of subplots
fig, ax = plt.subplots()

# Data for the pie chart
s = [count_withdraw, count_deposit, count_transfer]
l = ["Withdraw", "Deposit", "Transfer"]

# Create the pie chart
ax.pie(s, labels=l, autopct='%1.1f%%', startangle=90)

# Embed the pie chart in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a toolbar (optional)
toolbar = ttk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
toolbar_button = ttk.Button(toolbar, text="Quit", command=root.destroy)
toolbar_button.pack(side=tk.RIGHT)

# Run the Tkinter event loop
root.mainloop()
