
import matplotlib
matplotlib.use('TkAgg')
from pathlib import Path
import time
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from raw_main import Employee, Customer, User
from subprocess import call

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\GUI Assets\login_assets\ver2\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Login_Page:
    
    def __init__(self):
        self.employee = Employee()
        self.customer = Customer()
        self.dedicated_id = None  # Variable to store dedicated ID
        self.login_window = None
        self.terminate_flag = False
        # self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        # self.shift = 30
        
    
    def login_page(self):
        self.login_window = Tk()
        self.login_window.geometry("595x650")
        self.login_window.configure(bg="#FAFBFD")
        self.login_window.title("Log In Page")
        self.login_window.protocol("WM_DELETE_WINDOW", self.terminate_program)
            
        connection = self.employee.connect_database()
        cursor = connection.cursor()

        login_canvas = Canvas(
            self.login_window,
            bg="#FAFBFD",
            height=650,
            width=595,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        login_canvas.place(x=0, y=0)

        treasury_imageText = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = login_canvas.create_image(313.0, 165.0, image=treasury_imageText)

        upperline_image = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = login_canvas.create_image(297.0, 12.0, image=upperline_image)

        bankcard_image = PhotoImage(file=relative_to_assets("image_3.png"))
        image_3 = login_canvas.create_image(303.0, 430.0, image=bankcard_image)

        password_entry_image = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = login_canvas.create_image(297.5, 436.0, image=password_entry_image)
        password_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="•")
        password_entry.place(x=170.0, y=414.0, width=255.0, height=34.0)

        id_entry_image = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = login_canvas.create_image(297.5, 332.0, image=id_entry_image)
        dedicatedID_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        dedicatedID_entry.place(x=170.0, y=310.0, width=255.0, height=34.0)
        
        login_canvas.create_text(165.0, 295.0,anchor="nw", text="Dedicated ID", fill="#4C4A48", font=("Inter Black", 14 * -1))
        login_canvas.create_text(165.0, 401.0, anchor="nw", text="Password", fill="#4C4A48", font=("Inter Black", 14 * -1))
        
        emp_login_status = lambda: self.verify_login("Employee", dedicatedID_entry.get(), password_entry.get())
        empLogin_image = PhotoImage(file=relative_to_assets("button_1.png"))
        employee_login_button = Button(
            image=empLogin_image,
            borderwidth=0,
            highlightthickness=0,
            command=emp_login_status,
            relief="flat"
        )
        employee_login_button.place(x=152.0, y=490.0, width=249.45361328125, height=53.0)

        cust_login_status = lambda: self.verify_login("Customer", dedicatedID_entry.get(), password_entry.get())
        custLogin_image = PhotoImage(file=relative_to_assets("button_2.png"))
        customer_login_button = Button(
            image=custLogin_image,
            borderwidth=0,
            highlightthickness=0,
            command=cust_login_status,
            relief="flat"
        )
        customer_login_button.place(x=152.0, y=543.0, width=249.45361328125, height=53.0)

        logo_image = PhotoImage(file=relative_to_assets("image_4.png"))
        image_4 = login_canvas.create_image(296.0, 107.0, image=logo_image)
            
        self.login_window.resizable(False, False)
        self.login_window.mainloop()
        
        
        if self.terminate_flag:
            print("Program terminated")
            return [None, "", "Terminate"]
        else:
            print("User logged in")
            return [connection, self.dedicated_id, ""]
            
            
    def show_login_status(self, status, message_desc=""):
        message = "Log In Successful!" if status else f"Log In Failed: {message_desc}"
        formatted_message = " \n".join([message[i:i+40] for i in range(0, len(message), 40)])
        messagebox.showinfo("Login Status", formatted_message)
        if message == "Log In Successful!":
            self.login_window.destroy()
        
    
    def verify_login(self, user_type, id, password):
        Dedicated_ID = id
        Password = password
        self.dedicated_id = Dedicated_ID
        
        if user_type == "Employee":
            connection_established = self.employee.adminMain()
            if connection_established:
                login_success = self.employee.login(connection_established, Dedicated_ID, Password)
                if login_success:
                    self.show_login_status(True, "")
                    return True
                elif login_success == False: 
                    self.show_login_status(False, "Account Non-existent or Incorrect Password")
                    return False
                    
        elif user_type == "Customer":
            connection_established = self.customer.customerMain()
            if connection_established:
                login_success = self.customer.login(connection_established, Dedicated_ID, Password)
                if login_success:
                    self.show_login_status(True, "")
                    return True
                elif login_success == False:
                    self.show_login_status(False, "Account Non-existent or Incorrect Password")
                    return False
    
    
    def terminate_program(self):
        close_session = messagebox.askquestion("Exit", "Exit the Program", icon = 'warning')
        if close_session == 'yes':
            print("Closing Program")
            self.login_window.destroy()
            self.terminate_flag = True