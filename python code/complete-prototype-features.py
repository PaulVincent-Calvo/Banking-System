import mysql.connector
import os
from decimal import Decimal, DecimalException # for Decimal datatype input in mysql
from tabulate import tabulate # for precise (& effortless lol) tables & columns formatting 
from datetime import datetime


# NOTE: General Functions

def display_error(error_message, error_type=None): # for exeception errors
  if error_type:
    print(f"\n\t{error_type} Error: ..... {error_message} .....")
  else:
    print(f"\n\tError:...... {error_message}'''''")

  if not continue_session():
    return

def connect_database():
  connection = None
  try:                     # NOTE: all users who will access the database must be connected to the same network
    host = " 192.168.1.6"  # Set to this according to your internet's ipv4 address (to check the ip address, go to the terminal and type: ipconfig)
    username = "miguel"
    password = "password"
    database = "bankingoop"

    connection = mysql.connector.connect(
        host= host,
        user= username,
        password= password,
        database= database
    )
    
    print("Database Initialization Successful...")
    
  except mysql.connector.Error as error:
    display_error(error, "MySQL")
    
  return connection

def format_table(cursor): # using the tabulate library
  try:
    rows = cursor.fetchall()
    if rows:
      # extract column names from the cursor.description
      headers = [desc[0] for desc in cursor.description]
      # use the tabulate function to format the results as a table
      table = tabulate(rows, headers, tablefmt="pretty")
      print(table)
    else:
        print("No records found.")
        
  except mysql.connector.Error as error:
    display_error(error, "MySQL")
  
def continue_session(): # dedicated for looping purposes
  continue_session = int(input("\n\nContinue Session (1 | 0): "))
  if continue_session == 1:
    return 1
  else:
    return 0

def display_rows_affected(cursor, ID, IDContent):
  print(f"\n\t{cursor.rowcount} session initiated| {ID}: {IDContent}")



# NOTE: Inputs
def input_date(description):
  try:
    year = input(f"\n\t---- {description} Year (YYYY): ")
    month = input(f"\n\t---- {description} Month (MM): ")
    day = input(f"\n\t---- {description} Day(DD): ")
  
    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"  # ensure two-digit month and day
    transaction_date = datetime.strptime(date_str, "%Y-%m-%d").date() # converting into date format
    return transaction_date

  except ValueError as error:
    # display_error(error, "ValueError")
    return error
   
def display_current_value(column, current_value):
  print(f"\n\t---Current {column.capitalize()}: {current_value}")

def get_new_value(attribute):
  return input(f"\t------New {attribute}: ")

def get_decimal_input(prompt):
  while True:
    try:
      return Decimal(input(f"\n\t\t{prompt}: "))
    except DecimalException as de:
      display_error(de, "Decimal ValueError")
 
  
  
# NOTE: Input Handling
def handle_decimal_value_exception(description, id_content): # resuable exception handling for decimal types inputs
  try:
    amount = get_decimal_input(f"\n\t---- {description} {id_content} Amount: ")
    return amount
  except DecimalException as de:
    display_error(de, "Decimal ValueError")
    return 0

  

# NOTE: Searching/Selecting Queries
def select_all_rows(cursor, table):
  try:
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    format_table(cursor) # prints the formatted tables
    
  except mysql.connector.Error as error:
    display_error(error, "MySQL")
 
def check_account_existence(cursor, table, id_column, id_content): 
  try:
    query = f"SELECT * FROM {table} WHERE {id_column} = %s" # searches the customerID
    cursor.execute(query, (id_content,))
    account_exists = cursor.fetchone() # checks the account's existence
    return account_exists
  
  except mysql.connector.Error as error:
    display_error(error, "MySQL")
  
def fetch_single_value(connection, cursor, table, column, id_column, id_content): # function for DISPLAYING single values
  try:
    cursor = connection.cursor()
    query = f"SELECT {column} FROM {table} WHERE {id_column} = %s"
    value = id_content
    cursor.execute(query,(value,))
    Result = cursor.fetchone()
    return Result[0]
  
  except mysql.connector.Error as error:
    display_error(error, "MySQL")


  
