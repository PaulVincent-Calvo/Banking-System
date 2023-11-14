import mysql.connector
import os
from decimal import Decimal, DecimalException # for Decimal datatype input in mysql
from tabulate import tabulate # for precise tables & columns formatting 
from datetime import datetime


# NOTE: feel free suggest any improvement in this code



class User: # NOTE: all functions to be used in child classes (Employee, Customer) are included in here
  
  def __init__(self):
    self.connection = None
    
  def display_error(self, error_message, error_type = None):
    if error_type:
      print(f"\n\t{error_type} Error: ..... {error_message} .....")
      
    else:
      print(f"\n\tError:...... {error_message}'''''")
    
    if not self.continue_session():
      return
    
  def connect_database(self):
    try:                     # NOTE: all users who will access the database must be connected to the same network
      host = "192.168.18.48"  # Set to this according to your internet's ipv4 address (to check the ip address, go to the terminal and type: ipconfig)
      username = "miguel"
      password = "password"
      database = "bankingoop"

      self.connection = mysql.connector.connect(
          host= host,
          user= username,
          password= password,
          database= database)
    
      print("Database Initialization Successful...")
    
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      
    return self.connection

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
    
  def display_rows_affected(self, cursor, ID, IDContent):
    print(f"\n\t{cursor.rowcount} session initiated| {ID}: {IDContent}")

  def confirm_action(self):
    confirm = int(input("\n\tConfirm Selected Action | 1 | 0 |: "))
    return True if confirm == 1 else False
  
  # NOTE: Inputs
  def input_date(self, description):
    try:
      year = input(f"\n\t---- {description} Year (YYYY): ")
      month = input(f"\n\t---- {description} Month (MM): ")
      day = input(f"\n\t---- {description} Day(DD): ")
    
      date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"  # ensure two-digit month and day
      transaction_date = datetime.strptime(date_str, "%Y-%m-%d").date() # converting into date format
      return transaction_date

    except ValueError as error:
      return error
    
  def display_current_value(self, column, current_value):
    print(f"\n\tCurrent {column.capitalize()}: {current_value}")

  def get_new_value(self, attribute, datatype):
    if datatype == str:
      return input(f"\n\tNew {attribute}: ")
    
    elif datatype == Decimal:
      return self.get_decimal_input(f"\tNew {attribute}: ")

    elif datatype == datetime:
      return self.input_date("Transaction")
      
  def get_decimal_input(self, prompt):
    while True:
      try:
        return Decimal(input(f"\n\t\t{prompt}: "))
      except DecimalException as de:
        self.display_error(de, "Decimal ValueError")

    
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
  
  def check_account_existence(self, cursor, table, id_column, id_content):    
    try:
      query = f"SELECT * FROM {table} WHERE {id_column} = %s" # searches the customerID
      cursor.execute(query, (id_content,))
      account_exists = cursor.fetchone() # checks the account's existence
      return account_exists
    
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
    
  def fetch_single_value(self, connection, cursor, table, column, id_column, id_content): # function for DISPLAYING single values
    try:
      cursor = connection.cursor()
      query = f"SELECT {column} FROM {table} WHERE {id_column} = %s"
      value = id_content
      cursor.execute(query,(value,))
      Result = cursor.fetchone()
      return Result[0] #  returns the first column value of the first row in the result se
    
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")

  # NOTE: Updating Query
  def updating_query(self, connection, cursor, table, column, ID, IDcontent, value): # function for FLEXIBLE updation in both admin and customer features
    try:
      main_query = f"UPDATE {table} SET {column} = %s WHERE {ID} = %s"
      cursor.execute(main_query, (value, IDcontent)) 
      connection.commit() # a must
      self.display_rows_affected(cursor, ID, IDcontent)
      
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")

    
    
    
class Employee(User): # NOTE: inherits from USER 
  
  def __init__(self, banking_system): #  accept an instance of BankingSystem and store it as an attribute.
    super().__init__()
    self.banking_system = banking_system # to be used in the adminMain() 
        
  def admin_display_options(self, description):
    common_options = (f"\n\t_______{description} USERS_______\n\n"
                      "\t[1] Customer Information\n"
                      "\t[2] Checkings Accounts\n"
                      "\t[3] Bank Assets\n"
                      "\t[4] Transactions\n")

    additional_options = "\t[5] All Records\n \t[6] Return Home\n" if description == "VIEW" else "\t[5] Return Home\n"

    description_display = common_options + additional_options
    print(description_display)

  # NOTE: Deletion Queries
  def deletion_query(self, connection, cursor, table, column, ID):
    try:
      cursor = connection.cursor()
      query = f"DELETE FROM {table} WHERE {column} = %s"
      cursor.execute(query, (ID,))
      connection.commit()

    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")
      
    
  # NOTE: Foreign key constraints maintain referential integrity, ensuring that a user can only be deleted
          # IF AND ONLY IF its references in related tables have been deleted

  def delete_user_by_ID(self, connection, cursor, table, id_column, id_content):
    while True:
      account_exists = self.check_account_existence(cursor, table, id_column, id_content)
      confirm_deletion = self.confirm_action()

      if account_exists and confirm_deletion:
        try:
          cursor.execute("SET foreign_key_checks = 0") # disabling foreign key checks temporarily to avoid violating foreign key constraints
          
          if table == "customer_information":
            delete_main_value = self.deletion_query(connection, cursor, table, id_column, id_content )# NOTE: query for deleting the PARENT table's VALUE
            delete_sub_values = [ #NOTE: putting the deletion queries for CHILD tables into a list iterable
                "DELETE FROM transactions WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s)",
                "DELETE FROM bank_asset WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s)",
                "DELETE FROM checkings_account WHERE customer_id = %s"]
            
          elif table == "checkings_account":
            delete_main_value = self.deletion_query(connection, cursor, table, id_column, id_content )
            delete_sub_values = [
                        "DELETE FROM transactions WHERE checkings_id = %s",
                        "DELETE FROM bank_asset WHERE checkings_id = %s"]

          elif table == "bank_asset" or table == "transactions": # these tables don't have to comply to any foreign key constraints
            delete_main_value = self.deletion_query(connection, cursor, table, id_column, id_content )

          if table == "customer_information" or table == "checkings_account":
            for query in delete_sub_values: # NOTE: executing the deletion query for the child tables
              cursor.execute(query, (id_content,))
          
          cursor.execute(delete_main_value, (id_content,)) # NOTE: deletion for the main value in the parent table
          connection.commit()
          self.display_rows_affected(cursor, id_column, id_content)
          
        except mysql.connector.Error as error:
          self.display_error(error, "MySQL")

        finally:
          cursor.execute("SET foreign_key_checks = 1") # enabling the foreign key checks again
        
      elif not confirm_deletion:
        return

      else:
        print(f"\n\tAccount {id_content} is non-existent...")

      if not self.continue_session():
        self.adminMain()


  # NOTE: Insertion/Adding Queries
  def add_customer_information(self, connection, cursor):
    os.system('cls')
    print("\n\t---Add New Customer Information---\n")
    while True:
      try:
        cust_fname = input("\t\tFirst Name: ")
        cust_lname = input("\t\tLast Name: ")
        cust_passwword = input("\t\tPassword: ")
        cust_email = input("\t\tEmail: ")
        cust_address = input("\t\tAddress: ")
        cust_idType = input("\t\tID Type: ")
        cust_occupation = input("\t\tOccupation: ")
        cust_annGrossIncome = self.get_decimal_input("Annual Gross Income")

        query = "INSERT INTO customer_information (customer_password, first_name, last_name, email, address, id_type, occupation, annual_gross_income) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
        values = (cust_passwword, cust_fname, cust_lname, cust_email, cust_address, cust_idType, cust_occupation, cust_annGrossIncome)
        
        if self.confirm_action():
          cursor.execute(query, values)
          connection.commit()
          self.display_rows_affected(cursor, "customer_id", cursor.lastrowid)
          break
          
        else: return

      except ValueError as error:
        self.display_error(error, "MySQL")

  # NOTE: generic function for adding records(to be used in the checkings_account, bank_asset, transactions TABLES)
  def add_record(self, connection, cursor, referenced_table, insertion_table, prompt_message, column_names):
    os.system('cls')
    print(f"\n\t---{prompt_message}---\n")
    self.select_all_rows(cursor, referenced_table) 
    
    while True:
      try:
        id_content = int(input(f"\n\t{column_names[0]}: ")) # accesses the first value in the passed list(it's always the ID; checkings, asset, transaction)
        account_exists = self.check_account_existence(cursor, referenced_table, column_names[0], id_content)

        if account_exists:
          if len(column_names) == 2: # for either checkings_account or bank_asset tables
            balance = self.handle_decimal_value_exception("Customer Checking Account", id_content, "Balance")
            values = (id_content, balance)

          elif len(column_names) == 4: # for transactions table
            os.system('cls')
            transaction_date = self.input_date("Transaction")
            amount = self.handle_decimal_value_exception("Checking Account", id_content, "Transaction Amount")
            transaction_type = input("\n\tTransaction Type: ")
            values = (id_content, transaction_date, amount, transaction_type)
          
          if self.confirm_action():
            # NOTE: joining the values in the column_names then separating them using string formatting
            query = f"INSERT INTO {insertion_table} ({', '.join(column_names)}) VALUES({', '.join(['%s'] * len(values))})"
            cursor.execute(query, values)
            connection.commit()
            self.display_rows_affected(cursor, column_names[0], id_content)
            break
          
          else: return
          
        else:
          print(f"Account {id_content} is non-existent...")
        
      except mysql.connector.Error as error:
        self.display_error(error, "MySQL")
    
  def add_checkings_account(self, connection, cursor):
    referenced_table = "customer_information"
    insertion_table = "checkings_account"
    self.add_record(connection, cursor, referenced_table, insertion_table, "Add New Checkings Account", ["customer_id", "balance"]) # passing the column names for which values will be added in a list

  def add_bank_asset(self, connection, cursor):
    referenced_table = "checkings_account"
    insertion_table = "bank_asset"
    self.add_record(connection, cursor, referenced_table, insertion_table, "Add New Bank Asset Information", ["checkings_id", "checkings_balance"])

  def add_transactions(self, connection, cursor):
    referenced_table = "checkings_account"
    insertion_table = "transactions"
    self.add_record(connection, cursor, referenced_table, insertion_table, "Add New Transaction Information", ["checkings_id", "transaction_date", "amount", "transaction_type"])


  # NOTE: Editing Queries (generic function for editing the user)
  def edit_record(self, connection, cursor, column_description, table, id_column, id_content, display_columns_options):
    while True:
      print(f"\n---{column_description}---")
      account_exists = self.check_account_existence(cursor, table, id_column, id_content)

      if account_exists:
        os.system('cls')
        print(f"\n\t------Edit Information for Customer {id_content}------\n", display_columns_options)
        attribute = int(input("Choose Account Attribute: "))
        
        if table == "customer_information":
          if attribute == 1:
            print("Customer ID is not editable.") # assuming customer_id is not something the admin should update
            continue
          else:
            column = "customer_password" if attribute == 2 else "first_name" if attribute == 3 else "last_name" if attribute == 4 else "email" if attribute == 5 else "address" if attribute == 6 else "id_type" if attribute == 7 else "occupation" if attribute == 8 else "annual_gross_income" if attribute == 9 else None

        elif table == "checkings_account":
          column = "balance"

        elif table == "bank_asset":
          column = "checkings_balance"
        
        elif table == "transactions":
          if attribute == 1:
            column = "transaction_date"
          else:
            column = "amount" if attribute == 2 else "transaction_type" if attribute == 3 else None


        if column is not None:
          os.system('cls')
          print(f"\n\t------Edit {column.capitalize()}------")
          current_value = self.fetch_single_value(connection, cursor, table, column, id_column, id_content)
          self.display_current_value(column, current_value)

          try: # NOTE: Inputs(each depending on the column's datatype)
            if table == "customer_information":
              if column == "annual_gross_income":
                new_value = self.get_new_value(column, Decimal)
              else:
                new_value = self.get_new_value(column, str)
            
            elif table == "checkings_account" or table == "bank_asset":
              new_value = self.get_new_value(column, Decimal)

            elif table == "transactions":
              if column == "transaction_date":
                new_value = self.get_new_value(column, datetime)
              
              elif column == "amount":
                new_value = self.get_new_value(column, Decimal)
              
              elif column == "transaction_type":
                new_value = self.get_new_value(column, str)
            
            if self.confirm_action():
              self.updating_query(connection, cursor, table, column, id_column, id_content, new_value)
              
            else: return
            
            if not self.continue_session():
              self.adminMain()
            
          except ValueError as error:
            self.display_error(error)
          
      else:
        print(f"\n\t-----Account {id_content} non-existent....\n")

  def adminMain(self):
    connection = self.connect_database()
    while True:
      os.system('cls')
      try:
        print("\n_______ADMIN AUTHORIZED_______\n"
        "\t[1] View Users\n"
        "\t[2] Edit Users\n"
        "\t[3] Delete Users\n"
        "\t[4] Add Users\n"
        "\t[5] Logout")
        
        action = int(input("\n\tAction: "))
        
        if action == 1:
          self.admin_view_user(connection)
          break

        elif action == 2:
          self.admin_edit_user(connection)
          break

        elif action == 3:
          self.admin_delete_user(connection)
          break

        elif action == 4:
          self.admin_add_user(connection)
          break
        
        elif action == 5:
          os.system('cls')
          banking_system.banking_main()
        
        else:
          print("Invalid Input")
          
      except ValueError as error:
        self.display_error(error, "ValueError")

  def admin_view_user(self, connection):
    os.system('cls')
    cursor = connection.cursor()
    
    while True:
      os.system('cls')
      self.admin_display_options("VIEW")
        
      try: 
        action = int(input("\n\tAction: "))
        
        if action == 1:  # [1] Customer Information: table name as the parameter
          self.select_all_rows(cursor, "customer_information") 
            
        elif action == 2: # [2] Checkings Accounts
          self.select_all_rows(cursor, "checkings_account")

        elif action == 3: # [3] Bank Assets
          self.select_all_rows(cursor, "bank_asset")
          
        elif action == 4: # [4] Transactions
          self.select_all_rows(cursor, "transactions")
        
        elif action == 5: # [5] All Records NOTE: the "all_records" is a VIEW which is used to JOIN all information of the tables
          self.select_all_rows(cursor, "all_records")

        elif action == 6:
          self.adminMain()
          
        else:
          print("Invalid Input...")
        
        if not self.continue_session(): # returns to main menu if false
          self.adminMain()
          
      except ValueError as error:
        self.display_error(error, "ValueError")
  
  def admin_edit_user(self, connection):
    os.system('cls')
    cursor = self.connection.cursor()
    
    while True:
      os.system('cls')
      try:
        self.admin_display_options("EDIT")

        action = int(input("\n\tEdit From: "))
        
        if action == 1: # for Customer Information
          table = "customer_information"
          self.select_all_rows(cursor, table) # displays the exiting customer information records
          customer_id_content = int(input("\n\n\tCustomer ID: "))
          column_options = "\n\t [1] Customer ID\n\t [2] Customer Password\n\t [3] First Name\n\t [4] Last Name\n\t [5] Email\n\t [6] Address\n\t [7] ID Type\n\t [8] Occupation\n\t [9] Annual Gross Income\n\t"
          self.edit_record(connection, cursor, "Customer Information", table, "customer_id", customer_id_content, column_options)
    
        elif action == 2: # [2] Checkings Account
          table = "checkings_account"
          self.select_all_rows(cursor, table)
          checkings_id_content = int(input("\n\n\tCheckings ID: "))
          column_options = "\n\t[1] Balance\n"
          self.edit_record(connection, cursor, "Checkings Account Information", table, "checkings_id", checkings_id_content, column_options)
            
        elif action == 3: # [3] Bank Asset
          table = "bank_asset"
          self.select_all_rows(cursor, table)
          asset_id_content = int(input("Bank Asset ID: "))
          column_options = "\n\t[1] Checkings Balance\n"
          self.edit_record(connection, cursor, "Bank Asset Information", table, "asset_id", asset_id_content, column_options)
          
        elif action == 4: # [4] Transactions
          table = "transactions"
          self.select_all_rows(cursor, table)
          transaction_id_content = int(input("\n\tTransaction ID: "))
          column_options = "\n\t[1] Transaction Date\n\t[2] Amount\n\t[3] Transaction Type\n"
          self.edit_record(connection, cursor, "Transaction Information", table, "transactions_id", transaction_id_content, column_options)
          
        elif action == 5: # [5] Return Home
          self.adminMain()

        if not self.continue_session(): # looping
          self.adminMain()
        
      except ValueError as error:
        self.display_error(error, "ValueError")
          
  def admin_delete_user(self, connection):
    os.system('cls')
    cursor = self.connection.cursor()
    while True:
      os.system('cls')
      try:
        self.admin_display_options("DELETE")
        
        action = int(input("\n\tDelete From: "))
        
        if action == 1: # [1] Customer Information
          table = "customer_information"
          self.select_all_rows(cursor, table)
          customer_id_content = int(input("\n\tCustomer ID: "))
          self.delete_user_by_ID(connection, cursor, table, "customer_id", customer_id_content) # invoking the function for deletion given by the ff. parameters
            
            
        elif action == 2: # [2] Checkings Accounts
          table = "checkings_account"
          self.select_all_rows(cursor, table)
          checkings_id_content = int(input("\n\tCheckings Account ID: "))
          self.delete_user_by_ID(connection, cursor, table, "checkings_id", checkings_id_content)
          
          
        elif action == 3: # [3] Bank Assets
          table = "bank_asset"
          self.select_all_rows(cursor, table)
          asset_id_content = int(input("\n\tBank Asset ID: "))
          self.delete_user_by_ID(connection, cursor, table, "asset_id", asset_id_content)


        elif action == 4: # [4] Transactions
          table = "transactions"
          self.select_all_rows(cursor, table)
          transactions_id_content = int(input("\n\tTransaction ID: "))
          self.delete_user_by_ID(connection, cursor, table, "transactions_id", transactions_id_content)
          
        elif action == 5:
          self.adminMain()

      except ValueError as error:
        print(f"Invalid Input....{error}")


  def admin_add_user(self, connection):
    os.system('cls')
    try:
      cursor = connection.cursor()
      
      while True:
        os.system('cls')
        self.admin_display_options("ADD")

        action = int(input("\n\tAdd User To: "))
        
        if action == 1:
          self.add_customer_information(connection, cursor)

        elif action == 2:
          self.add_checkings_account(connection, cursor)

        elif action == 3:
          self.add_bank_asset(connection, cursor)

        elif action == 4:
          self.add_transactions(connection, cursor)

        elif action == 5:
          self.adminMain()

        else:
          continue
        
        if not self.continue_session():
          self.adminMain()
    
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")




