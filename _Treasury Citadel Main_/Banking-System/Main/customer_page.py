

from decimal import Decimal
from pathlib import Path
from data_charts import Data_Charts
import time

import mysql.connector
from raw_main import Customer
from tkinter import DoubleVar, IntVar, StringVar, Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from transaction_history_page import Session_Transaction_Histories

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\GUI Assets\_customer_page_assets\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Customer_Page:
    
    def __init__(self):
        self.customer = Customer()
        self.transac_history = Session_Transaction_Histories()
        self.charts = Data_Charts()
        global logout_var
        logout_var = False
        global display_transactions_history
        display_transactions_history = 0
        
    
        
    def customer_mainframe(self, checkings_id):
        
        self.customer_main_window = Tk()
        self.customer_main_window.geometry("1540x765")
        self.customer_main_window.configure(bg = "#FFFFFF")
        self.customer_main_window.title("Customer Landing Page")
        
        connection = self.customer.customerMain()
        cursor = connection.cursor()
        
        canvas = Canvas(
            self.customer_main_window,
            bg = "#FFFFFF",
            height = 765,
            width = 1540,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(273.0, 496.0, image=image_image_1)

        canvas.create_rectangle(
            937.0,
            477.0,
            1799.0,
            933.0,
            fill="#FFFFFF",
            outline="")

        session_log_bg = PhotoImage(
            file=relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(
            1035.0,
            498.0,
            image=session_log_bg
        )

        hello_text = canvas.create_text(
            34.0, 32.0,
            anchor="nw", text="Hello, ",
            fill="#4C4A48", font=("Inter", 50 * -1))

        username_text = canvas.create_text(
            34.0, 116.0,
            anchor="nw", text=self.customer.fetch_customer_name(cursor, checkings_id),
            fill="#4C4A48", font=("Inter Bold", 75 * -1))

        balance_text_img = PhotoImage(
            file=relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(
            1037.0,
            69.0,
            image=balance_text_img
        )

        balance_bg = PhotoImage(
            file=relative_to_assets("image_4.png"))
        image_4 = canvas.create_image(
            1037.0,
            150.0,
            image=balance_bg
        )

        img_depoButton = PhotoImage(
            file=relative_to_assets("button_1.png"))
        deposit_button = Button(
            image=img_depoButton,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: deposit_session(),
            relief="flat"
        )
        deposit_button.place(
            x=90.0,
            y=508.0,
            width=71.561279296875,
            height=72.6612548828125
        )

        img_transfrBut = PhotoImage(
            file=relative_to_assets("button_2.png"))
        transfer_button = Button(
            image=img_transfrBut,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: transfer_session(),
            relief="flat"
        )
        transfer_button.place(
            x=233.561279296875,
            y=508.0,
            width=71.561279296875,
            height=72.6612548828125
        )

        img_withdrwBut = PhotoImage(
            file=relative_to_assets("button_3.png"))
        withdraw_button = Button(
            image=img_withdrwBut,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: withdraw_session(),
            relief="flat"
        )
        withdraw_button.place(
            x=368.12255859375,
            y=508.0,
            width=71.56103515625,
            height=72.6612548828125
        )

        total_deposited_var = StringVar()
        initial_total_depo = self.customer.fetch_total_amount_by_session(cursor, checkings_id, 'Deposit')
        total_deposited_var.set(str(initial_total_depo))
        total_deposits_text = canvas.create_text(
            136.06884765625,
            683.925537109375,
            anchor="nw",
            text=total_deposited_var.get(),
            fill="#FFFFFF",
            font=("Inter ExtraBold", 11 * -1)
        )
        
        total_transferred_var = StringVar()
        initial_total_transferred = self.customer.fetch_total_amount_by_session(cursor, checkings_id, 'Transfer')
        total_transferred_var.set(str(initial_total_transferred))
        total_transferred_text= canvas.create_text(
            272.06884765625,
            683.925537109375,
            anchor="nw",
            text=total_transferred_var.get(),
            fill="#FFFFFF",
            font=("Inter ExtraBold", 11 * -1)
        )

        total_withdrew_var = StringVar()
        initial_total_withdrew = self.customer.fetch_total_amount_by_session(cursor, checkings_id, 'Withdraw')
        total_withdrew_var.set(str(initial_total_withdrew))
        total_withdrew_text = canvas.create_text(
            411.06884765625,
            683.925537109375,
            anchor="nw",
            text=total_withdrew_var.get(),
            fill="#FFFFFF",
            font=("Inter ExtraBold", 11 * -1)
        )
        
        
        holder = ""
        def log_out_session():
            close_window = messagebox.askquestion("Exit", "Confirm Logout", icon = "warning")
            if close_window == 'yes':
                print("Logging Out")
                self.customer_main_window.destroy()
                holder = "Go Back to Login"
                print(holder)
                
            elif close_window == 'no':
                holder = ""
                
        if holder == "Go Back to Login":
            employee_id = ""
            print("Going Back to LogIn Page")
            return holder
        

        
        img_logoutBut = PhotoImage(
            file=relative_to_assets("button_4.png"))
        logout_button = Button(
            image=img_logoutBut,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: log_out_session(),
            relief="flat"
        )
        logout_button.place(
            x=29.0,
            y=17.0,
            width=87.0,
            height=22.0
        )
        
        # entries
        img_accEntry = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            270.5,
            321.0,
            image=img_accEntry
        )
        account_number_entry = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        account_number_entry.place(
            x=101.0,
            y=293.0,
            width=339.0,
            height=50.0
        )
        
        
        img_amountEntry = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            273.5,
            434.0,
            image=img_amountEntry
        )
        amount_entry = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        amount_entry.place(
            x=104.0,
            y=405.0,
            width=339.0,
            height=50.0
        )
        
        logo_image = PhotoImage(
            file=relative_to_assets("image_5.png"))
        image_5 = canvas.create_image(
            441.0,
            75.0,
            image=logo_image
        )
        
        # initial bal (updates once a transac is performed)
        balance_var = StringVar()
        initial_balance = self.customer.check_balance(connection, checkings_id)
        balance_var.set(str(initial_balance)) 
        balance_text = canvas.create_text(
            775.0,
            113.0,
            anchor="nw",
            text=balance_var.get(), 
            fill="#000000",
            font=("Inter Bold", 50 * -1)
        )


        img_transacChart = PhotoImage(
            file=relative_to_assets("button_5.png"))
        transaction_chart_button = Button(
            image=img_transacChart,
            borderwidth=0,
            highlightthickness=0,
            command = lambda: self.charts.run_transaction_chart("Customer", checkings_id),
            relief="flat"
        )
        transaction_chart_button.place(
            x=1324.0,
            y=273.0,
            width=176.0,
            height=72.0
        )
        
        def deposit_session():
            confirm_deposit = self.customer_session('Deposit', account_number_entry.get(), amount_entry.get())
            while True:
                if confirm_deposit[0] == True:
                    deposit_amount = confirm_deposit[1]
                    deposit_status = self.customer.customer_deposit(connection, checkings_id, deposit_amount)

                    if deposit_status == True:
                        updated_balance = self.customer.check_balance(connection, checkings_id)
                        balance_var.set(str(updated_balance))
                        canvas.itemconfig(balance_text, text=balance_var.get())
                        
                        # for the total deposited
                        updated_total_deposits = self.customer.fetch_total_amount_by_session(cursor, checkings_id, 'Deposit')
                        total_deposited_var.set(str(updated_total_deposits))
                        canvas.itemconfig(total_deposits_text, text=total_deposited_var.get())
                        messagebox.showinfo("Session Status", f"₱ {deposit_amount} deposited.")
                        break
                
                else: break

        def transfer_session():
            recepient_account = account_number_entry.get()
            if self.customer.check_account_existence(cursor, "checkings_account", "checkings_id", recepient_account):
                confirm_transfer = self.customer_session('Tranfer', account_number_entry.get(), amount_entry.get())

                while True:
                    if confirm_transfer[0] == True:
                        trasnfer_amount = confirm_transfer[1]
                        transfer_status = self.customer.customer_transfer(connection, checkings_id, trasnfer_amount, account_number_entry.get())

                        if transfer_status == True:
                            updated_balance = self.customer.check_balance(connection, checkings_id)
                            balance_var.set(str(updated_balance))
                            canvas.itemconfig(balance_text, text=balance_var.get())

                            updated_total_transfers = self.customer.fetch_total_amount_by_session(cursor, checkings_id, 'Transfer')
                            total_transferred_var.set(str(updated_total_transfers))
                            canvas.itemconfig(total_transferred_text, text=total_transferred_var.get())
                            messagebox.showinfo("Session Status", f"₱ {trasnfer_amount} trasnferred to {account_number_entry.get()}.")
                            break
                    
                    else: break

            else:
                messagebox.showerror("Invalid Session", " Recepient Account Inexistent")


        def withdraw_session():
            confirm_withdrawal = self.customer_session('Withdrawal', account_number_entry.get(), amount_entry.get())
            
            while True:
                if confirm_withdrawal[0] == True:
                    withdrawal_amount = confirm_withdrawal[1]
                    withdrawal_status = self.customer.customer_withdraw(connection, checkings_id, withdrawal_amount)
                    
                    if withdrawal_status == True:
                        updated_balance = self.customer.check_balance(connection, checkings_id)
                        balance_var.set(str(updated_balance))
                        canvas.itemconfig(balance_text, text=balance_var.get())

                        updated_total_withdraws = self.customer.fetch_total_amount_by_session(cursor, checkings_id, 'Withdraw')
                        total_withdrew_var.set(updated_total_withdraws)
                        canvas.itemconfig(total_withdrew_text, text=total_withdrew_var.get())
                        messagebox.showinfo("Session Status", f"₱ {withdrawal_amount} withdrew.")
                        break
                
                else: break
        
        self.transac_history.transactions_customer(self.customer_main_window, checkings_id)
            
        self.customer_main_window.resizable(False, False)
        self.customer_main_window.mainloop()
        
        
        
    def customer_session(self, session_type, account_number, amount):
        try:
            if account_number == "" and amount != "":
                try:
                    amount_int = int(amount)
                    amount_decimal = Decimal(amount_int)
                except ValueError:
                    try:
                        amount_float = float(amount)
                        amount_decimal = Decimal(amount_float)
                    except ValueError:
                        messagebox.showerror(f"{session_type} Status", "Invalid amount. Please enter a valid number.")
                        return [False, None]
                    
                status = self.confirm_transaction_session(session_type)
                if status == "Proceed":
                    return [True, amount_decimal]
                else:
                    return [False, ""]
                    
            
            
            elif account_number != "" and amount != "":
                try:
                    amount_int = int(amount)
                    amount_decimal = Decimal(amount_int)
                except ValueError:
                    try:
                        amount_float = float(amount)
                        amount_decimal = Decimal(amount_float)
                    except ValueError:
                        messagebox.showerror(f"{session_type} Status", "Invalid amount. Please enter a valid number.")
                        return [False, None]

                status = self.confirm_transaction_session(session_type)
                if status == "Proceed":
                    return [True, amount_decimal]
                else:
                    return [False, ""]
                # messagebox.showinfo(f"{session_type} Status", f"Confirm {session_type}?")
                # return [True, amount_decimal]
            
            else:
                messagebox.showerror(f"{session_type} Status", "Invalid Session..")
                return [False, None]

        except ValueError:
            messagebox.showerror(f"{session_type} Status", "Invalid amount. Please enter a valid number.")
            return [False, None]
        
        
    def confirm_transaction_session(self, transaction_type):
        confirm = messagebox.askquestion("Confirm Session", f"Verify {transaction_type}", icon="warning")
        status = "Proceed" if confirm == 'yes' else "Revoke"
        return status
        
        
    
# customer_page = Customer_Page()
# customer_page.customer_mainframe("ATC232")
