import matplotlib
matplotlib.use('TkAgg')

import subprocess
from Main_Ver2 import Employee, Customer
from Login_Page import Login_Page
from Final_Admin_LandingPage import Admin_Page

class GUI_Main:
  
  def __init__(self):
    self.user_login = Login_Page()
    self.admin_main = Admin_Page()

  def Main(self):
      login_as = self.user_login.login_page() # calling a method from another file/class oneinamillion
      user_type = login_as[0]  # either Employee or User
      dedicated_id = login_as[1] # employee or customer id
      
      if user_type == "Employee":
        self.admin_main.admin_mainframe(dedicated_id)
        
    
  def call_file(self, file_path):
    try:
      return_code = subprocess.call(['python', file_path])
      
      if return_code == 0:
        print("Script executed successfully.")
      else:
        print(f"Script failed with return code: {return_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
      

main = GUI_Main()
main.Main()
