import subprocess
import random
import string
import time
from tkinter import messagebox
import mysql.connector
import os
from decimal import Decimal, DecimalException # for Decimal datatype input in mysql
from tabulate import tabulate # for precise tables & columns formatting 
from datetime import datetime
from abc import ABC, abstractmethod



# NOTE: Transactions ID (to be generate by JB's algo)
# NOTE: pending Transactions ID


class User(ABC): # NOTE: all functions to be used in child classes (Employee, Customer) are included in here
  
  def __init__(self, host, username, password, database): # encapsulation
    self._host = host
    self._username = username
    self._password = password
    self._database = database
    self._connection = None

  @abstractmethod
  def add_transaction_log(self):
    pass

  @abstractmethod
  def view_transaction_log(self):
    pass
  
  @abstractmethod
  def login(self):
    pass
  

    
  def display_error(self, error_message, error_type = None):
    if error_type:
      print(f"\n\t{error_type} Error: ..... {error_message} .....")
      
    else:
      print(f"\n\tError:...... {error_message}'''''")
    
    if not self.continue_session():
      return
    
  def connect_database(self):
    try:                     # NOTE: all users who will access the database must be connected to the same network
      host = self._host  # Set to this according to your internet's ipv4 address (to check the ip address, go to the terminal and type: ipconfig)
      username = self._username
      password = self._password
      database = self._database

      self.connection = mysql.connector.connect(
          host= host,
          user= username,
          password= password,
          database= database)
    
      print("Database Initialization Successful...")
    
    except mysql.connector.Error as error:
      error_message = f"MySQL: {error}"
      messagebox.showerror("Error", error_message)
      
    return self.connection

  def check_database_connection(self):
    if self.connection is not None:
      return True
    else:
      return False

  def close_database(self):
    if self._connection:
      self._connection.close()
      print("Database Connection Closed.")
            
  def continue_session(self): # dedicated for looping purposes
    continue_session = int(input("\n\nContinue Session (1 | 0): "))
    return 1 if continue_session == 1 else 0

  def format_table(self, cursor): # using the tabulate library
    try:
      rows = cursor.fetchall()
      if rows:
        headers = [desc[0] for desc in cursor.description] # extract column names from the cursor.description
        table = tabulate(rows, headers, tablefmt="pretty") # use the tabulate function to format the results as a table
        print(table)
      else:
          print("No records found.")
          
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")
    
  def display_rows_affected(self, cursor, ID, IDContent):
    print(f"\n\t{cursor.rowcount} session initiated| {ID}: {IDContent}")

  def confirm_action(self):
    confirm = int(input("\n\tConfirm Selected Action | 1 | 0 |: "))
    return True if confirm == 1 else False
    
  def display_current_value(self, column, current_value):
    print(f"\n\tCurrent {column.capitalize()}: {current_value}")

  def deletion_status(self, status, account_id):
        status_message = f"Account {account_id} deleted successfully.." if status else f"Error for the deletion of account {account_id}"
        messagebox.showinfo("Deletion Status", status_message) if status else messagebox.showerror("Deletion Error", status_message)
  
  def confirm_deletion(self, window, account_id):
        confirm = messagebox.askquestion("Confirm Session", f"Delete Information for Account {account_id} ?\nNote All Records will be deleted due to foreign key referencing...")
        status = "Deletion Initiated" if confirm == 'yes' else "Deletion Revokes"
        return status
      
  def proceed_to_session(self, session_type, account_id):
        proceed = messagebox.askquestion("Session", f"You will be {session_type} for account {account_id}.")
        status = "Yes" if proceed == 'yes' else "No"
        return status      
      
  def logout(self):
        close_window = messagebox.askquestion("Exit", "Confirm Logout", icon = "warning")
        status = "Go Back to Login" if close_window == 'yes' else ''
        return status

  
      
    
  # NOTE: Input Handling
  def handle_decimal_value_exception(self, description, id_content, value_type): # resuable exception handling for decimal types inputs
    try:
      amount = self.get_decimal_input(f"\n\t{description} {id_content} {value_type}: ")
      return amount
    except DecimalException as de:
      self.display_error(de, "Decimal ValueError")
      return 0


  # NOTE: Searching/Selecting Queries
  def select_all_rows(self, cursor, table):
    try:
      query = f"SELECT * FROM {table}"
      cursor.execute(query)
      self.format_table(cursor) # prints the formatted tables
      
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;") # undo the changes made during the transaction/session
  
  def check_account_existence(self, cursor, table, id_column, id_content):    
    try:
      query = f"SELECT * FROM {table} WHERE {id_column} = %s"
      cursor.execute(query, (id_content,))
      account_exists = cursor.fetchone() # checks the account's existence
      return account_exists
    
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")

  def fetch_single_value(self, connection, cursor, table, column, id_column, id_content): # function for DISPLAYING single values
    try:
      cursor = connection.cursor()
      query = f"SELECT {column} FROM {table} WHERE {id_column} = %s"
      value = id_content
      cursor.execute(query,(value,))
      Result = cursor.fetchone()
      return Result[0]#  returns the first column value of the first row in the result se
    
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")

  def search_credentials(self, connection, dedicated_id):
    cursor = connection.cursor()
    try:
      if self.check_account_existence(cursor, "customer_information", "customer_id", dedicated_id):
        return "SELECT * FROM customer_information WHERE customer_id = %s"

      elif self.check_account_existence(cursor, "checkings_account", "checkings_id", dedicated_id):
        return "SELECT * FROM checkings_account WHERE checkings_id = %s"

      elif self.check_account_existence(cursor, "transactions", "transactions_id", dedicated_id):
        return "SELECT * FROM transactions WHERE transactions_id = %s"
      
      elif dedicated_id == "New" or dedicated_id == "New Account":
        return "New Account"

      else:
        return "Account Non-existent"

    except mysql.connector.Error as errro:
      print(errro)

  # NOTE: Updating Query: employs optimistic concurreny control(checks if the timestamp and version during the reading/searching
  # is the same during the writing/updating period ; if yes, the update proceeds; if not, a waiting time until the next session is initiated)
  
  def updating_query(self, connection, cursor, table, column, ID, IDcontent, value):
    try:
      cursor.execute("START TRANSACTION;")
      update_attempt = 0
      max_attempts = 3 
      waiting_time = 5
      
      while update_attempt < max_attempts:
        cursor.execute(f"SELECT version, last_modified FROM {table} WHERE {ID} = %s;", (IDcontent,)) # reads the current version(a placeholder varaiable) and timestamp of the record
        result = cursor.fetchone()
        current_version, last_modified = result[0], result[1] # 0 = version & 1 = last_modified(timestamp)
        
        print("\n\tProcessing.....")
        time.sleep(2) 
        
        # NOTE: the current timestamp must match the last_modified timestamp to proceed to the update
        main_query = f"UPDATE {table} SET {column} = %s, version = version + 1, last_modified = CURRENT_TIMESTAMP WHERE {ID} = %s AND last_modified = %s"
        cursor.execute(main_query, (value, IDcontent, last_modified))
        connection.commit()
        
        if cursor.rowcount > 0: # Update successful
          os.system('cls')
          self.display_rows_affected(cursor, ID, IDcontent)
          break

        else:
          print(f"Update failed. Retrying after {waiting_time} seconds...")
          update_attempt += 1
          time.sleep(waiting_time) # 5 sec.
          
      if update_attempt == max_attempts:
        print(f"Maximum update attempts reached. Update aborted.")
        
      return True
            
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")
      raise

    

    
