
import time
import matplotlib
matplotlib.use('TkAgg')

from pathlib import Path

import mysql.connector
from raw_main import Employee
from tkinter import RIGHT, Y, Frame, Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, ttk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\GUI Assets\search_page_assets\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Search_Account_Page:
    
    def __init__(self):
        self.employee = Employee()
        self.connection = None
    
    def search_account(self, account_id, toplevel):
        window = toplevel
        print(str(account_id))
        self.connection = self.employee.adminMain()
        search_account_query = self.employee.search_credentials(self.connection, account_id)
        window.geometry("1486x417")
        window.configure(bg = "#FFFFFF")

        canvas = Canvas(
            window,
            bg = "#FFFFFF",
            height = 417,
            width = 1486,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_text(
            350,
            20.0,
            anchor="nw",
            text=account_id,
            fill="#000000",
            font=("Arial Black", 60 * -1)
        )

        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            742.0,
            264.0,
            image=image_image_1
        )

        image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(
            159.0,
            64.0,
            image=image_image_2
        )
        
        self.display_searched_account(window, self.connection, search_account_query, account_id, "Search User")
        window.resizable(False, False)
        window.mainloop()
        

    def display_searched_account(self, window, connection, search_acc_query, account_id, session_type):
        print("display_searched_account ACCESSED")
        cursor = connection.cursor()
       
        style2 = ttk.Style()
        style2.theme_use("clam")
        
        style2.configure("Treeview",
        background="4f72ff",
        foreground="black",  # text color
        rowheight=50,
        fieldbackground="#ffffff",
        font=("Arial*2", 9))
        

        
        style2.configure("Treeview.Heading",
                        font=("Helvetica Bold*2", 9),
                        background="#3498db",
                        foreground="white")
        
    
        style2.map("Treeview", 
                background = [('selected', '#4a60db')])

        table_frame2 = Frame(window)
        if session_type == "Search User":
            table_frame2.pack(side='bottom', pady=40) 
            
        elif session_type == "Edit User" or session_type == "Add User":
            table_frame2.place(relx=0.08, rely=0.10, anchor='nw')
        
        table_scrollbar2 = Scrollbar(table_frame2)
        table_scrollbar2.pack(side=RIGHT, fill=Y)

        table4 = ttk.Treeview(table_frame2, height=3, selectmode='browse', yscrollcommand=table_scrollbar2.set)
        table4.pack(expand=True, fill='both')  
        
        table_scrollbar2.configure(command=table4.yview)
        
        
        try:
            if search_acc_query =="SELECT * FROM customer_information WHERE customer_id = %s":
                new_query = "SELECT * FROM customer_information_view WHERE customer_id = %s"
                table4["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
                table4["show"] = "headings"
                
                table4.column("1", width=100, anchor="c")
                table4.column("2", width=100, anchor="c")
                table4.column("3", width=170, anchor="c")
                table4.column("4", width=200, anchor="c")
                table4.column("5", width=130, anchor="c")
                table4.column("6", width=130, anchor="c")
                table4.column("7", width=100, anchor="c")
                table4.column("8", width=150, anchor="c")
                
                table4.heading("1", text = "CustomerID")
                table4.heading("2", text = "FirstName")
                table4.heading("3", text = "LastName")
                table4.heading("4", text = "Email")
                table4.heading("5", text = "Address")
                table4.heading("6", text = "IDType")
                table4.heading("7", text = "Occupation")
                table4.heading("8", text = "AnnualGrossIncome")
                            
                cursor.execute(new_query, (account_id,))

                rows = cursor.fetchall()
                for row in rows:
                    table4.insert("", 'end', iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
               

            elif search_acc_query =="SELECT * FROM checkings_account WHERE checkings_id = %s":
                new_query = "SELECT * FROM checkings_account_view WHERE checkings_id = %s"
                table4["columns"] = ("1", "2", "3", "4", "5")
                table4["show"] = "headings"
                
                table4.column("1", width=100, anchor="c")
                table4.column("2", width=100, anchor="c")
                table4.column("3", width=170, anchor="c")
                table4.column("4", width=200, anchor="c")
                table4.column("5", width=130, anchor="c")
                
                table4.heading("1", text = "CheckingsID")
                table4.heading("2", text = "Password")
                table4.heading("3", text = "Balance")
                table4.heading("4", text = "Status")
                table4.heading("5", text = "CustomerID")
                            
                cursor.execute(new_query, (account_id,))

                rows = cursor.fetchall()
                for row in rows:
                    table4.insert("", 'end', iid=row[0], values=(row[0], row[1], row[2], row[3], row[4]))
               
            
            elif search_acc_query =="SELECT * FROM transactions WHERE transactions_id = %s":
                new_query = "SELECT * FROM transactions_view WHERE transactions_id = %s"
                table4["columns"] = ("1", "2", "3", "4", "5", "6")
                table4["show"] = "headings"
                
                table4.column("1", width=100, anchor="c")
                table4.column("2", width=100, anchor="c")
                table4.column("3", width=170, anchor="c")
                table4.column("4", width=200, anchor="c")
                table4.column("5", width=130, anchor="c")
                table4.column("6", width=130, anchor="c")
                
                table4.heading("1", text = "Transactions ID")
                table4.heading("2", text = "Checkings ID")
                table4.heading("3", text = "Transaction Type")
                table4.heading("4", text = "Receiving Account")
                table4.heading("5", text = "Transaction Date")
                table4.heading("6", text = "Amount")
                
                cursor.execute(new_query, (account_id,))

                rows = cursor.fetchall()
                for row in rows:
                    table4.insert("", 'end', iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))

            
        except mysql.connector.Error as error:
            print(error)
            
            