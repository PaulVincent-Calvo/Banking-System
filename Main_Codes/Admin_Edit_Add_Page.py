import matplotlib
matplotlib.use('TkAgg')
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, messagebox
from Search_Account_Page import Search_Account_Page
from Main_Ver2 import Employee
import mysql.connector

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\final_edit_add_page\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Admin_Edit_Add_Page:
    
    def __init__(self) -> None:
        self.search_frame = Search_Account_Page()
        self.employee = Employee()
        self.connection = None

    def edit_add_page(self, account_id, toplevel_window, session_indicator): #(self,account_id, toplevel_window, session_indicator)

        self.connection = self.employee.adminMain()
        cursor = self.connection.cursor()
        search_account_query = self.employee.search_credentials(self.connection, account_id)
        print(search_account_query)
        
        
        window = toplevel_window
        window.geometry("1271x700")
        window.configure(bg = "#FFFFFF")
        

        canvas = Canvas(
            window,
            bg = "#FFFFFF",
            height = 700,
            width = 1271,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        bankcard_img = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            1003.0,
            342.0,
            image=bankcard_img
        )

        canvas.create_text(
            221.0,
            11.0,
            anchor="nw",
            text=account_id,
            fill="#4C4A48",
            font=("Inter Black", 55 * -1)
        )
        
        # Customer Information Section
        customerInfo_icons = PhotoImage(
            file=relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(
            436.0,
            532.0,
            image=customerInfo_icons
        )

        img_entryFname = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            323.5,
            437.5,
            image=img_entryFname
        )
        first_name_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        first_name_entry.place(
            x=241.5,
            y=418.0,
            width=164.0,
            height=31.0
        )
        

        img_entryLname = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        entry_bg_3 = canvas.create_image(
            323.5,
            506.5,
            image=img_entryLname
        )
        last_name_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        last_name_entry.place(
            x=241.5,
            y=487.0,
            width=164.0,
            height=31.0
        )

        img_entryEmail = PhotoImage(
            file=relative_to_assets("entry_5.png"))
        entry_bg_5 = canvas.create_image(
            323.5,
            575.5,
            image=img_entryEmail
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

        img_entryAnnualInc = PhotoImage(
            file=relative_to_assets("entry_7.png"))
        entry_bg_7 = canvas.create_image(
            323.5,
            644.5,
            image=img_entryAnnualInc
        )
        annual_income_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        print(annual_income_entry.get())
        annual_income_entry.place(
            x=241.5,
            y=625.0,
            width=164.0,
            height=31.0
        )

        img_entryIDtype = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            717.5,
            437.5,
            image=img_entryIDtype
        )
        ID_type_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        ID_type_entry.place(
            x=635.5,
            y=418.0,
            width=164.0,
            height=31.0
        )

        img_entryOccupation = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = canvas.create_image(
            717.5,
            506.5,
            image=img_entryOccupation
        )
        occupation_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        print(occupation_entry.get())
        occupation_entry.place(
            x=635.5,
            y=487.0,
            width=164.0,
            height=31.0
        )

        img_entryAddress = PhotoImage(
            file=relative_to_assets("entry_6.png"))
        entry_bg_6 = canvas.create_image(
            717.5,
            575.5,
            image=img_entryAddress
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

        bg_current_data = PhotoImage(
            file=relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(
            630.0,
            131.0,
            image=bg_current_data
        )

        imgText_changes = PhotoImage(
            file=relative_to_assets("image_5.png"))
        image_5 = canvas.create_image(
            1081.0,
            662.0,
            image=imgText_changes
        )

        img_applyChanges_but = PhotoImage(
            file=relative_to_assets("button_1.png"))
        apply_changes_button = Button(
            canvas,
            image=img_applyChanges_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:function_To_call,  # Use the function reference directly
            relief="flat"
        )
        apply_changes_button.place(
            x=954.0,
            y=584.0,
            width=60.0,
            height=58.0
        )

        img_revokeChanges_but = PhotoImage(
            file=relative_to_assets("button_2.png"))
        revoke_changes_button = Button(
            canvas,
            image=img_revokeChanges_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        revoke_changes_button.place(
            x=1130.0,
            y=584.0,
            width=60.0,
            height=58.0
        )
        
        # Transaction Section
        bg_transaction_section = PhotoImage(
            file=relative_to_assets("image_4.png"))
        image_4 = canvas.create_image(
            635.0,
            309.0,
            image=bg_transaction_section
        )

        img_transacDate_but = PhotoImage(
            file=relative_to_assets("button_3.png"))
        transaction_date_button = Button(
            canvas,
            image=img_transacDate_but,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        transaction_date_button.place(
            x=75.0,
            y=261.0,
            width=177.0,
            height=45.0
        )

        img_entryTransacAmount_ = PhotoImage(
            file=relative_to_assets("entry_8.png"))
        entry_bg_8 = canvas.create_image(
            492.5,
            336.5,
            image=img_entryTransacAmount_
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

        img_entryTransacType = PhotoImage(
            file=relative_to_assets("entry_9.png"))
        entry_bg_9 = canvas.create_image(
            801.5,
            333.5,
            image=img_entryTransacType
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

        # Checkings Account Section
        bg_checkingsAcc_section = PhotoImage(
            file=relative_to_assets("image_6.png"))
        image_6 = canvas.create_image(
            1057.0,
            453.0,
            image=bg_checkingsAcc_section
        )

        img_entryReceivingAcc = PhotoImage(
            file=relative_to_assets("entry_10.png"))
        entry_bg_10 = canvas.create_image(
            1096.5,
            335.5,
            image=img_entryReceivingAcc
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

        img_entryAccBal = PhotoImage(
            file=relative_to_assets("entry_11.png"))
        entry_bg_11 = canvas.create_image(
            1156.5,
            424.5,
            image=img_entryAccBal
            

        )
        account_balance_entry = Entry(
            canvas, 
            bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        
        def get_balance():
         x = account_balance_entry.get()
         print(x)
         return x
            
        
        
        get_balance()
        
        account_balance_entry.place(
            x=1093.5,
            y=405.0,
            width=126.0,
            height=31.0
        )
        get_balance()
        
        img_entryAccStatus = PhotoImage(
            file=relative_to_assets("entry_12.png"))
        entry_bg_12 = canvas.create_image(
            1156.5,
            481.5,
            image=img_entryAccStatus
        )
        account_status_entry = Entry(
            canvas, bd=0,
            bg="#ffffff",
            fg="#000716",
            highlightthickness=0
        )
        
        print(account_status_entry.get())
        account_status_entry.place(
            x=1093.5,
            y=462.0,
            width=126.0,
            height=31.0
        )
        
        self.search_frame.display_searched_account(window, self.connection, search_account_query, account_id, session_indicator)
        
       # Buttons
        if search_account_query == "SELECT * FROM customer_information WHERE customer_id = %s":
            def add_into_checkings_account():
                
                try:

                    
                    if self.employee.check_account_existence(cursor, "checkings_account", "customer_id", account_id):
                        messagebox.showinfo("Invalid Session", "Customer ID already exists in Checkings Account")
                    else:
                        checkings_id_generator = self.employee.generate_checkings_id()
                        password_generator = self.employee.generate_checkings_id()
                        account_balance = account_balance_entry.get()
                        account_status = account_status_entry.get()
                        query = "INSERT INTO checkings_account(checkings_id, account_password, balance, account_status, customer_id) VALUES(%s, %s, %s, %s, %s)"
                        values = (checkings_id_generator, password_generator, account_balance_entry.get() , account_status, account_id)
                        cursor.execute(query, values)
                        self.connection.commit()
                        print(account_balance)
                        print(account_status)
                        print(checkings_id_generator, " and ", password_generator)
                        
                except mysql.connector.Error as error:
                    print(error)

            function_To_call = add_into_checkings_account()

        elif search_account_query == "SELECT * FROM checkings_account WHERE checkings_id = %s":
            pass

        elif search_account_query == "SELECT * FROM transactions WHERE transactions_id = %s":
            pass

        elif search_account_query == "New Account":
            pass

        get_balance()

        window.resizable(False, False)
        window.mainloop()


    
    
    def add_customer(self, account_id, session_indicator):

        if account_id == "New":
            pass # can only add to customer information
           
        elif account_id == "Customer ID":
            pass # can only add checkings account

        elif account_id == "Checkings Account":
            pass # can only add transactions
        
        else:
            messagebox.showinfo("Invalid Session", "Add/Edit Proper Values")
    


admin_edit_page = Admin_Edit_Add_Page()
top_level = Toplevel()
admin_edit_page.edit_add_page(11, top_level, "Add user")
            
