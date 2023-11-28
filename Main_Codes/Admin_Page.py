from pathlib import Path
import subprocess
from tkinter import RIGHT, Y, Frame, Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, ttk
from Main_Ver2 import Employee, Customer, User
from Login_Page import Login_Page
from tkinter import Toplevel
from Search_Account_Page import Search_Account_Page
import mysql.connector 
from pichart import Pie_Chart


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\admin_landing_page\build\assets\frame0")

# NOTE: To Finish: buttons

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Admin_Page:
    
    def __init__(self):
        self.employee = Employee()
        self.customer = Customer()
        self.login_frame = Login_Page()
        self.search_frame = Search_Account_Page()
        self.pie_chart = Pie_Chart()
        self.admin_main_window = None
        self.connection = None
    
    def admin_mainframe(self, employee_id):
        self.connection = self.employee.adminMain()
        self.admin_main_window = Tk()
        self.admin_main_window.geometry("1535x780")
        self.admin_main_window.configure(bg="#FAFBFD")

        canvas = Canvas(self.admin_main_window, bg = "#FAFBFD", height = 765, width = 1540, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        all_records_frame = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(765.0, 600.0,image=all_records_frame)

        session_log_frame = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(1060.0, 183.0, image=session_log_frame)

        authority_frame = PhotoImage(file=relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(303.0,154.0, image=authority_frame)

        img_logout_button = PhotoImage(file=relative_to_assets("button_1.png"))
        logout_button = Button(
            image=img_logout_button,
            borderwidth=0,
            highlightthickness=0,
            command=self.logout,
            relief="flat"
        )
        logout_button.place(x=1392.0,y=13.0,width=109.0, height=37.0)

        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            374.0,
            133.0, image=entry_image_1 
        )
        search_entry = Entry(
            bd=0, bg="#FFFFFF",
            fg="#000716", highlightthickness=0,
        )
        search_entry.place(
            x=207.0,
            y=115.0,
            width=334.0,
            height=28.0
        )
        
        search_account_query = self.employee.search_credentials(self.connection, search_entry.get())
        
        img_search_button = PhotoImage(file=relative_to_assets("button_2.png"))
        search_button = Button(
            image=img_search_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.call_search_account_Page(search_entry.get()),
            relief="flat"
        )
        search_button.place(x=46.0, y=193.0, width=71.561279296875, height=72.6612548828125)


        
        img_add_button = PhotoImage(file=relative_to_assets("button_3.png"))
        add_button = Button(
            image=img_add_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.pie_chart.main(),
            relief="flat"
        )
        add_button.place(
            x=197.561279296875,
            y=193.0,
            width=71.561279296875,
            height=72.6612548828125
        )


        img_edit_button = PhotoImage(file=relative_to_assets("button_4.png"))
        edit_button = Button(
            image=img_edit_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        edit_button.place(
            x=349.12255859375,
            y=193.0,
            width=71.561279296875,
            height=72.6612548828125
        )


        img_delete_button = PhotoImage(file=relative_to_assets("button_5.png"))
        delete_button = Button(
            image=img_delete_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        delete_button.place(
            x=500.68359375,
            y=193.0,
            width=71.561279296875,
            height=72.6612548828125
        )

        self.view_customer_account_records(self.connection, self.admin_main_window, employee_id)
        self.admin_main_window.resizable(False, False)
        self.admin_main_window.mainloop()
        
    
    def call_search_account_Page(self, account_id):
        top_level_window = Toplevel()
        self.search_frame.search_account(account_id, top_level_window)
        
    
    def view_customer_account_records(self, connection, admin_window, employee_id):
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

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview",
                background="4f72ff",
                foreground="white",  # text color
                rowheight=50,
                fieldbackground="#4f72ff",
                font=("Arial*2", 9))

        # style for Treeview headings
        style.configure("Treeview.Heading",
                        font=("Helvetica Bold*2", 9),
                        background="white")
        
        #when a row is clicked
        style.map("Treeview", 
                background = [('selected', '#4a60db')])

        table_frame = Frame(admin_window)
        table_frame.pack(side='bottom', pady=22) 
        
        table_scrollbar = Scrollbar(table_frame)
        table_scrollbar.pack(side=RIGHT, fill=Y)

        table = ttk.Treeview(table_frame, height=6, selectmode='browse', yscrollcommand=table_scrollbar.set)
        table.pack(expand=True, fill='both')  

        table_scrollbar.configure(command=table.yview)

        table["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11")
        table["show"] = "headings"
        
        table.column("1", width=100, anchor="c")
        table.column("2", width=140, anchor="c")
        table.column("3", width=170, anchor="c")
        table.column("4", width=200, anchor="c")
        table.column("5", width=130, anchor="c")
        table.column("6", width=150, anchor="c")
        table.column("7", width=140, anchor="c")
        table.column("8", width=90, anchor="c")
        table.column("9", width=120, anchor="c")
        table.column("10", width=100, anchor="c")
        table.column("11", width=100, anchor="c")

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

        self.employee.add_transaction_log(self.connection, employee_id, "View User", "customer_information",None, None, None)
    

    # NOTE: to finish, not priority
    def logout(self):
        if self.admin_main_window:
            self.admin_main_window.withdraw()
            self.login_frame.login_page()

   