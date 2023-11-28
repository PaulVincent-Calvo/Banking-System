import time
import matplotlib
matplotlib.use('TkAgg')
from pathlib import Path
from tkinter import Toplevel
from tkinter import RIGHT, Y, Frame, Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, ttk
from Main_Ver2 import Employee, Customer, User
from Login_Page import Login_Page
from Search_Account_Page import Search_Account_Page
from pichart import Pie_Chart
from Admin_Edit_Add_Page import Admin_Edit_Add_Page


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\final_admin_Landing_page\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Admin_Page:
    
    def __init__(self):
        self.employee = Employee()
        self.customer = Customer()
        self.login_frame = Login_Page()
        self.search_frame = Search_Account_Page()
        self.admin_edit_add_page = Admin_Edit_Add_Page()
        self.pie_chart = Pie_Chart()
        self.admin_main_window = None
        self.connection = None

    def admin_mainframe(self, employee_id):
        self.connection = self.employee.adminMain()
        self.admin_main_window = Tk()
        self.admin_main_window.geometry("1540x765")
        self.admin_main_window.configure(bg = "#FAFBFD")


        canvas = Canvas(
            self.admin_main_window,
            bg = "#FAFBFD",
            height = 765,
            width = 1540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)

        main_bg = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            753.0,
            375.0,
            image=main_bg
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            371.0,
            128.0,
            image=entry_image_1
        )
        search_entry = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        search_entry.place(
            x=206.0,
            y=108.0,
            width=330.0,
            height=32.0
        )

        img_search_but = PhotoImage(
            file=relative_to_assets("button_9.png"))
        search_button = Button(
            image=img_search_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.call_search_account_page(search_entry.get()),
            relief="flat"
        )
        search_button.place(
            x=56.0,
            y=181.0,
            width=73.0,
            height=71.0
        )

        img_logout_but = PhotoImage(
            file=relative_to_assets("button_1.png"))
        logout_button = Button(
            image=img_logout_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("log_out button clicke"),
            relief="flat"
        )
        logout_button.place(
            x=1390.0,
            y=0.0,
            width=109.0,
            height=37.0
        )

        img_transacHist_but = PhotoImage(
            file=relative_to_assets("button_2.png"))
        transaction_history_button = Button(
            image=img_transacHist_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        transaction_history_button.place(
            x=630.0,
            y=149.0,
            width=177.0,
            height=72.0
        )

        img_sesLog_but = PhotoImage(
            file=relative_to_assets("button_3.png"))
        session_log_button = Button(
            image=img_sesLog_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        session_log_button.place(
            x=853.0,
            y=149.0,
            width=177.0,
            height=61.0
        )

        img_transacChart_but = PhotoImage(
            file=relative_to_assets("button_4.png"))
        transac_chart_button = Button(
            image=img_transacChart_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.pie_chart.main(),
            relief="flat"
        )
        transac_chart_button.place(
            x=1078.0,
            y=149.0,
            width=176.0,
            height=72.0
        )

        img_accChart = PhotoImage(
            file=relative_to_assets("button_5.png"))
        account_chart_button = Button(
            image=img_accChart,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        account_chart_button.place(
            x=1302.0,
            y=149.0,
            width=176.0,
            height=61.0
        )

        img_delete_but = PhotoImage(
            file=relative_to_assets("button_6.png"))
        delete_button = Button(
            image=img_delete_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        delete_button.place(
            x=455.0,
            y=179.0,
            width=73.0,
            height=71.0
        )

        img_edit_but = PhotoImage(
            file=relative_to_assets("button_7.png"))
        edit_button = Button(
            image=img_edit_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.call_add_or_edit_page(search_entry.get(), "Edit User"),
            relief="flat"
        )
        edit_button.place(
            x=324.0,
            y=179.0,
            width=73.0,
            height=71.0
        )

        img_add_but = PhotoImage(
            file=relative_to_assets("button_8.png"))
        add_button = Button(
            image=img_add_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.call_add_or_edit_page(search_entry.get(), "Add User"),
            relief="flat"
        )
        add_button.place(
            x=193.0,
            y=179.0,
            width=73.0,
            height=71.0
        )

        self.view_customer_account_records(self.connection, self.admin_main_window, employee_id)
        self.admin_main_window.resizable(True, True)
        self.admin_main_window.mainloop()

    def call_search_account_page(self, account_id):
        top_level_window = Toplevel()
        self.search_frame.search_account(account_id, top_level_window)
    
    def call_add_or_edit_page(self, account_id, session_indicator):  # session_indicator(either Add or Edit)
        top_level_window = Toplevel(self.admin_main_window)
        self.admin_edit_add_page.edit_add_page(account_id, top_level_window, session_indicator)

        # self.admin_main_window.deiconify()
    
    def view_customer_account_records(self, connection, admin_window, employee_id):
        table_frame = Frame(admin_window)
        table_frame.pack(side='bottom', pady=22)

        table_scrollbar = Scrollbar(table_frame)
        table_scrollbar.pack(side=RIGHT, fill=Y)

        table = ttk.Treeview(table_frame, height=6, selectmode='browse', yscrollcommand=table_scrollbar.set)
        table.pack(expand=True, fill='both')

        table_scrollbar.configure(command=table.yview)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="4f72ff",
                        foreground="black",
                        rowheight=50,
                        fieldbackground="#ffffff",
                        font=("Arial*2", 9))

        style.configure("Treeview.Heading",
                        font=("Helvetica Bold*2", 9),
                        background="white")

        style.map("Treeview",
                background=[('selected', '#4a60db')])

        table.configure(style="Treeview")

        cursor = connection.cursor()
        query = "SELECT * FROM customer_checkings_view"

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

        table.heading("1", text="CustomerID")
        table.heading("2", text="CustomerName")
        table.heading("3", text="Email")
        table.heading("4", text="Address")
        table.heading("5", text="IDType")
        table.heading("6", text="Occupation")
        table.heading("7", text="AnnualGrossIncome")
        table.heading("8", text="CheckingsID")
        table.heading("9", text="AccountPassword")
        table.heading("10", text="Balance")
        table.heading("11", text="AccountStatus")

        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            table.insert("", 'end', iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))

        self.employee.add_transaction_log(self.connection, employee_id, "View User", "customer_information", None, None, None)

    # def apply_final_style(self, widget):
    #     style = ttk.Style()
    #     style.theme_use("clam")

    #     style.configure("Treeview",
    #                     background="4f72ff",
    #                     foreground="black",
    #                     rowheight=50,
    #                     fieldbackground="#ffffff",
    #                     font=("Arial*2", 9))

    #     style.configure("Treeview.Heading",
    #                     font=("Helvetica Bold*2", 9),
    #                     background="white")

    #     style.map("Treeview",
    #                 background=[('selected', '#4a60db')])

    #     widget.configure(style="Treeview")
        
    # NOTE: to finish, not priority
    def logout(self):
        if self.admin_main_window:
            self.admin_main_window.withdraw()
            self.login_frame.login_page()