class Employee(User): # NOTE: inherits from USER 
  
  def __init__(self): #  accept an instance of BankingSystem and store it as an attribute
    super().__init__(host="localhost", 
                     username="root",
                     password="",
                     database="treasury_citadel_database")

    #self.banking_system = banking_system # to be used in the adminMain() 

  
  def login(self, connection, dedicated_id, dedicated_password):
    cursor = connection.cursor()
    table = "employee_admin"
    
    if self.check_account_existence(cursor, table, "employee_id", dedicated_id):
      query = f"SELECT * FROM {table} WHERE employee_password = %s"
      cursor.execute(query, (dedicated_password,))
      verified_user = cursor.fetchone() # checks the password's existence
    
      if verified_user:
        return True
      
      else:
        return False
        
    else:
      return False
        

  def generate_checkings_id(self):
    alphanumeric = string.ascii_letters + string.digits
    return 'ATC' + ''.join(random.choice(alphanumeric).capitalize() for _ in range(3))

  def generate_checkingsAcc_password(self):
    generated_account_id = self.generate_checkings_id()
    alphanumeric = string.ascii_letters + string.digits
    return generated_account_id + ''.join(random.choice(alphanumeric).capitalize() for _ in range(3))


  # NOTE: Transaction Logs
  def insertion_transaction_log(self, connection, cursor, employee_id, session_type, table_involved, column_involved, modified_value, stored_value):
    try:
      cursor.execute("SET foreign_key_checks = 0")
      query = "INSERT INTO session_log (employee_id, session_type, table_involved, column_involved, modified_value, stored_value, status) VALUES(%s, %s, %s, %s, %s, %s, %s)"
      values = (employee_id, session_type, table_involved, column_involved, modified_value, stored_value, "Successful")
      cursor.execute(query, list(values))
      connection.commit()
    
    except mysql.connector.Error as err:
      self.display_error(err, "MySQL")

    finally:
      cursor.execute("SET foreign_key_checks = 1")
      
  def add_transaction_log(self, connection, employee_id, session_type, table_involved, column_involved, modified_value, stored_value):
    cursor = connection.cursor()
    try:
      if isinstance(column_involved, list): # for multiple columns and values(data atomicity must be maintained)
        for col, val in zip(column_involved, stored_value):
          self.insertion_transaction_log(connection, cursor, employee_id, session_type, table_involved, col, modified_value, val)
      
      else:
        self.insertion_transaction_log(connection, cursor, employee_id, session_type, table_involved, column_involved, modified_value, stored_value)

      self.display_rows_affected(cursor, "Session Log ID", cursor.lastrowid)

    except mysql.connector.Error as error:
        self.display_error(error, "MySQL")
        cursor.execute("ROLLBACK;")

  def view_transaction_log(self, connection):
    try:
      cursor = connection.cursor()
      os.system('cls')
      print("\n\tFetching.....")
      time.sleep(2)
      os.system('cls')
      print(f"\n\t\t\t\t\t-------Admin Transaction Log History-------")
      cursor.execute("SELECT * FROM session_log")
      self.format_table(cursor)
      
      input("Press Enter to continue...")
      os.system('clear') 
      
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")
    
  def add_to_sessionlog(self, connection, employee_id, session_type, table_involved, values, specified_dictionary):
        i = 0
        for column in specified_dictionary:
            self.add_transaction_log(connection, employee_id, session_type, table_involved, column, "None", values[i])
            i += 1


  # NOTE: Foreign key constraints maintain referential integrity, ensuring that a user can only be deleted IF AND ONLY IF its references in related tables have been deleted
  def deletion_query(self, connection, cursor, table, column, ID):
    try:
      cursor = connection.cursor()
      query = f"DELETE FROM {table} WHERE {column} = %s"
      cursor.execute(query, (ID,))
      connection.commit()

    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")

  def delete_user_by_ID(self, connection, cursor, employee_id, table, id_column, id_content):

      print("delete user accessed")
      try:
        cursor.execute("SET foreign_key_checks = 0") # disabling foreign key checks temporarily to avoid violating foreign key constraints
        
        if table == "customer_information":
          delete_main_value = self.deletion_query(connection, cursor, table, id_column, id_content )# NOTE: query for deleting the PARENT table's VALUE
          delete_sub_values = [ #NOTE: putting the deletion queries for CHILD tables into a list iterable
              "DELETE FROM transactions WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s)",
              "DELETE FROM checkings_account WHERE customer_id = %s"]
          
        elif table == "checkings_account":
          delete_main_value = self.deletion_query(connection, cursor, table, id_column, id_content )
          delete_sub_values = ["DELETE FROM transactions WHERE checkings_id = %s"]

        elif table == "transactions": # this table don't have to comply to any foreign key constraints
          delete_main_value = self.deletion_query(connection, cursor, table, id_column, id_content )

        if table == "customer_information" or table == "checkings_account":
          for query in delete_sub_values: # NOTE: executing the deletion query for the child tables
            cursor.execute(query, (id_content,))
        
        cursor.execute(delete_main_value, (id_content,)) # NOTE: deletion for the main value in the parent table
        connection.commit()
        self.display_rows_affected(cursor, id_column, id_content)
        self.add_transaction_log(connection, employee_id, "Delete User", table, None, f"{id_column.capitalize()}: {id_content}", "Deleted")
        return True
        
      except mysql.connector.Error as error:
        self.display_error(error, "MySQL")
        cursor.execute("ROLLBACK;")
        return False

      finally:
        cursor.execute("SET foreign_key_checks = 1") # enabling the foreign key checks again


  # NOTE: Insertion Queries
  def add_customer_information(self, connection, cursor, employee_id, account_id, f_name, l_name, email, ann_income, id_type, occupation, address, dict_for_customer_info ):
        while True:
            if self.proceed_to_session("addition to transactions", account_id) == "Yes":
                if f_name == "" or l_name== "" or email == "" or ann_income == "" or id_type == "" or occupation == "" or address == "":
                    messagebox.showerror("Invalid Entry Values", f"Customer: Name, Email, Income, ID Type, Occupation, Address are the only allowed info for Customer ID: {account_id}")
                    break
                else:
                    query = "INSERT INTO customer_information(first_name, last_name, email, address, id_type, occupation, annual_gross_income) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    values = (f_name, l_name, email, address, id_type, occupation, ann_income)
                    cursor.execute(query, values)
                    connection.commit()
                    messagebox.showinfo("Added Credentials", "Customer Info Added to New Customer")
                    self.add_to_sessionlog(connection, employee_id, "Add User", "Customer Information", list(values), dict_for_customer_info)
                    break
                
            else: break
  
  def add_into_checkings_account(self, connection, cursor, employee_id, account_id, account_status, account_balance, dict_for_checkings_account):
      while True:
          if self.proceed_to_session("addition to transactions", account_id) == "Yes":
              checkings_id = self.generate_checkings_id()
              password = self.generate_checkings_id()
              dict_for_checkings_account["checkings_id"] = checkings_id
              dict_for_checkings_account["account_password"] = password
              
              if account_balance == "" or account_status == "":
                  messagebox.showerror("Invalid Entry Values", f"Account Balance and Status are the only allowed info for Customer ID: {account_id}")
                  break
              
              else:
                  query = "INSERT INTO checkings_account(checkings_id, account_password, balance, account_status, customer_id) VALUES(%s, %s, %s, %s, %s)"
                  values = (checkings_id, password, account_balance , account_status, account_id)
                  cursor.execute(query, values)
                  connection.commit()
                  messagebox.showinfo("Session Status", f"Information Added to Customer {account_id} with Checkings ID: {checkings_id}")
                  # print(f"Balance: {account_balance},  Account Status: {account_status}")
                  # print(checkings_id, " and ", password)
                  
                  values = [checkings_id, password, account_balance, account_status] 
                  self.add_to_sessionlog(connection, employee_id, "Add User", "Checkings Account", values, dict_for_checkings_account)

                  break
              
          else: break
  
  def add_into_transactions(self, connection, cursor, employee_id, account_id, transac_id, transac_type, receiving_acc, transac_date, amount, dict_for_transactions):
                    
        if self.check_account_existence(cursor, "checkings_account", "checkings_id", receiving_acc) or receiving_acc == "" or receiving_acc == "None":
            while True:
                if self.proceed_to_session("addition to transactions", account_id) == "Yes":
                    
                    if transac_type == "" or receiving_acc == "" or transac_date == "" or amount == "":
                        messagebox.showerror("Invalid Entry Values", f"Transaction: Type, Receiving Account, Date and Amount are the only allowed info for Checkings ID: {account_id}")
                        break
                    else:
                        query = "INSERT INTO transactions (transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount) VALUES(%s, %s, %s, %s, %s, %s)"
                        values = (transac_id, account_id, transac_type, receiving_acc, transac_date, amount)
                        cursor.execute(query, values)
                        connection.commit()
                        messagebox.showinfo("Session Status", f"Transaction Added for Checkings ID: {account_id} with Transactions ID: {transac_id} ")
                        print(f"Transaction ID: {transac_id}, Checkings ID: {account_id}, Transaction Type: {transac_type}, Receiving Account: {receiving_acc}, Date: {transac_date}, Amount: {amount}")
                        values = list(values)
                        self.add_to_sessionlog(connection, employee_id, "Add User", "Transactions", values, dict_for_transactions)
                        break
                    
                else: break
                
        else: messagebox.showerror("Session Error", f"Receiving account {receiving_acc} not found.")
    
  

  

  def adminMain(self):
    connection = self.connect_database()
    
    while True:
      if self.check_database_connection():
          return connection
      else:
        messagebox.showerror("Error", "Connection could not be established.")
          
          
       