# NOTE: Updating Queries
def updating_query(connection, cursor, table, column, ID, IDcontent, value): # function for FLEXIBLE updating the query in the admin_editUser function
  try:
    main_query = f"UPDATE {table} SET {column} = %s WHERE {ID} = %s"
    cursor.execute(main_query, (value, IDcontent)) 
    connection.commit() # a must
    display_rows_affected(cursor, ID, IDcontent)
    
  except mysql.connector.Error as error:
    display_error(error, "MySQL")


# NOTE: Deletion Queries
def deletion_query(connection, cursor, table, column, ID):
  try:
    cursor = connection.cursor()
    query = f"DELETE FROM {table} WHERE {column} = %s"
    cursor.execute(query, (ID,))
    connection.commit()

  except mysql.connector.Error as error:
    display_error(error, "MySQL")
    
  
 # NOTE: Foreign key constraints maintain referential integrity, ensuring that a user can only be deleted
        # IF AND ONLY IF its references in related tables have been deleted

def delete_user_by_ID(connection, cursor, table, id_column, id_content):
  account_exists = check_account_existence(cursor, table, id_column, id_content)
  confirm_deletion = int(input("\n\t-CONFIRM Deletion? |1|: "))

  if account_exists and confirm_deletion == 1:
    try:
      cursor.execute("SET foreign_key_checks = 0") # disabling foreign key checks temporarily to avoid violating foreign key constraints
      
      if table == "customer_information":
        delete_main_value = deletion_query(connection, cursor, table, id_column, id_content )# NOTE: query for deleting the PARENT table's VALUE
        delete_sub_values = [ #NOTE: putting the deletion queries for CHILD tables into a list iterable
            "DELETE FROM transactions WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s)",
            "DELETE FROM bank_asset WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s)",
            "DELETE FROM checkings_account WHERE customer_id = %s"]
        
      elif table == "checkings_account":
        delete_main_value = deletion_query(connection, cursor, table, id_column, id_content )
        delete_sub_values = [
                    "DELETE FROM transactions WHERE checkings_id = %s",
                    "DELETE FROM bank_asset WHERE checkings_id = %s"]

      elif table == "bank_asset" or table == "transactions": # these tables don't have to comply to any foreign key constraints
        delete_main_value = deletion_query(connection, cursor, table, id_column, id_content )

      if table == "customer_information" or table == "checkings_account":
        for query in delete_sub_values: # NOTE: executing the deletion query for the child tables
          cursor.execute(query, (id_content,))
         
      cursor.execute(delete_main_value, (id_content,)) # NOTE: deletion for the main value in the parent table
      connection.commit()
      display_rows_affected(cursor, id_column, id_content)
      
    
    except mysql.connector.Error as error:
      display_error(error, "MySQL")


    finally:
      cursor.execute("SET foreign_key_checks = 1") # enabling the foreign key checks again
    
  
  else:
     print(f"\n\tAccount {id_content} is non-existent...")
  
  if not continue_session():
    adminMain()



# NOTE: Insertion/Adding Queries
def add_customer_information(connection, cursor):
  
  os.system('cls')
  print("\n\t---Add New Customer Information---\n")

  try:
    cust_fname = input("\t\tFirst Name: ")
    cust_lname = input("\t\tLast Name: ")
    cust_passwword = input("\t\tPassword: ")
    cust_email = input("\t\tEmail: ")
    cust_address = input("\t\tAddress: ")
    cust_idType = input("\t\tID Type: ")
    cust_occupation = input("\t\tOccupation: ")
    cust_annGrossIncome = get_decimal_input("\tAnnual Gross Income: ")

    query = "INSERT INTO customer_information (customer_password, first_name, last_name, email, address, id_type, occupation, annual_gross_income) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
    values = (cust_passwword, cust_fname, cust_lname, cust_email, cust_address, cust_idType, cust_occupation, cust_annGrossIncome)

    cursor.execute(query, values)
    connection.commit()
    display_rows_affected(cursor, "customer_id", cursor.lastrowid)

  except ValueError as error:
    display_error(error, "MySQL")

