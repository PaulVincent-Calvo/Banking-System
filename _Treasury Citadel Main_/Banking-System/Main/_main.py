import matplotlib
matplotlib.use('TkAgg')
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
    self.connection = None
    self.cursor = None
    

  def Main(self):
    session_status = False
    while True:
      self.loading_page.run_loading_page()
      login_as = self.user_login.login_page() 
      if login_as[0] is None and login_as[1] == "":
        break

      else:
        self.connection = login_as[0]
        self.cursor = self.connection.cursor()
        dedicated_id = login_as[1]
        
        user_type = self.get_user_type(dedicated_id)
        session_status = True
        
        if dedicated_id != "":
          if user_type == "Employee" and session_status == True:
            print(f"Employee: {dedicated_id}")
            admin_session = self.admin_main.admin_mainframe(dedicated_id, self.connection, self.cursor)
            if admin_session == "Go Back to Login":
              continue

              
          elif user_type == "Customer" and session_status == True:
            print(f"Customer: {dedicated_id}")
            customer_session = self.customer_main.customer_mainframe(dedicated_id, self.connection, self.cursor)
            if customer_session == True:
              continue

        else:
          break
  
  
  
  def get_user_type(self, dedicated_id):
    if self.employee.check_account_existence(self.cursor, "employee_admin", "employee_id", dedicated_id):
        return "Employee"
    else:
        return "Customer"
      
      
      
if __name__ == "__main__":
  main = GUI_Main()
  main.Main()