class Customer(User): # NOTE: inherits from USER 
  def __init__(self):
    super().__init__(host="localhost",
                     username="root",
                     password="",
                     database="treasury_citadel_database")
    
  
  def login(self, connection, dedicated_id, dedicated_password):
    
    cursor = connection.cursor()
    table = "checkings_account"

    while True:
      if self.check_account_existence(cursor, table, "checkings_id", dedicated_id):
        query = f"SELECT * FROM {table} WHERE account_password = %s"
        cursor.execute(query, (dedicated_password,))
        verified_user = cursor.fetchone()

        if verified_user:
          print("\n\tLog In Successful")
          return True
  
        else:
          return False

      else:
        return False
  
  def generate_transaction_id(self):
    alphanumeric = string.ascii_letters + string.digits
    return 'TTC' + ''.join(random.choice(alphanumeric).capitalize() for _ in range(3))

  def customer_session(self, Balance, session_type): # session type(Withdrawal| Deposit| Transfer)
    while True:
      os.system('cls')
      print(f"\n\t------{session_type.capitalize()} Session------")
      try:
        print( f"\n\tYour current balance is: {Balance}\n")
        session_amount = self.get_decimal_input(f"Amount to {session_type}: ") 
      except Exception as e:
        self.display_error(e, "Exception")
        continue
      
      return session_amount

  def view_transaction_status(self, new_balance):
    message_transaction = f"Transaction completed successfully, your new balance is {new_balance}."
    messagebox.showinfo("Session Status", message_transaction)
    print("\n\t___________________________\n"
              f"\n\tTransaction completed successfully, your new balance is {new_balance}.")
    input("\tPress Enter to Return to Customer Home Page...")

  def add_transaction_log(self, connection, checkings_id, transaction_type, receiving_account, amount):
    cursor = connection.cursor()
    try:
      cursor = connection.cursor()
      transaction_date = datetime.now().strftime("%Y-%m-%d") # returns the current date
      transaction_id = self.generate_transaction_id()
      
      query = "INSERT INTO transactions (transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount) VALUES(%s, %s, %s, %s, %s, %s)"
      values = (transaction_id,checkings_id, transaction_type, receiving_account, transaction_date, amount)
      cursor.execute(query, values)
      connection.commit()
      return "Bitch"

    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")

  def view_transaction_log(self, connection, checking_account_id):
    try:
      os.system('cls')
      cursor = connection.cursor()
      fetch_query = "SELECT transactions_id, checkings_id, transaction_type, receiving_account, transaction_date, amount FROM transactions WHERE checkings_id = %s"
      cursor.execute(fetch_query, (checking_account_id,))
      print(f"\n\t-------Account {checking_account_id} Transaction Log History-------")
      self.format_table(cursor)
    
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      cursor.execute("ROLLBACK;")
        
    input("Press Enter to exit...")


  def customerMain(self):
    os.system('cls')
    connection = self.connect_database()

    while True:
      if self.check_database_connection():
        return connection
      else:
        messagebox.showerror("Error", "Connection could not established.")
  

  def customer_withdraw(self, connection, checking_account_id, withdrawal_amount):
    cursor = connection.cursor()
    table = "checkings_account"
    column = "balance"

    current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", checking_account_id) 
    
    while True:
      if withdrawal_amount <= current_balance:
        try:

          message = f"The amount you want to withdraw is {withdrawal_amount}..."
          messagebox.showinfo("Withdrawal", message)
          new_balance = current_balance - withdrawal_amount

          # NOTE: updates the balance in the checkings_account table
          self.updating_query(connection, cursor, table, column, "checkings_id", checking_account_id, new_balance)
          transac_log_status = self.add_transaction_log(connection,checking_account_id, "Withdraw", "None", withdrawal_amount)
          print(transac_log_status)
          return True

        except mysql.connector.Error as error:
          message_error= f"MySQL: {error}"
          messagebox.showerror("Error", message_error)
          break

      elif withdrawal_amount > current_balance:
        messagebox.showerror("Withdrawal Error", "The amount you want to withdraw exceeds your current balance.")
        return False
      
      break


  def customer_deposit(self, connection, checking_account_id, deposit_amount):
    cursor = connection.cursor()
    table = "checkings_account"
    column = "balance"

    while True:
      current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", checking_account_id)
      
      try:
        messagebox.showinfo("Deposit", f"The amount you want to deposit is {deposit_amount}..." )
        new_balance = current_balance + deposit_amount
        
        self.updating_query(connection, cursor, table, column, "checkings_id", checking_account_id, new_balance)
        transac_log_status = self.add_transaction_log(connection, checking_account_id, "Deposit", "None", deposit_amount )
        print(transac_log_status)
        
        return True
      
      except mysql.connector.Error as err:
        messagebox.showerror("MySQL Error", err)
    
    

  def customer_transfer(self, connection, my_checking_account_id, transfer_amount, recepient_checkAccID):
    cursor = connection.cursor()
    table = "checkings_account"
    column = "balance"
    
    try:
      my_current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", my_checking_account_id)
      recepient_current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", recepient_checkAccID)
      while True:
        if my_current_balance >= transfer_amount:
            
          account_exists = self.check_account_existence(cursor, table, "checkings_id", recepient_checkAccID)

          if account_exists and recepient_checkAccID != my_checking_account_id: # NOTE: executing the transfer
            sender_new_balance = my_current_balance - transfer_amount
            
            if self.updating_query(connection, cursor, table, column, "checkings_id", my_checking_account_id, sender_new_balance):
              recepient_new_balance = transfer_amount + recepient_current_balance
              self.updating_query(connection, cursor, table, column, "checkings_id", recepient_checkAccID, recepient_new_balance)
              
            transac_log_status = self.add_transaction_log(connection, my_checking_account_id, "Transfer", recepient_checkAccID, transfer_amount)
            print(transac_log_status)
            return True
            
          if recepient_checkAccID == my_checking_account_id or account_exists == None :
            messagebox.showerror("Session Status", "Invalid Transferring Account")
            break
        
          
            
        elif my_current_balance < transfer_amount:
          messagebox.showerror("Invalid Session", "You do not have the necessary funds to transfer that amount.")
          break
      
        break
        
    except mysql.connector.Error as error:
      cursor.execute("ROLLBACK;")
      messagebox.showerror("MySQL Error: ", error)
              
      
  def check_balance(self, connection, checking_account_id):
      os.system('cls')
      cursor = connection.cursor()
      try:
          cursor.execute("SELECT balance FROM checkings_account WHERE checkings_id = %s", (checking_account_id,))
          Balance = cursor.fetchone()
          return float(Balance[0])
        
      except mysql.connector.Error as error:
          messagebox.showerror("Error Fetching Balance", error)
          cursor.execute("ROLLBACK;")
     


  def fetch_customer_name(self, cursor, checking_account_id):
    try:
      cursor.execute("SELECT first_name FROM fetch_username WHERE checkings_id = %s", (checking_account_id,))
      result = cursor.fetchone()
      return result
    except mysql.connector.Error as err:
      messagebox.showerror("Error Fetching Username", err)

  def fetch_total_amount_by_session(self, cursor, checkings_id, session_type):
    try:
      query = """
            SELECT SUM(amount) FROM transactions 
            WHERE checkings_id = %s AND transaction_type = %s """
      cursor.execute(query, (checkings_id, session_type,))
      Result = cursor.fetchone()
      return Result[0]
    
    except mysql.connector.Error as error:
      messagebox.showerror("MySQL: ", error)




class Banking_System(): # NOTE: main
  def __init__(self):
    self.employee = Employee(self)  # Employee instance with a reference to the Banking_System instance it belongs to
    self.customer = Customer(self)
    self.connection = None 
    

  # MAIN program entrance
  def banking_main(self):
    while True:
      os.system('cls')
      print("\n\t----------Treasury Citadel Banking System----------\n\n"
            "\t\t[1]: Admin / Employee\n\n"
            "\t\t[2]: User / Customer\n")
      
      action = int(input("\n\t\tLog In as: "))

      if action == 1:
        # implement admin's log in system
        # self.user = self.employee  # Do not create an instance of User directly
        # self.connection = self.employee.connect_database()  # Use connect_database directly or in your adminMain method
        self.employee.adminMain()
        break
      
      elif action == 2:
        # implement customer's log in system
        self.customer.customerMain()
        break

      else:
        os.system('cls')
        print("\n\t-------Invalid Credential....")
        input("\n\n\tPress enter to return to the main menu......")
        continue
    
  
# MAIN program entrance
if __name__ == "__main__":
  banking_system = Banking_System()
  banking_system.banking_main()