def add_checkings_account(connection, cursor):
  referenced_table = "customer_information"
  os.system('cls')
  print("\n\t---Add New Checkings Account Info---\n")
  select_all_rows(cursor, referenced_table)

  try:
    customer_id_content = int(input("\t\tCustomer ID: "))
    account_exists = check_account_existence(cursor, referenced_table, "customer_id", customer_id_content)

    if account_exists:
      balance = handle_decimal_value_exception("Customer Account", customer_id_content)
      query = "INSERT INTO checkings_account (customer_id, balance) VALUES(%s, %s)"
      values = (customer_id_content, balance)

      cursor.execute(query, values)
      connection.commit()
      display_rows_affected(cursor, "checkings_id", cursor.lastrowid)

    else:
      print(f"Customer {customer_id_content} is non-existent...")

  except mysql.connector.Error as error:
      display_error(error, "MySQL")

def add_bank_asset(connection, cursor):
  referenced_table = "checkings_account"
  os.system('cls')
  print("\n\t---Add New Bank Asset Info---\n")
  select_all_rows(cursor, referenced_table)

  try:
    checkingsIDcontent = int(input("\t\tCheckings ID: "))
    account_exists = check_account_existence(cursor, referenced_table, "checkings_id", checkingsIDcontent)

    if account_exists:
      checkings_balance = handle_decimal_value_exception("Checking Account", checkingsIDcontent)
      query = "INSERT INTO bank_asset(checkings_id, checkings_balance) VALUES(%s, %s)"
      values = (checkingsIDcontent, checkings_balance)

      cursor.execute(query, values)
      connection.commit()
      display_rows_affected(cursor, "asset_id", cursor.lastrowid)

    else:
      print(f"Account {checkingsIDcontent} is non-existent...")

  except mysql.connector.Error as error:
      print(f"Error: {error}")

def add_transactions(connection, cursor):
  referenced_table = "checkings_account"
  os.system('cls')
  print("\n\t---Add New Transaction Information---\n")
  select_all_rows(cursor, referenced_table)
  
  while True:
    try:
      checkingsIDcontent = int(input("\t\tCheckings ID: "))
      account_exists = check_account_existence(cursor, referenced_table, "checkings_id", checkingsIDcontent)

      if account_exists:
        transaction_date = input_date("Transaction")
        amount = handle_decimal_value_exception("Checkings Account", checkingsIDcontent)
        transaction_type = input("\t\tTransaction Type: ")

        query = "INSERT INTO transactions(checkings_id, transaction_date, amount, transaction_type) VALUES (%s, %s, %s, %s)"
        values = (checkingsIDcontent, transaction_date, amount, transaction_type)

        cursor.execute(query, values)
        connection.commit()
        display_rows_affected(cursor, "transactions_id", cursor.lastrowid)

      else:
        print(f"Checkings Account {checkingsIDcontent} is non-existent...")

    except mysql.connector.Error as error:
      print(f"Error: {error}")





# NOTE: Admin

def adminMain():
  os.system('cls')
  connection = connect_database()
  
  while True:
    try:
      print("\n_______ADMIN AUTHORIZED_______\n"
      "\t[1] View Users\n"
      "\t[2] Edit Users\n"
      "\t[3] Delete Users\n"
      "\t[4] Add Users\n"
      "\t[5] Logout")
      
      action = int(input("\n\tAction: "))
      
      if action == 1:
        admin_view_user(connection)
        break

      elif action == 2:
        admin_edit_user(connection)
        break

      elif action == 3:
        admin_delete_user(connection)
        break

      elif action == 4:
        admin_add_user(connection)
        break
      
      elif action == 5:
        os.system('cls')
        banking_main()
      
      else:
        print("Invalid Input")
        
    except ValueError as error:
      display_error(error, "ValueError")


def admin_view_user(connection):
  os.system('cls')
  cursor = connection.cursor()
  
  while True:
    os.system('cls')
    print("\n\t_______VIEW USERS_______\n\n"
      "\t[1] Customer Information\n"
      "\t[2] Checkings Accounts\n"
      "\t[3] Bank Assets\n"
      "\t[4] Transactions\n"
      "\t[5] All Records\n"
      "\t[6] Return Home")
      
    try: 
      action = int(input("\n\tAction: "))
      
      if action == 1:  # [1] Customer Information: table name as the parameter
        select_all_rows(cursor, "customer_information") 
           
      elif action == 2: # [2] Checkings Accounts
        select_all_rows(cursor, "checkings_account")

      elif action == 3: # [3] Bank Assets
        select_all_rows(cursor, "bank_asset")
        
      elif action == 4: # [4] Transactions
        select_all_rows(cursor, "transactions")
      
      elif action == 5: # [5] All Records NOTE: the "all_records" is a VIEW which is used to JOIN all information of the tables
        select_all_rows(cursor, "all_records")

      elif action == 6:
        adminMain()
        
      else:
        print("Invalid Input...")
      
      if not continue_session(): # returns to main menu if false
        adminMain()
        
    except ValueError as error:
      display_error(error, "ValueError")
      
  
