
import matplotlib
matplotlib.use('TkAgg')
import mysql.connector
from pathlib import Path
from tkinter import Toplevel, messagebox
from tkinter import RIGHT, Y, Frame, Scrollbar, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, ttk
from raw_main import Employee, Customer, User
from login_page import Login_Page
from search_account_page import Search_Account_Page
from data_charts import Data_Charts
from admin_edit_add_page import Edit_Add_Page
from transaction_history_page import Session_Transaction_Histories


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\GUI Assets\_admin_page_assets\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Admin_Page:
    
    def __init__(self):
        self.employee = Employee()
        self.customer = Customer()
        self.login_frame = Login_Page()
        self.search_frame = Search_Account_Page()
        self.admin_edit_add_page = Edit_Add_Page()
        self.charts = Data_Charts()
        self.session = Session_Transaction_Histories()
        self.admin_main_window = None
        # self.connection = None

    def admin_mainframe(self, employee_id, connection, cursor):
        # self.connection = self.employee.connect_database()
        # cursor = self.connection.cursor()
        self.admin_main_window = Tk()
        self.admin_main_window.geometry("1540x765")
        self.admin_main_window.configure(bg = "#FAFBFD")
        self.admin_main_window.title("Admin Landing Page")
        
        
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
            command=lambda: self.call_search_account_page(connection, self.admin_main_window, search_entry.get()),
            relief="flat"
        )
        search_button.place(
            x=66.0,
            y=190.0,
            width=67.0,
            height=65.0
        )
        
        img_logout_but = PhotoImage(
            file=relative_to_assets("button_1.png"))
        logout_button = Button(
            image=img_logout_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: log_out_session(),
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
            command=lambda: self.session.transactions_admin(),
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
            command=lambda: self.session.session_log(employee_id),
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
            command=lambda:self.charts.run_transaction_chart("Employee", None),
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
            command=lambda: self.charts.run_account_status_chart(),
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
            command=lambda: self.call_deletion_page(employee_id, connection, cursor, self.admin_main_window, search_entry.get()),
            relief="flat"
        )
        delete_button.place(
            x=458.0,
            y=190.0,
            width=67.0,
            height=65.0
        )

        img_edit_but = PhotoImage(
            file=relative_to_assets("button_7.png"))
        edit_button = Button(
            image=img_edit_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.call_add_or_edit_page(connection, cursor, self.admin_main_window, search_entry.get(), "Edit User", employee_id),
            relief="flat"
        )
        edit_button.place(
            x=329.0,
            y=190.0,
            width=67.0,
            height=65.0
        )

        img_add_but = PhotoImage(
            file=relative_to_assets("button_8.png"))
        add_button = Button(
            image=img_add_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.call_add_or_edit_page(connection, cursor, self.admin_main_window, search_entry.get(), "Add User", employee_id),
            relief="flat"
        )
        add_button.place(
            x=196.0,
            y=190.0,
            width=67.0,
            height=65.0
        )
        
        log_out_status = ""
        def log_out_session():
            log_out_status = self.employee.logout()
            if log_out_status == "Go Back to Login":
                self.admin_main_window.destroy()
        
        if log_out_status == "Go Back to Login":
            employee_id = ""
            print("Going Back to LogIn Page")
            return log_out_status
        
        self.session.customer_checkings_view(connection, self.admin_main_window, employee_id)
        self.admin_main_window.resizable(True, True)
        self.admin_main_window.mainloop()
        

    # def logout(self):
    #     close_window = messagebox.askquestion("Exit", "Confirm Logout", icon = "warning")
    #     status = "Go Back to Login" if close_window == 'yes' else ''
    #     return status
        
    
    
    def call_search_account_page(self, connection, window, account_id):
        search_account_query = self.employee.search_credentials(connection, account_id)
        if search_account_query == "Account Non-existent":
            messagebox.showerror("Search Account Status", "Account Not Found")
        
        else:
            top_level_window = Toplevel()
            self.search_frame.search_account(account_id, top_level_window)
    
    def call_add_or_edit_page(self, connection, cursor, window, account_id, session_indicator, employee_id):  # session_indicator(either Add or Edit)
        search_account_query = self.employee.search_credentials(connection, account_id)
        
        if search_account_query == "Account Non-existent":
            messagebox.showerror("Searched Account Error", "Account Non-Existent")

        else:
            if session_indicator == "Add User":
                while True:
                    if self.employee.proceed_to_session("adding information", account_id) == "Yes":
                        
                        if search_account_query == "SELECT * FROM customer_information WHERE customer_id = %s":
                            table_involved = "customer_information"
                            

                            if self.employee.check_account_existence(cursor, "checkings_account", "customer_id", account_id):
                                messagebox.showerror("Invalid Session", "Customer ID already exists in Checkings Account")
                                break
                                
                            elif self.employee.check_account_existence(cursor, "customer_information", "customer_id", account_id) is None:
                                messagebox.showerror("Session Log", "Customer ID Non-Existent")
                                break
                            
                            else:
                                top_level_window = Toplevel()
                                self.admin_edit_add_page.main(connection, cursor, account_id, top_level_window, session_indicator, "checkings_account", employee_id)
                                break

                        elif search_account_query == "SELECT * FROM checkings_account WHERE checkings_id = %s":
                            top_level_window = Toplevel()
                            self.admin_edit_add_page.main(connection, cursor, account_id, top_level_window, session_indicator, "transactions", employee_id)
                            break

                        elif search_account_query == "SELECT * FROM transactions WHERE transactions_id = %s":
                            if self.employee.check_account_existence(cursor, "transactions", "transactions_id", account_id):
                                messagebox.showerror("Invalid Session", "Transactions ID already exists in Transactions")
                                break
                            
                        elif search_account_query == "New Account":
                            top_level_window = Toplevel()
                            self.admin_edit_add_page.main(connection, cursor, account_id, top_level_window, session_indicator, "New Account", employee_id)
                            break
                        
                    else: break
            
            elif session_indicator == "Edit User":
                while True:
                    if self.employee.proceed_to_session("editing information", account_id) == "Yes":
                        
                        if search_account_query == "SELECT * FROM customer_information WHERE customer_id = %s":
                            top_level_window = Toplevel()
                            self.admin_edit_add_page.main(connection, cursor, account_id, top_level_window, session_indicator, "customer_information", employee_id)
                            break

                        elif search_account_query == "SELECT * FROM checkings_account WHERE checkings_id = %s":
                            top_level_window = Toplevel()
                            self.admin_edit_add_page.main(connection, cursor, account_id, top_level_window, session_indicator, "checkings_account", employee_id)
                            break

                        elif search_account_query == "SELECT * FROM transactions WHERE transactions_id = %s":
                            top_level_window = Toplevel()
                            self.admin_edit_add_page.main(connection, cursor, account_id, top_level_window, session_indicator, "transactions", employee_id)
                            break

                    else: break

    # def proceed_to_session(self, session_type, account_id):
    #     proceed = messagebox.askquestion("Session", f"You will be {session_type} for account {account_id}.")
    #     status = "Yes" if proceed == 'yes' else "No"
    #     return status
     
    def call_deletion_page(self, employee_id, connection, cursor, window, account_id):
        search_account_query = self.employee.search_credentials(connection, account_id)
        confirm_deletion = self.employee.confirm_deletion(window, account_id)
        
        while True:
            if confirm_deletion == "Deletion Initiated":
                if search_account_query == "SELECT * FROM customer_information WHERE customer_id = %s":
                    delete_account = self.employee.delete_user_by_ID(connection, cursor, employee_id, "customer_information", "customer_id", account_id)
                
                elif search_account_query == "SELECT * FROM checkings_account WHERE checkings_id = %s":
                    delete_account = self.employee.delete_user_by_ID(connection, cursor, employee_id, "checkings_account", "checkings_id", account_id)
                    
                elif search_account_query == "SELECT * FROM transactions WHERE transactions_id = %s":
                    delete_account = self.employee.delete_user_by_ID(connection, cursor, employee_id, "transactions", "transactions_id", account_id )

                else:  messagebox.showerror("Error", "Account Non-Existent")
                
                (self.employee.deletion_status(True, account_id)) if delete_account == True else (self.employee.deletion_status(False,account_id))
                break

            else: break

    # def confirm_deletion(self, window, account_id):
    #     confirm = messagebox.askquestion("Confirm Session", f"Delete Information for Account {account_id} ?\nNote All Records will be deleted due to foreign key referencing...")
    #     status = "Deletion Initiated" if confirm == 'yes' else "Deletion Revokes"
    #     return status
        
    # def deletion_status(self, status, account_id):
    #     status_message = f"Account {account_id} deleted successfully.." if status else f"Error for the deletion of account {account_id}"
    #     messagebox.showinfo("Deletion Status", status_message) if status else messagebox.showerror("Deletion Error", status_message)
                    
          
