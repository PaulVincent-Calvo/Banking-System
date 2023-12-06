import time
import matplotlib
matplotlib.use('TkAgg')
import subprocess
from raw_main import Employee, Customer
from login_page import Login_Page
from admin_page import Admin_Page
from customer_page import Customer_Page
from loading_page import Loading_Page



class GUI_Main:
  
  def __init__(self):
    self.employee = Employee()
    self.customer = Customer()
    self.user_login = Login_Page()
    self.admin_main = Admin_Page()
    self.customer_main = Customer_Page()
    self.loading_page = Loading_Page()
    

  def Main(self):
    global session_status
    session_status = False
    while True:
      self.loading_page.run_loading_page()
      login_as = self.user_login.login_page() # calling a method from another file/class oneinamillion
      if login_as[0] is None and login_as[1] == "":
        break

      else:
        connection = login_as[0]
        dedicated_id = login_as[1]
        
        if self.employee.new_check_account_existence(connection, "employee_admin", "employee_id", dedicated_id):
          user_type = "Employee"
          session_status = True
          
        else:
          user_type = "Customer"
          session_status = True
        
        if dedicated_id != "":
          if user_type == "Employee" and session_status == True:
            print(f"Employee: {dedicated_id}")
            admin_session = self.admin_main.admin_mainframe(dedicated_id)
            if admin_session == "Go Back to Login":
              print(admin_session)
              continue
            
            elif admin_session == "Reload Page":
              print(admin_session)
              self.reload_page(dedicated_id)
               
              
          elif user_type == "Customer" and session_status == True:
            print(f"Customer: {dedicated_id}")
            customer_session = self.customer_main.customer_mainframe(dedicated_id)
            if customer_session == True:
              continue

        else:
          break
  
  
  
  def reload_page(self, dedicated_id):
    while True:
      self.loading_page.run_loading_page()
      admin_session = self.admin_main.admin_mainframe(dedicated_id)
      if admin_session == "Go Back to Login":
        break
          
      
  
  # def call_loading_page(self):
  #   self.call_file(r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\Main_Codes\loading_page.py")
  #   time.sleep(0.3)
    
        
  # def call_file(self, file_path):
  #   try:
  #     return_code = subprocess.call(['python', file_path])
      
  #     if return_code == 0:
  #       print("Script executed successfully.")
  #     else:
  #       print(f"Script failed with return code: {return_code}")
  #   except Exception as e:
  #       print(f"An error occurred: {e}")
      
      
main = GUI_Main()
main.Main()