def admin_edit_user(connection):
  os.system('cls')
  cursor = connection.cursor()
  
  while True:
    os.system('cls')
    try:
      print("\n\t_______EDIT USERS_______\n\n" # data/values editing would be table-based
      "\t[1] Customer Information\n"
      "\t[2] Checkings Accounts\n"
      "\t[3] Bank Assets\n"
      "\t[4] Transactions\n"
      "\t[5] Return Home")

      action = int(input("\n\tEdit From: "))
      
      if action == 1: # for Customer Information
        print("\n---Customer Information---")
        table = "customer_information"
        select_all_rows(cursor, table) # displays all customer info
        customerIDcontent = int(input("\n\n\tCustomer ID: "))
        account_exists = check_account_existence(cursor, table, "customer_id", customerIDcontent)
        
        
        if account_exists:  
          print("\n\t [1] Customer ID\n\t [2] Customer Password\n\t [3] First Name\n\t [4] Last Name\n\t [5] Email\n\t [6] Address\n\t [7] ID Type\n\t [8] Occupation\n\t [9] Annual Gross Income\n\t")
          attribute = int(input("Choose Account Attribute: "))
          
          if attribute == 1:
            print("Customer ID is not editable.") # Assuming customer_id is not something the admin should update
          
          else: # code refactoring(for shorter lines)
            column = "customer_password" if attribute == 2 else "first_name" if attribute == 3 else "last_name" if attribute == 4 else "email" if attribute == 5 else "address" if attribute == 6 else "id_type" if attribute == 7 else "occupation" if attribute == 8 else "annual_gross_income" if attribute == 9 else None

            if column is not None:
              current_value = fetch_single_value(connection, cursor, table, column, "customer_id", customerIDcontent) # fetching the current value of the given column
              display_current_value(column, current_value)
              new_value = get_new_value(column)
              updating_query(connection, cursor, table, column, "customer_id" , customerIDcontent, new_value) # using customerID as ID 

           
      elif action == 2: # [2] Checkings Account
        print("\n---Customer Checkings Account---")
        table = "checkings_account"
        select_all_rows(cursor, table) # displays all checkings account info
        checkingsIDcontent = int(input("\n\n\tCheckings ID: "))
        account_exists = check_account_existence(cursor, table, "checkings_id", checkingsIDcontent)
        
        if account_exists:
          print("\n\t[1] Balance\n")
          attribute = int(input("\tChoose Account Attribute: "))
          
          if attribute == 1:
            column = "balance"
            current_balance = fetch_single_value(connection, cursor, table, column, "checkings_id",checkingsIDcontent) # fetching the current balance based on the given parameters
            print(f"\n\t---Current Balance: {current_balance}")

            try: 
              new_balance = get_decimal_input("\n\t\t---New Balance")
              
            except DecimalException as de:
              display_error(de, "Decimal ValueError")

            updating_query(connection, cursor, table, column, "checkings_id" , checkingsIDcontent, new_balance)
          
          else:
            print("Invalid Account Attribute")
            return
          
  
      elif action == 3: # [3] Bank Asset
        print("\n---Customer Bank Asset---")
        table = "bank_asset"
        select_all_rows(cursor, table) # displays all bank asset info
        bankAsset_ID = int(input("Bank Asset ID: "))
        account_exists = check_account_existence(cursor, table, "asset_id", bankAsset_ID)

        if account_exists:
          print("\n\t[1] Checkings Balance\n")
          attribute = int(input("\tChoose Account Attribute: "))

          if attribute == 1:
            column = "checkings_balance"
            current_checkingsBal = fetch_single_value(connection, cursor, table, column, "asset_id", bankAsset_ID)
            print(f"\n\t--Current Checkings Balance: {current_checkingsBal}")
            try:
              new_checkings_balance = get_decimal_input("\n\t---New Checkings Balance: ")
            
            except DecimalException as de:
              display_error(de, "Decimal ValueError")
            
            updating_query(connection, cursor, table, column, "asset_id", bankAsset_ID, new_checkings_balance)
          
          else:
            print("Invalid Account Attribute")
            return

   
      elif action == 4: # [4] Transactions
        print("\n\t---User Transactions")
        table = "transactions"
        select_all_rows(cursor, table) # displays all transactions info
        transactionID_content = int(input("\n\tTransaction ID: "))
        account_exists = check_account_existence(cursor, table, "transactions_id", transactionID_content)

        if account_exists:
          print("\n\t[1] Transaction Date\n\t[2] Amount\n\t[3] Transaction Type\n")
          attribute = int(input("Choose Account Attribute: "))
          
          if attribute == 1:
            column = "transaction_date"
            current_transaction_date = fetch_single_value(connection, cursor, table, column, "transactions_id", transactionID_content)
            display_current_value(column, current_transaction_date)
            new_value = input_date("Transaction")
          
          else:
            column = "amount" if attribute == 2 else "transaction_type" if attribute == 3 else None

            if column is not None:
              current_value = fetch_single_value(connection, cursor, table, column, "transactions_id", transactionID_content)
              display_current_value(column, current_value)
              new_value = get_new_value("Transaction Type")
          
          updating_query(connection, cursor, table, column, "transactions_id", transactionID_content, new_value)

      elif action == 5:
        adminMain()

      if not continue_session(): # looping
        adminMain()
      
    except ValueError as error:
      display_error(error, "ValueError")
    
    
