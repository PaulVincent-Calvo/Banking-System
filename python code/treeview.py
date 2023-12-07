import os
import random
from re import X
import string
import mysql.connector
from tkinter import BOTTOM, RIGHT, Y, Frame, Scrollbar, ttk
import tkinter as tk


def connect_to_database():
    connection = None
    try:
        # NOTE: all users who will access the database must be connected to the same network
        host = "192.168.1.19"  # Set to this according to your internet's ipv4 address (to check the ip address, go to the terminal and type: ipconfig)
        username = " user_treasury_citadel"
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

        

def transactions():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = f"SELECT transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount FROM transactions"

    window = tk.Tk()
    window.geometry('400x800')
    window.title("Ulol Nielle")
    
    #Adding Styles
    style = ttk.Style()
    
    #themes
    style.theme_use("clam")
    
    
    style.configure("Treeview",
                    background = "transparent",
                    foreground = "black", #text color
                    rowheight = 20,
                    fieldbackground = "white",
                    font = ("Arial", 8))
    
    style.configure("Treeview.Heading", 
                    font=("Helvetica Bold*2", 11),
                    background = "#blue,")
    
    #when a row is clicked
    style.map("Treeview", 
              background = [('selected', '#4a60db')])
    
    

    trv = ttk.Treeview(window, selectmode='browse')
    trv.grid(row=1, column=1, padx=20, pady=20)
    
    
    trv["columns"] = ("1", "2", "3", "4", "5", "6")
    trv["show"] = "headings"

    trv.column("1", width=100, anchor="c")
    trv.column("2", width=100, anchor="c")
    trv.column("3", width=140, anchor="c")
    trv.column("4", width=140, anchor="c")
    trv.column("5", width=130, anchor="c")
    trv.column("6", width=130, anchor="c")

    trv.heading("1", text="Transactions ID")
    trv.heading("2", text="Checkings ID")
    trv.heading("3", text="Transaction Type")
    trv.heading("4", text="Receiving Account")
    trv.heading("5", text="Transaction Date")
    trv.heading("6", text="Amount")
    
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        # Inserting values to the Treeview
        trv.insert("", 'end', iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))
        
        
        
    

    window.mainloop()



def customer_account_records():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = '''
    SELECT
        c.customer_id AS CustomerID,
        CONCAT(c.first_name, ' ', c.last_name) AS CustomerName,
        c.email AS Email,
        c.address AS Address,
        c.id_type AS IDType,
        c.occupation AS Occupation,
        c.annual_gross_income AS AnnualGrossIncome,
        ca.checkings_id AS CheckingsID,
        ca.account_password AS AccountPassword,
        ca.balance AS Balance,
        ca.account_status AS AccountStatus
    FROM
        customer_information c
    JOIN
        checkings_account ca ON c.customer_id = ca.customer_id'''

    window = tk.Tk()
    window.geometry('1535x810')
    window.title("Customer Records")

    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("Treeview",
                    background = "transparent",
                    foreground = "black", #text color
                    rowheight = 50,
                    fieldbackground = "white",
                    font = ("Arial", 9))
    
    style.configure("Treeview.Heading", 
                    font=("Helvetica Bold*2", 9),
                    background = "#blue,")
    
    #when a row is clicked
    style.map("Treeview", 
              background = [('selected', '#4a60db')])
    

    table_frame = Frame(window)
    table_frame.pack(side='bottom', pady=20) 
    
    table_scrollbar = Scrollbar(table_frame)
    table_scrollbar.pack(side=RIGHT, fill=Y)

    table = ttk.Treeview(table_frame, height=7, selectmode='browse', yscrollcommand=table_scrollbar.set)
    table.pack(expand=True, fill='both')  
    
    table_scrollbar.configure(command=table.yview)

    table["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11")
    table["show"] = "headings"
    
    table.column("1", width=100, anchor="c")
    table.column("2", width=100, anchor="c")
    table.column("3", width=170, anchor="c")
    table.column("4", width=140, anchor="c")
    table.column("5", width=130, anchor="c")
    table.column("6", width=130, anchor="c")
    table.column("7", width=100, anchor="c")
    table.column("8", width=90, anchor="c")
    table.column("9", width=100, anchor="c")
    table.column("10", width=100, anchor="c")
    table.column("11", width=80, anchor="c")

    table.heading("1", text = "CustomerID")
    table.heading("2", text = "CustomerName")
    table.heading("3", text = "Email")
    table.heading("4", text = "Address")
    table.heading("5", text = "IDType")
    table.heading("6", text = "Occupation")
    table.heading("7", text = "AnnualGrossIncome")
    table.heading("8", text = "CheckingsID")
    table.heading("9", text = "AccountPassword")
    table.heading("10",text = "Balance")
    table.heading("11",text = "AccountStatus")
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    

    for row in rows:
        table.insert("", 'end', iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))

    
    window.mainloop()




transactions()
