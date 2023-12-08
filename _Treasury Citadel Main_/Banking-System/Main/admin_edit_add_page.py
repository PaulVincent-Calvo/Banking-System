import logging
import os
import time
import matplotlib
matplotlib.use('TkAgg')
import datetime
import tkinter
import tkinter as tk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, TkVersion, Toplevel, messagebox
from search_account_page import Search_Account_Page
from raw_main import Employee, Customer
import mysql.connector
from transaction_history_page import Session_Transaction_Histories


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\GUI Assets\edit_and_add_page_assets\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# NOTE Transaction Log: None: Search, Edit, Add, Delete
# NOTE: Add Identifier for Transaction(Like: Edit User, Add something in add or delete)


class Edit_Add_Page:
    
    def __init__(self) -> None:
        self.search_frame = Search_Account_Page()
        self.employee = Employee()
        self.customer = Customer()
        # self.connection = None
        self.window = None
    
    def validate_date_format(self, date_string):
        try:
            # Attempt to parse the date using strptime
            datetime.datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    
     
    def main(self, connection, cursor, account_id, toplevel_window, session_indicator, table_involved, employee_id):
        # self.connection = self.employee.adminMain()
        # cursor = self.connection.cursor()
        
        search_account_query = self.employee.search_credentials(connection, account_id)
        print(search_account_query)

        self.window = toplevel_window
        self.window.geometry("1271x700")
        self.window.configure(bg = "#FFFFFF")
        canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 700,
            width = 1271,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            1003.0,
            342.0,
            image=image_image_1
        )

        image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(
            436.0,
            532.0,
            image=image_image_2
        )

        img_Fname = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            323.5,
            437.5,
            image=img_Fname
        )
        firstname_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        firstname_entry.place(
            x=241.5,
            y=418.0,
            width=164.0,
            height=31.0
        )

        img_IDType = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            717.5,
            434.5,
            image=img_IDType
        )
        IDType_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        IDType_entry.place(
            x=635.5,
            y=415.0,
            width=164.0,
            height=31.0
        )

        img_Lname = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        entry_bg_3 = canvas.create_image(
            323.5,
            506.5,
            image=img_Lname
        )
        lastname_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        lastname_entry.place(
            x=241.5,
            y=487.0,
            width=164.0,
            height=31.0
        )

        img_occupation = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = canvas.create_image(
            717.5,
            506.5,
            image=img_occupation
        )
        occupation_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        occupation_entry.place(
            x=635.5,
            y=487.0,
            width=164.0,
            height=31.0
        )

        img_email = PhotoImage(
            file=relative_to_assets("entry_5.png"))
        entry_bg_5 = canvas.create_image(
            323.5,
            575.5,
            image=img_email
        )
        email_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        email_entry.place(
            x=241.5,
            y=556.0,
            width=164.0,
            height=31.0
        )

        img_address = PhotoImage(
            file=relative_to_assets("entry_6.png"))
        entry_bg_6 = canvas.create_image(
            717.5,
            575.5,
            image=img_address
        )
        address_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        address_entry.place(
            x=635.5,
            y=556.0,
            width=164.0,
            height=31.0
        )

        img_annualIncome = PhotoImage(
            file=relative_to_assets("entry_7.png"))
        entry_bg_7 = canvas.create_image(
            323.5,
            644.5,
            image=img_annualIncome
        )
        annual_income_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        annual_income_entry.place(
            x=241.5,
            y=625.0,
            width=164.0,
            height=31.0
        )

        image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(
            631.0,
            122.0,
            image=image_image_3
        )

        image_image_4 = PhotoImage(
            file=relative_to_assets("image_4.png"))
        image_4 = canvas.create_image(
            635.0,
            309.0,
            image=image_image_4
        )

        image_image_5 = PhotoImage(
            file=relative_to_assets("image_5.png"))
        image_5 = canvas.create_image(
            1081.0,
            662.0,
            image=image_image_5
        )

        img_applyChanges_button = PhotoImage(
            file=relative_to_assets("button_1.png"))
        apply_changes_button = Button(
            canvas, image=img_applyChanges_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: function_To_call(),
            relief="flat"
        )
        apply_changes_button.place(
            x=954.0,
            y=584.0,
            width=60.0,
            height=58.0
        )

        img_revokeChanges_button = PhotoImage(
            file=relative_to_assets("button_2.png"))
        revoke_changes_button = Button(
            canvas, image=img_revokeChanges_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.window.destroy(),
            relief="flat"
        )
        revoke_changes_button.place(
            x=1130.0,
            y=584.0,
            width=60.0,
            height=58.0
        )

        image_image_6 = PhotoImage(
            file=relative_to_assets("image_6.png"))
        image_6 = canvas.create_image(
            1057.0,
            453.0,
            image=image_image_6
        )
        
        def check_date_format():
            entered_date = transaction_date_entry.get()
            if self.validate_date_format(entered_date):
                date_added = datetime.datetime.strptime(entered_date, "%Y-%m-%d").date() 
                return date_added
            else:
                self.window.iconify()
                messagebox.showerror("Incorrect Format", "Please enter a date in the YYYY-MM-DD format")
                self.window.deiconify()
                
        transaction_date_entry = Entry(
        canvas, bd=0,
        bg="#ffffff",
        fg="#000716",
        highlightthickness=0)
        
        transaction_date_entry.place(
            x=130.5,
            y=317.0,
            width=100.0,
            height=31.0)

        check_format_button = tk.Button(
            canvas,
            text="Check Format",
            command=check_date_format,
            relief="flat")
        
        check_format_button.place(
            x=260.5,
            y=310.0,
            width=80.0,
            height=20.0)
        
        
        img_transacAmount = PhotoImage(
            file=relative_to_assets("entry_8.png"))
        entry_bg_8 = canvas.create_image(
            492.5,
            336.5,
            image=img_transacAmount
        )
        transaction_amount_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        transaction_amount_entry.place(
            x=427.5,
            y=317.0,
            width=130.0,
            height=31.0
        )

        img_transacType = PhotoImage(
            file=relative_to_assets("entry_9.png"))
        entry_bg_9 = canvas.create_image(
            801.5,
            333.5,
            image=img_transacType
        )
        transaction_type_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        transaction_type_entry.place(
            x=724.5,
            y=314.0,
            width=154.0,
            height=31.0
        )

        img_receivingAcc = PhotoImage(
            file=relative_to_assets("entry_10.png"))
        entry_bg_10 = canvas.create_image(
            1096.5,
            335.5,
            image=img_receivingAcc
        )
        receiving_account_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        receiving_account_entry.place(
            x=1019.5,
            y=316.0,
            width=154.0,
            height=31.0
        )

        # ADD DOWN: MINUS UP
        img_checkings_id = PhotoImage(
            file=relative_to_assets("entry_14.png"))
        entry_bg_14 = canvas.create_image(
            1096.5,
            200.5,
            image=img_checkings_id
        )
        checkings_id_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        checkings_id_entry.place(
            x=1023.5,
            y=185.0,
            width=145.0,
            height=25.0
        )

        

        img_accountBal = PhotoImage(
            file=relative_to_assets("entry_11.png"))
        entry_bg_11 = canvas.create_image(
            1156.5,
            424.5,
            image=img_accountBal
        )
        account_balance_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        account_balance_entry.place(
            x=1093.5,
            y=405.0,
            width=126.0,
            height=31.0
        )

        img_accountStatus = PhotoImage(
            file=relative_to_assets("entry_12.png"))
        entry_bg_12 = canvas.create_image(
            1156.5,
            481.5,
            image=img_accountStatus
        )
        account_status_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        account_status_entry.place(
            x=1093.5,
            y=462.0,
            width=126.0,
            height=31.0
        )
        
        img_transacDate = PhotoImage(file=relative_to_assets("transac_date_icon.png"))

        transaction_date_image = canvas.create_image(
            75.0,          # x-coordinate
            255.0,         # y-coordinate
            image=img_transacDate,
            anchor="nw"     # anchor point (north-west)
        )

        canvas.create_text(
            221.0,
            11.0,
            anchor="nw",
            text=account_id,
            fill="#4C4A48",
            font=("Inter Black", 55 * -1)
        )
        self.search_frame.display_searched_account(self.window, connection, search_account_query, account_id, session_indicator)
        # self.frame.display_searched_account(self.window, search_acc_query, )

        
        
        # dynamic access to the entries
        dict_for_customer_info = {
                "first_name" : firstname_entry.get() if firstname_entry.get() != "" else "", 
                "last_name" : lastname_entry.get() if lastname_entry.get() != "" else "",
                "email": email_entry.get() if email_entry.get() != "" else "",
                "address": address_entry.get() if address_entry.get() != "" else "",
                "id_type": IDType_entry.get() if IDType_entry.get() != "" else "",
                "occupation": occupation_entry.get() if occupation_entry.get() != "" else "",
                "annual_gross_income": annual_income_entry.get() if annual_income_entry.get() != "" else ""
            }
        
        dict_for_checkings_account = {
                "checkings_id" : "", 
                "account_password" : "" ,
                "balance": account_balance_entry.get() if account_balance_entry.get() != "" else "",
                "account_status": account_status_entry.get() if account_status_entry.get() != "" else "",
            }
        
        dict_for_transactions = {
                "transactions_id": self.customer.generate_transaction_id(),
                "checkings_id": checkings_id_entry.get() if checkings_id_entry.get() != "" else "",
                "transaction_type": transaction_type_entry.get() if transaction_type_entry.get() != "" else "",
                "receiving_account": receiving_account_entry.get() if receiving_account_entry.get() != "" else "",
                "transaction_date": transaction_date_entry.get() if transaction_date_entry.get() != "" else "",
                "amount": transaction_amount_entry.get() if transaction_amount_entry.get() != "" else ""
            }
        
        
        def edit_from_customer_info():
            
            self.updation_session(employee_id, "customer_id", account_id, "customer_information", dict_for_customer_info)
            
             
        def edit_from_checkings_account():
            self.updation_session(employee_id, "checkings_id", account_id, "checkings_account", dict_for_checkings_account)
            
            
        def edit_from_transactions():
            self.updation_session(employee_id, "transactions_id", account_id, "transactions", dict_for_transactions)
            
        if session_indicator == "Add User":
            
            if table_involved == "checkings_account": # add to checkings_account when customer_id is entered
                def add_checkings_account_session():
                    account_balance = account_balance_entry.get()
                    account_status = account_status_entry.get()
                    self.employee.add_into_checkings_account(connection, cursor, employee_id, account_id, account_balance, account_status, dict_for_checkings_account)
                    
                function_To_call = add_checkings_account_session
                
                       
            elif table_involved == "transactions": # add to transactions when checkings_id is entered
                def add_transaction_session():
                    transac_id = dict_for_transactions.get("transactions_id")
                    transac_type = transaction_type_entry.get()
                    receiving_acc = receiving_account_entry.get()
                    transac_date = transaction_date_entry.get()
                    amount = transaction_amount_entry.get()
                    self.employee.add_into_transactions(connection, cursor, employee_id, account_id, transac_id, transac_type, receiving_acc, transac_date, amount, dict_for_transactions)

                function_To_call = add_transaction_session


            elif table_involved == "New Account": # add new customer 
                def add_cust_info_session():
                    
                    self.employee.add_customer_information(connection, cursor, employee_id, account_id, firstname_entry.get(), lastname_entry.get(), email_entry.get(), annual_income_entry.get(), IDType_entry.get(), occupation_entry.get(), address_entry.get(), dict_for_customer_info)
                            
                function_To_call = add_cust_info_session
  


        elif session_indicator == "Edit User":
            
            if table_involved == "customer_information":
                function_To_call = edit_from_customer_info

            elif table_involved == "checkings_account":
                function_To_call = edit_from_checkings_account

            elif table_involved == "transactions":
                function_To_call = edit_from_transactions
        
        
        self.window.resizable(False, False)
        self.window.mainloop()

    
    
    # def add_customer_information(self, connection, cursor, employee_id, account_id, f_name, l_name, email, ann_income, id_type, occupation, address, dict_for_customer_info ):
    #     while True:
    #         if self.employee.proceed_to_session("addition to transactions", account_id) == "Yes":
    #             if f_name == "" or l_name== "" or email == "" or ann_income == "" or id_type == "" or occupation == "" or address == "":
    #                 messagebox.showerror("Invalid Entry Values", f"Customer: Name, Email, Income, ID Type, Occupation, Address are the only allowed info for Customer ID: {account_id}")
    #                 break
    #             else:
    #                 query = "INSERT INTO customer_information(first_name, last_name, email, address, id_type, occupation, annual_gross_income) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    #                 values = (f_name, l_name, email, address, id_type, occupation, ann_income)
    #                 cursor.execute(query, values)
    #                 connection.commit()
    #                 messagebox.showinfo("Added Credentials", "Customer Info Added to New Customer")
    #                 self.employee.add_to_sessionlog(connection, employee_id, "Add User", "Customer Information", list(values), dict_for_customer_info)
    #                 break
                
    #         else: break
    
    # def add_into_checkings_account(self, connection, cursor, employee_id, account_id, account_status, account_balance, dict_for_checkings_account):
    #     while True:
    #         if self.employee.proceed_to_session("addition to transactions", account_id) == "Yes":
    #             checkings_id = self.employee.generate_checkings_id()
    #             password = self.employee.generate_checkings_id()
    #             dict_for_checkings_account["checkings_id"] = checkings_id
    #             dict_for_checkings_account["account_password"] = password
                
    #             if account_balance == "" or account_status == "":
    #                 messagebox.showerror("Invalid Entry Values", f"Account Balance and Status are the only allowed info for Customer ID: {account_id}")
    #                 break
                
    #             else:
    #                 query = "INSERT INTO checkings_account(checkings_id, account_password, balance, account_status, customer_id) VALUES(%s, %s, %s, %s, %s)"
    #                 values = (checkings_id, password, account_balance , account_status, account_id)
    #                 cursor.execute(query, values)
    #                 connection.commit()
    #                 messagebox.showinfo("Session Status", f"Information Added to Customer {account_id} with Checkings ID: {checkings_id}")
    #                 # print(f"Balance: {account_balance},  Account Status: {account_status}")
    #                 # print(checkings_id, " and ", password)
                    
    #                 values = [checkings_id, password, account_balance, account_status] 
    #                 self.employee.add_to_sessionlog(connection, employee_id, "Add User", "Checkings Account", values, dict_for_checkings_account)

    #                 break
                
    #         else: break
    
    # def add_into_transactions(self, connection, cursor, employee_id, account_id, transac_id, transac_type, receiving_acc, transac_date, amount, dict_for_transactions):
                    
    #     if self.employee.check_account_existence(cursor, "checkings_account", "checkings_id", receiving_acc) or receiving_acc == "" or receiving_acc == "None":
    #         while True:
    #             if self.employee.proceed_to_session("addition to transactions", account_id) == "Yes":
                    
    #                 if transac_type == "" or receiving_acc == "" or transac_date == "" or amount == "":
    #                     messagebox.showerror("Invalid Entry Values", f"Transaction: Type, Receiving Account, Date and Amount are the only allowed info for Checkings ID: {account_id}")
    #                     break
    #                 else:
    #                     query = "INSERT INTO transactions (transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount) VALUES(%s, %s, %s, %s, %s, %s)"
    #                     values = (transac_id, account_id, transac_type, receiving_acc, transac_date, amount)
    #                     cursor.execute(query, values)
    #                     connection.commit()
    #                     messagebox.showinfo("Session Status", f"Transaction Added for Checkings ID: {account_id} with Transactions ID: {transac_id} ")
    #                     print(f"Transaction ID: {transac_id}, Checkings ID: {account_id}, Transaction Type: {transac_type}, Receiving Account: {receiving_acc}, Date: {transac_date}, Amount: {amount}")
    #                     values = list(values)
    #                     self.employee.add_to_sessionlog(connection, employee_id, "Add User", "Transactions", values, dict_for_transactions)
    #                     break
                    
    #             else: break
                
    #     else: messagebox.showerror("Session Error", f"Receiving account {receiving_acc} not found.")
    
 
    # def add_to_sessionlog(self, connection, employee_id, session_type, table_involved, values, specified_dictionary):
    #     i = 0
    #     for column in specified_dictionary:
    #         self.employee.add_transaction_log(connection, employee_id, session_type, table_involved, column, "None", values[i])
    #         i += 1
            
    def updation_session(self, employee_id, id_column, account_id, table_involved, dict_for_table):
        connection = self.employee.connect_database()
        cursor = connection.cursor()
        initial_values = {}
        for column in dict_for_table:
            fetched_val = self.employee.fetch_single_value(connection, cursor, table_involved, column, id_column, account_id)
            initial_values[column] = fetched_val

        
        try:
            if self.employee.proceed_to_session("modifying", account_id) == "Yes":
                # set_clause = ", ".join([f"{column} = %s" for column, value in dict_for_table.items() if value != ""])
                # print(set_clause)
                set_clause = ", ".join([f"{column} = %s" for column in dict_for_table if dict_for_table[column] != ""])
                query_val = f"UPDATE {table_involved} SET {set_clause} WHERE {id_column} = %s"
                values_tuple = tuple([value for value in dict_for_table.values() if value != ""] + [account_id])
                cursor.execute(query_val, values_tuple)
                connection.commit()
                messagebox.showinfo("Updation Status", f"Updation success for account {account_id}...")
                

                for non_empty_val in dict_for_table:
                    value = dict_for_table.get(non_empty_val)
                    if value != "":
                        modified_value = initial_values.get(non_empty_val)
                        self.employee.add_transaction_log(connection, employee_id, "Edit User", table_involved, non_empty_val, modified_value, value)
                
                    else: continue      

        except mysql.connector.Error as err:
            message_error = f"Failed to process updation to Account: {account_id} due to {err}"
            messagebox.showerror("Updation Error", message_error)
            
    