def admin_delete_user(connection):
  os.system('cls')
  cursor = connection.cursor()
  while True:
    os.system('cls')
    try:
      print("\n\t_______DELETE USERS_______\n\n" 
      "\t[1] Customer Information\n"
      "\t[2] Checkings Accounts\n"
      "\t[3] Bank Assets\n"
      "\t[4] Transactions\n"
      "\t[5] Return Home")
      
      action = int(input("\n\tDelete From: "))
      
      if action == 1: # [1] Customer Information
        table = "customer_information"
        select_all_rows(cursor, table)
        customer_id_content = int(input("\n\tCustomer ID: "))
        delete_user_by_ID(connection, cursor, table, "customer_id", customer_id_content) # invoking the function for deletion given by the ff. parameters
          
          
      elif action == 2: # [2] Checkings Accounts
        table = "checkings_account"
        select_all_rows(cursor, table)
        checkings_id_content = int(input("\n\tCheckings Account ID: "))
        delete_user_by_ID(connection, cursor, table, "checkings_id", checkings_id_content)
        
        
      elif action == 3: # [3] Bank Assets
        table = "bank_asset"
        select_all_rows(cursor, table)
        asset_id_content = int(input("\n\tBank Asset ID: "))
        delete_user_by_ID(connection, cursor, table, "asset_id", asset_id_content)


      elif action == 4: # [4] Transactions
        table = "transactions"
        select_all_rows(cursor, table)
        transactions_id_content = int(input("\n\tTransaction ID: "))
        delete_user_by_ID(connection, cursor, table, "transactions_id", transactions_id_content)
        
      elif action == 5:
        adminMain()

    except ValueError as error:
      print(f"Invalid Input....{error}")


def admin_add_user(connection):
  os.system('cls')
  try:
    cursor = connection.cursor()
    
    while True:
      os.system('cls')
      print("\n\t_______ADD USERS_______\n\n"
        "\t[1] Customer Information\n"
        "\t[2] Checkings Accounts\n"
        "\t[3] Bank Assets\n"
        "\t[4] Transactions\n"
        "\t[5] Return Home\n")


      action = int(input("Add User To: "))
      
      if action == 1:
        add_customer_information(connection, cursor)

      elif action == 2:
        add_checkings_account(connection, cursor)

      elif action == 3:
        add_bank_asset(connection, cursor)

      elif action == 4:
        add_transactions(connection, cursor)

      elif action == 5:
        adminMain()

      else:
        continue
      
      if not continue_session():
        adminMain()
  
  except mysql.connector.Error as error:
    display_error(error, "MySQL")
  
  
  
# NOTE: Customer-associated functions
  