class Customer(User): # NOTE: inherits from USER 
  def __init__(self, banking_system):
    super().__init__()
    self.banking_system = banking_system

    
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
    print("\n\t___________________________\n"
              f"\n\tTransaction completed successfully, your new balance is {new_balance}.")
    input("\tPress Enter to Return to Customer Home Page...")

  def add_transaction_history(self, connection, cursor, checkings_id, amount, transaction_type):
    try:
      cursor = connection.cursor()
      transaction_date = datetime.now().strftime("%Y-%m-%d") # returns the current date
      
      query = "INSERT INTO transactions(checkings_id, transaction_date, amount, transaction_type) VALUES(%s, %s, %s, %s)"
      values = (checkings_id, transaction_date, amount, transaction_type)
      cursor.execute(query, values)
      connection.commit()

    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")

  def display_transaction_history(self, connection, checking_account_id):
    try:
      os.system('cls')
      cursor = connection.cursor()
      fetch_query = "SELECT transactions_id, transaction_date, amount, transaction_type FROM transactions WHERE checkings_id = %s"
      cursor.execute(fetch_query, (checking_account_id,))
      print(f"\n\t-------Account {checking_account_id} Transaction History-------")
      self.format_table(cursor)
    
    except mysql.connector.Error as error:
        self.display_error(error, "MySQL")
        
    input("Press Enter to exit...")


  def customerMain(self):
    os.system('cls')
    connection = self.connect_database()
    cursor = self.connection.cursor()

    while True:
      try:
        os.system('cls')
        checking_account_id = int(input("\n\tEnter your dedicated Checkings Account ID: "))
        account_exist = self.check_account_existence(cursor, "checkings_account", "checkings_id", checking_account_id)
        
        if account_exist:
          while True:
            try:
              os.system('cls')
              print("\n_______Customer Page_______\n"
              "\t[1] Withdraw Money\n"
              "\t[2] Deposit Amount\n"
              "\t[3] Transfer Money\n"
              "\t[4] Check Balance\n"
              "\t[5] Transaction History\n"
              "\t[6] Logout\n")
              
              action = int(input("\n\tAction: "))
              
              if action == 1:
                self.customer_withdraw(connection, checking_account_id)

              elif action == 2:
                self.customer_deposit(connection, checking_account_id)

              elif action == 3:
                self.customer_transfer(connection, checking_account_id)

              elif action == 4:
                self.customer_check_balance(connection, checking_account_id)
              
              elif action == 5:
                self.display_transaction_history(connection, checking_account_id)
                
              elif action == 6:
                os.system('cls')
                banking_system.banking_main()
              
              else:
                print("Invalid Input...")
                continue
                
            except ValueError as error:
              self.display_error(error, "ValueError")
            
        else:
          os.system('cls')
          print(f"\n\t___________________________\n"
                f"\tInvalid Account Number...")
      
      except mysql.connector.Error as error:
        self.display_error(error, "MySQL")

  

  def customer_withdraw(self, connection, checking_account_id):
    cursor = connection.cursor()
    table = "checkings_account"
    column = "balance"

    while True:
      current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", checking_account_id) 
      withdraw_amount = self.customer_session(current_balance, "withdraw")
      confirm_withdrawal = self.confirm_action()
      
      if withdraw_amount <= current_balance and confirm_withdrawal:
        try:
          os.system('cls')
          print(f"\n\tThe amount you want to withdraw is {withdraw_amount}...\n")
          new_balance = current_balance - withdraw_amount

          # NOTE: updates the balance in the checkings_account table
          self.updating_query(connection, cursor, table, column, "checkings_id", checking_account_id, new_balance)
          self.view_transaction_status(new_balance)  # displays the transaction status
          self.add_transaction_history(connection, cursor, checking_account_id, withdraw_amount, "Withdraw")

        except Exception as e:
          print(f"Transaction Failed: {e}")
          if not self.continue_session():
            return

        break


      elif withdraw_amount > current_balance:
        os.system('cls')
        print(f"\n\t___________________________\n"
              f"\n\tThe amount you want to withdraw exceeds your current balance ({current_balance})")

      elif not confirm_withdrawal:
        return

      if not self.continue_session():
        break


  def customer_deposit(self, connection, checking_account_id):
    cursor = connection.cursor()
    table = "checkings_account"
    column = "balance"

    while True:
      current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", checking_account_id)
      deposit_amount = self.customer_session(current_balance, "deposit")
      
      try:
        os.system('cls')
        print(f"\n\tThe amount you want to deposit is {deposit_amount}...\n")
        new_balance = current_balance + deposit_amount
        
        self.updating_query(connection, cursor, table, column, "checkings_id", checking_account_id, new_balance)
        self.add_transaction_history(connection, cursor, checking_account_id, deposit_amount, "Deposit")
        self.view_transaction_status(new_balance)
      
      except Exception as e:
        print(f"Transaction Failed: {e}")
        if not self.continue_session():
          return

      break
    

  def customer_transfer(self, connection, my_checking_account_id):
    cursor = connection.cursor()
    table = "checkings_account"
    column = "balance"
    
    while True:
      try:
        current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", my_checking_account_id)
        transfer_amount = self.customer_session(current_balance, "transfer")

        if current_balance >= transfer_amount:
          while True: 
            
            try:
              os.system('cls')
              recepient_checkAccID = int(input("\tEnter the Account Number of the account to transfer to: "))
              account_exists = self.check_account_existence(cursor, table, "checkings_id", recepient_checkAccID)

              if account_exists and recepient_checkAccID != my_checking_account_id: # NOTE: executing the transfer
                
                # NOTE: Updating the Sending User Account Balance 
                sender_new_balance = current_balance - transfer_amount
                self.updating_query(connection, cursor, table, column, "checkings_id", my_checking_account_id, sender_new_balance) 
                
                # NOTE: Updating the Receiving User Account Balance
                recepient_current_balance = self.fetch_single_value(connection, cursor, table, column, "checkings_id", recepient_checkAccID)
                recepient_new_balance = transfer_amount + recepient_current_balance
                
                self.updating_query(connection, cursor, table, column, "checkings_id", recepient_checkAccID, recepient_new_balance)
                self.view_transaction_status(sender_new_balance)
                self.add_transaction_history(connection, cursor, my_checking_account_id, transfer_amount, "Transfer")
                return # to the Main Menu
                
                
              if recepient_checkAccID == my_checking_account_id: # NOTE: Invalid Session
                print(f"\n\t___________________________\n"f"\n\tInvalid Account Number..."
                        f"\n\tYou Entered your own Account Number which is invalid...")
                if not self.continue_session():
                  return
                
            except mysql.connector.Error as error:
              self.display_error(error, "MySQL")
              if not self.continue_session():
                return
        
        
        elif current_balance < transfer_amount:
          os.system('cls') 
          print(f"\n\t___________________________\n" f"\n\tYou do not have the necessary funds to transfer that amount...")
          if not self.continue_session():
            return

      except ValueError as error:
        self.display_error(error, "ValueError")
        if not self.continue_session():
          return
        

  def customer_check_balance(self, connection, checking_account_id):
    os.system('cls')
    try:
      cursor = connection.cursor()
      Balance = self.fetch_single_value(connection, cursor, "checkings_account", "balance", "checkings_id", checking_account_id) # passing all the credentials as parameters to access the Balance
      print(f"\n\t___________________________\n \tYour Current Balance is {Balance}.")
      input("\tPress Enter to Return to Customer Home Page...")
      
    except mysql.connector.Error as error:
      self.display_error(error, "MySQL")




class Banking_System(): # NOTE: main
  def __init__(self):
    self.user = User()
    self.connection = self.user.connect_database()
    self.employee = Employee(self) # Employee instance with a reference to the Banking_System instance it belongs to
    self.customer = Customer(self)    
    

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