def customer_session(Balance, sessionType):
  while True:
    os.system('cls')
    try:
      print("\n\t___________________________\n" f"\n\tYour current balance is: {Balance}\n")
      
      # Get withdrawal | deposit | transfer amount from user
      session_amount_input = input(f"\tEnter the amount you want to {sessionType}: ")
      
      try:
        session_amount = Decimal(session_amount_input)  # convert the input to a Decimal
        break
        
      except ValueError:
        os.system('cls')
        print("\n\t___________________________\n" "\n\tError, please enter a valid decimal value")
        continue

    except Exception as e:
      os.system('cls')
      print(f"\n\t___________________________\n" f"\n\tError: {e}")
      continue
    
  return session_amount

def view_transaction_status(newBalance):
  print("\n\t___________________________\n"
            f"\n\tTransaction completed successfully, your new balance is {newBalance}.")
  input("\tPress Enter to Return to Customer Home Page...")

def add_transaction_history(connection, cursor, checkings_id, amount, transaction_type):
  try:
    cursor = connection.cursor()
    transaction_date = datetime.now().strftime("%Y-%m-%d") # returns the current date
    
    query = "INSERT INTO transactions(checkings_id, transaction_date, amount, transaction_type) VALUES(%s, %s, %s, %s)"
    values = (checkings_id, transaction_date, amount, transaction_type)
    cursor.execute(query, values)
    connection.commit()

  except mysql.connector.Error as error:
    display_error(error, "MySQL")




def display_transaction_history(connection, checking_account_id):
  try:
    os.system('cls')
    cursor = connection.cursor()
    fetch_query = "SELECT transactions_id, transaction_date, amount, transaction_type FROM transactions WHERE checkings_id = %s"
    cursor.execute(fetch_query, (checking_account_id,))
    print(f"\n\t-------Account {checking_account_id} Transaction History-------")
    format_table(cursor)
    
  except mysql.connector.Error as error:
      display_error(error, "MySQL")

  
  input("Press Enter to exit...")



def customerMain():
  os.system('cls')
  connection = connect_database()
  cursor = connection.cursor()

  while True:
    try:
      os.system('cls')
      checking_account_id = int(input("\n\tEnter your dedicate Checkings Account ID: "))
      account_exist = check_account_existence(cursor, "checkings_account", "checkings_id", checking_account_id)
      
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
              customer_withdraw(connection, checking_account_id)

            elif action == 2:
              customer_deposit(connection, checking_account_id)

            elif action == 3:
              customer_transfer(connection, checking_account_id)

            elif action == 4:
              customer_check_balance(connection, checking_account_id)
            
            elif action == 5:
              display_transaction_history(connection, checking_account_id)
              
            elif action == 6:
              os.system('cls')
              banking_main()
            
            else:
              print("Invalid Input...")
              continue
              
          except ValueError as error:
            display_error(error, "ValueError")
          
      else:
        os.system('cls')
        print(f"\n\t___________________________\n"
              f"\tInvalid Account Number...")
    
    except ValueError as error:
      display_error(error, "ValueError")
  
  
def customer_withdraw(connection, checking_account_id):
  os.system('cls')
  print("\n\t------WITHDRAWAL------\n")
  cursor = connection.cursor()
  table = "checkings_account"
  column = "balance"

  while True:
    Balance = fetch_single_value(connection, cursor, table, column, "checkings_id", checking_account_id)
    withdraw_amount = customer_session(Balance, "withdraw")
    

    if withdraw_amount <= Balance:
      try:
        os.system('cls')
        print(f"\n\tThe amount you want to withdraw is {withdraw_amount}...\n")
        newBalance = Balance - withdraw_amount

        # Update the balance in the checkings_account table
        updating_query(connection, cursor, table, column, "checkings_id", checking_account_id, newBalance)

      except Exception as e:
        print(f"Transaction Failed: {e}")
        if not continue_session():
          return

      view_transaction_status(newBalance)  # displays the transaction status
      add_transaction_history(connection, cursor, checking_account_id, withdraw_amount, "Withdraw")
      break


    elif withdraw_amount > Balance:
      os.system('cls')
      print(f"\n\t___________________________\n"
            f"\n\tThe amount you want to withdraw exceeds your current balance ({Balance})")

    if not continue_session():
      break


def customer_deposit(connection, checking_account_id):
  os.system('cls')
  print("\n\t------DEPOSIT------\n")
  cursor = connection.cursor()
  table = "checkings_account"
  column = "balance"

  while True:
    Balance = fetch_single_value(connection, cursor, table, column, "checkings_id", checking_account_id)
    deposit_amount = customer_session(Balance, "deposit")
    
    try:
      os.system('cls')
      print(f"\n\tThe amount you want to deposit is {deposit_amount}...\n")
      newBalance = Balance + deposit_amount
      
      updating_query(connection, cursor, table, column, "checkings_id", checking_account_id, newBalance)
      add_transaction_history(connection, cursor, checking_account_id, deposit_amount, "Deposit")
    
    except Exception as e:
      print(f"Transaction Failed: {e}")
      if not continue_session():
        return
    
    view_transaction_status(newBalance)
    break
    

def customer_transfer(connection, checking_account_id):
  os.system('cls')
  print("\n\t------TRANSFER------\n")
  cursor = connection.cursor()
  table = "checkings_account"
  column = "balance"
  
  while True:
    try:
      Balance = fetch_single_value(connection, cursor, table, column, "checkings_id", checking_account_id)
      transfer_amount = customer_session(Balance, "transfer")

      if Balance >= transfer_amount:
        while True: 
          
          try:
            os.system('cls')
            recepient_checkAccID = int(input("\tEnter the Account Number of the account to transfer to: "))
            account_exists = check_account_existence(cursor, table, "checkings_id", recepient_checkAccID)

            if account_exists and recepient_checkAccID != checking_account_id: # NOTE: executing the transfer
              
              # NOTE: Updating the Sending User Account Balance 
              sender_newBalance = Balance - transfer_amount
              updating_query(connection, cursor, table, column, "checkings_id", checking_account_id, sender_newBalance) 
              
              # NOTE: Updating the Receiving User Account Balance
              recepient_currentBal = fetch_single_value(connection, cursor, table, column, "checkings_id", recepient_checkAccID)
              recepient_newBalance = transfer_amount + recepient_currentBal
              updating_query(connection, cursor, table, column, "checkings_id", recepient_checkAccID, recepient_newBalance)

              view_transaction_status(sender_newBalance)
              add_transaction_history(connection, cursor, checking_account_id, transfer_amount, "Transfer")
              return # to the Main Menu
              
              
            if recepient_checkAccID == checking_account_id: # NOTE: Invalid Session
              print(f"\n\t___________________________\n"
                      f"\n\tInvalid Account Number..."
                      f"\n\tYou Entered your own Account Number which is invalid...")
              if not continue_session():
                return
              
            
          
          except mysql.connector.Error:
            os.system('cls')
            print(f"\n\t-------Account {checking_account_id} non-existent....-------")
            if not continue_session():
              return

      
      elif Balance < transfer_amount:
        os.system('cls') 
        print(f"\n\t___________________________\n" f"\n\tYou do not have the necessary funds to transfer that amount...")
        if not continue_session():
          return

    except ValueError:
      os.system('cls')
      print("\n\t___________________________\n" "\n\tError, please enter a valid amount...")
      if not continue_session():
        return
      

def customer_check_balance(connection, checking_account_id):
  os.system('cls')
  cursor = connection.cursor()
  Balance = fetch_single_value(connection, cursor, "checkings_account", "balance", "checkings_id", checking_account_id) # passing all the credentials as parameters to access the Balance
  print("\n\t___________________________\n")
  print(f"\tYour Current Balance is {Balance}.")
  input("\tPress Enter to Return to Customer Home Page...")



# MAIN program entrance
def banking_main():
  while True:
    os.system('cls')
    print("\n\t----------Treasury Citadel Banking System----------\n\n"
          "\t\t[1]: Admin / Employee\n\n"
          "\t\t[2]: User / Customer\n")
    
    action = int(input("\n\t\tLog In as: "))

    if action == 1:
      # implement admin's log in system
      adminMain()
      break
    
    elif action == 2:
      # implement customer's log in system
      customerMain()
      break

    else:
      os.system('cls')
      print("\n\t-------Invalid Credential....")
      input("\n\n\tPress enter to return to the main menu......")
      continue
      

banking_main()



