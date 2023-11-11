import mysql.connector
import os
from decimal import Decimal # for Decimal datatype input in mysql
from tabulate import tabulate # for precise (& effortless lol) tables & columns formatting 
from datetime import datetime


def connectDatabase():
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
    print(f"Failed Database Connectivity: {error}")
    
  return connection


def tableFormatter(cursor): # using the tabulate library
  rows = cursor.fetchall()
  if rows:
    # extract column names from the cursor.description
    headers = [desc[0] for desc in cursor.description]
    # use the tabulate function to format the results as a table
    table = tabulate(rows, headers, tablefmt="pretty")
    print(table)
  else:
      print("No records found.")
  
  
# SELECT/VIEW Queries
def selectAll_query(cursor, table):
  query = f"SELECT * FROM {table}"
  cursor.execute(query)
  tableFormatter(cursor)
  
  
def continueSession(): # dedicated for looping purposes
  continue_session = int(input("\nContinue Session (1 | 0): "))
  if continue_session == 1:
    return 1
  else:
    return 0

#                                     actual primary key name         value
def checkAcc_existence(cursor, table,        ID,                    IDcontent): # to be used in the admin_editUser and admin_deleteUser
  query = f"SELECT * FROM {table} WHERE {ID} = %s" # searches the customerID
  cursor.execute(query, (IDcontent,))
  account_exists = cursor.fetchone() # checks the account's existence
  return account_exists
  

def displayRowsAffected(cursor, ID, IDContent):
  print(f"\n\t{cursor.rowcount} session initiated| {ID}: {IDContent}")


# function for FLEXIBLE updating the query in the admin_editUser function
def editUser_updatingQuery(connection, cursor, table, column, ID, IDcontent, value):
  try:
    main_query = f"UPDATE {table} SET {column} = %s WHERE {ID} = %s"
    cursor.execute(main_query, (value, IDcontent)) 
    connection.commit() # a must
    # print(f"\n\t{cursor.rowcount} row/s affected| ID: {IDcontent}")
    displayRowsAffected(cursor, ID, IDcontent)
    
  except mysql.connector.Error:
    print("Session Error")
    if not continueSession():
      return
  


# function for DISPLAYING single values:                 primary key       value
def fetch_singleValues(connection, cursor, table, column,    ID,         IDcontent):
  try:
    cursor = connection.cursor()
    query = f"SELECT {column} FROM {table} WHERE {ID} = %s"
    value = IDcontent
    cursor.execute(query,(value,))
    Result = cursor.fetchone()
    return Result[0]
  
  except mysql.connector.Error:
    print("Session Error")
    if not continueSession():
      return
  

def input_date(description):
  try:
    year = input(f"\n\t---- {description} Year (YYYY): ")
    month = input(f"\n\t---- {description} Month (MM): ")
    day = input(f"\n\t---- {description} Day(DD): ")
  
    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"  # ensure two-digit month and day
    transaction_date = datetime.strptime(date_str, "%Y-%m-%d").date() # converting into date format

  except ValueError as error:
    print(f"Invalid Input: {error}")
  
  return transaction_date




def adminMain():
  os.system('cls')
  connection = connectDatabase()
  
  while True:
    try:
      print("\n_______ADMIN AUTHORIZED_______\n"
      "\t[1] View Users\n"
      "\t[2] Edit Users\n"
      "\t[3] Delete Users\n"
      "\t[4] Add Users")
      
      action = int(input("\n\tAction: "))
      
      if action == 1:
        admin_viewUser(connection)
        break

      elif action == 2:
        admin_editUser(connection)
        break

      elif action == 3:
        admin_deleteUser(connection)
        break

      elif action == 4:
        admin_addUser(connection)
        pass
      
      else:
        print("Invalid Input")
        
    except ValueError as error:
      print(f"Invalid Input: {error}")



def admin_viewUser(connection):
  os.system('cls')
  cursor = connection.cursor()
  
  while True:
    os.system('cls')
    print("\n\t_______VIEW USERS_______\n\n"
      "\t[1] Customer Information\n"
      "\t[2] Checkings Accounts\n"
      "\t[3] Bank Assets\n"
      "\t[4] Transactions\n"
      "\t[5] All Records")
      
    try: 
      action = int(input("\n\tAction: "))
      
      if action == 1:  # [1] Customer Information: table name as the parameter
        selectAll_query(cursor, "customer_information") 
           
      elif action == 2: # [2] Checkings Accounts
        selectAll_query(cursor, "checkings_account")

      elif action == 3: # [3] Bank Assets
        selectAll_query(cursor, "bank_asset")
        
      elif action == 4: # [4] Transactions
        selectAll_query(cursor, "transactions")
      
      elif action == 5: # [5] All Records NOTE: the "all_records" is a view used to JOIN all information the tables
        selectAll_query(cursor, "all_records")
     
      else:
        print("Invalid Input...")
      
      if not continueSession(): # returns to main menu if false
          adminMain()
        
    except ValueError as error:
      print("\n\tValue Error: ", error)

    
  
def admin_editUser(connection):
  os.system('cls')
  cursor = connection.cursor()
  
  while True:
    os.system('cls')
    try:
      print("\n\t_______EDIT USERS_______\n\n" # data/values editing would be table-based
      "\t[1] Customer Information\n"
      "\t[2] Checkings Accounts\n"
      "\t[3] Bank Assets\n"
      "\t[4] Transactions\n")

      action = int(input("\n\tEdit From: "))
      
      if action == 1: # for Customer Information
        print("\n---Customer Information---")
        table = "customer_information"
        selectAll_query(cursor, table) # displays all customer info
        customerIDcontent = int(input("\n\n\tCustomer ID: "))
        account_exists = checkAcc_existence(cursor, table, "customer_id", customerIDcontent)
        
        
        if account_exists:  
          print("\n\t [1] Customer ID\n\t [2] Customer Password\n\t [3] First Name\n\t [4] Last Name\n\t [5] Email\n\t [6] Address\n\t [7] ID Type\n\t [8] Occupation\n\t [9] Annual Gross Income\n\t")
          attribute = int(input("Choose Account Attribute: "))
          
          if attribute == 1:
            # Assuming customer_id is not something the admin should update
            print("Customer ID is not editable.")

          elif attribute == 2:
            column = "customer_password" # both are to be passed as arguments
            current_pass = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent) # fetching the current password
            print(f"\t---Customer {customerIDcontent} Current Password: {current_pass}")
            value = input("\t----New Account Password: ")

          elif attribute == 3:
            column = "first_name"
            current_fname = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent) 
            print(f"\t---Current First Name: {current_fname}")
            value = input("\t------New Customer First Name: ")

          elif attribute == 4:
            column = "last_name"
            current_lname = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent)
            print(f"\t---Current Last Name: {current_lname}")
            value = input("\t------New Customer Last Name: ")

          elif attribute == 5:
            column = "email"
            current_email = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent)
            print(f"\t---Current Email: {current_email}")
            value = input("\t------New Customer Email: ")

          elif attribute == 6:
            column = "address"
            current_address = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent)
            print(f"\t---Current Address: {current_address}")
            value = input("\t------New Customer Address: ")

          elif attribute == 7:
            column = "id_type"
            current_idType = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent)
            print(f"\t---Current ID Type: {current_idType}")
            value = input("\t------New Customer ID Type: ")
            
          elif attribute == 8:
            column = "occupation"
            current_occupation = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent)
            print(f"\t---Current Occupation: {current_occupation}")
            value = input("\t------New Customer Occupation: ")

          elif attribute == 9:
            column = "annual_gross_income"
            current_annGrossIncome = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent)
            print(f"\t---Current Annual Gross Income: {current_annGrossIncome}")
            value = input("\t------New Customer Annual Gross Income: ")

          else:
            print("Invalid choice. Please choose a valid attribute (1-9).")
            return
          
          editUser_updatingQuery(connection, cursor, table, column, "customer_id" , customerIDcontent, value) # using customerID as ID 


           
      elif action == 2: # [2] Checkings Account
        print("\n---Customer Checkings Account---")
        table = "checkings_account"
        selectAll_query(cursor, table) # displays all checkings account info
        checkingsIDcontent = int(input("\n\n\tCheckings ID: "))
        account_exists = checkAcc_existence(cursor, table, "checkings_id", checkingsIDcontent)
        
        if account_exists:
          print("\n\t[1] Balance\n")
          attribute = int(input("\tChoose Account Attribute: "))
          
          if attribute == 1:
            column = "balance"
            currentBal = fetch_singleValues(connection, cursor, table, column, "checkings_id",checkingsIDcontent) # fetching the current balance based on the given parameters
            print(f"\n\t---Current Balance: {currentBal}")
    
            new_balance = Decimal(input("\n\t\t---New Balance: "))
          
          else:
            print("Invalid Account Attribute")
            return
          
          editUser_updatingQuery(connection, cursor, table, column, "checkings_id" , checkingsIDcontent, new_balance)
          
          
      
      elif action == 3: # [3] Bank Asset
        print("\n---Customer Bank Asset---")
        table = "bank_asset"
        selectAll_query(cursor, table) # displays all bank asset info
        bankAsset_ID = int(input("Bank Asset ID: "))
        account_exists = checkAcc_existence(cursor, table, "asset_id", bankAsset_ID)

        if account_exists:
          print("\n\t[1] Checkings Balance\n")
          attribute = int(input("\tChoose Account Attribute: "))

          if attribute == 1:
            column = "checkings_balance"
            current_checkingsBal = fetch_singleValues(connection, cursor, table, column, "asset_id", bankAsset_ID)
            print(f"\n\t--Current Checkings Balance: {current_checkingsBal}")
            new_checkingsBal = Decimal(input("\n\t---New Checkings Balance: "))
          
          else:
            print("Account Attribute Non-existent")
            return

          editUser_updatingQuery(connection, cursor, table, column, "asset_id", bankAsset_ID, new_checkingsBal)
          

      
      elif action == 4: # [4] Transactions
        print("\n\t---User Transactions")
        table = "transactions"
        selectAll_query(cursor, table) # displays all transactions info
        transactionID_content = int(input("\n\tTransaction ID: "))
        account_exists = checkAcc_existence(cursor, table, "transactions_id", transactionID_content)

        if account_exists:
          print("\n\t[1] Transaction Date\n\t[2] Amount\n\t[3] Transaction Type\n")
          attribute = int(input("Choose Account Attribute: "))

          if attribute == 1:
            column = "transaction_date"
            current_transacDate = fetch_singleValues(connection, cursor, table, column, "transactions_id", transactionID_content)
            print(f"\n\t---Current Transaction Date: {current_transacDate}")
            value = input_date("Transaction") # invoking the function for date inputs
            
          
          elif attribute == 2:
            column = "amount"
            currentAmount = fetch_singleValues(connection, cursor, table, column, "transactions_id", transactionID_content)
            print(f"Current Transaction Amount: {currentAmount}")
            value = Decimal(input("New Transaction Amount: "))

          elif attribute == 3:
            column = "transaction_type"
            current_transacType = fetch_singleValues(connection, cursor, table, column, "transactions_id", transactionID_content)
            print(f"Current Transaction Type: {current_transacType}")
            value = input("New Transaction Type: ")

          else:
            print("Invalid Input")
            return

          editUser_updatingQuery(connection, cursor, table, column, "transactions_id", transactionID_content, value)
      
      if not continueSession(): # looping
        adminMain()
      
    except ValueError as error:
      print(f"Invalid Input: {error}")
    

        
def admin_deleteUser(connection):
  os.system('cls')
  cursor = connection.cursor()
  while True:
    os.system('cls')
    try:
      print("\n\t_______DELETE USERS_______\n\n" 
      "\t[1] Customer Information\n"
      "\t[2] Checkings Accounts\n"
      "\t[3] Bank Assets\n"
      "\t[4] Transactions\n")
      
      action = int(input("\n\tDelete From: "))
      
      if action == 1: # [1] Customer Information
        table = "customer_information"
        selectAll_query(cursor, table) 
        customerIDcontent = int(input("\n\tCustomer ID: "))
        account_exists = checkAcc_existence(cursor, table, "customer_id", customerIDcontent)
        confirmDeletion = int(input("\n\t-CONFIRM Deletion? |1|: "))
        
        # NOTE: Foreign key constraints maintain referential integrity, ensuring that a user can only be deleted
        # IF AND ONLY IF its references in related tables have been deleted

        if account_exists and confirmDeletion == 1:
          try: 
            cursor.execute("SET foreign_key_checks = 0") # disabling foreign key checks temporarily to avoid violating foreign key constraints.
            
            # delete records to NOTE: Child Tables
            delete_transactions_query = "DELETE FROM transactions WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s)"
            cursor.execute(delete_transactions_query, (customerIDcontent,))
            
            delete_bank_asset_query = "DELETE FROM bank_asset WHERE checkings_id IN (SELECT checkings_id FROM checkings_account WHERE customer_id = %s)"
            cursor.execute(delete_bank_asset_query, (customerIDcontent,))

            delete_checkings_account_query = "DELETE FROM checkings_account WHERE customer_id = %s"
            cursor.execute(delete_checkings_account_query, (customerIDcontent,))
            
            # delete record to NOTE: Parent Table
            delete_customer_query = "DELETE FROM customer_information WHERE customer_id = %s"
            cursor.execute(delete_customer_query, (customerIDcontent,))
            connection.commit()
            displayRowsAffected(cursor, "Customer ID", customerIDcontent)

          except mysql.connector.Error as error:
            print(f"Error: {error}")
            
          finally:
            cursor.execute("SET foreign_key_checks = 1") # enabling foreign key checks
        
        else:
          print(f"Account {customerIDcontent} is non-existent...")
          
        if not continueSession():
          adminMain()
          
          
      elif action == 2: # [2] Checkings Accounts
        table = "checkings_account"
        selectAll_query(cursor, table) 
        checkingsIDcontent = int(input("\n\tCheckings Account ID: "))
        account_exists = checkAcc_existence(cursor, table, "checkings_id", checkingsIDcontent)
        confirmDeletion = int(input("\n\t-CONFIRM Deletion? |1|: "))
        
        if account_exists and confirmDeletion == 1:
          try:
            cursor.execute("SET foreign_key_checks = 0")
            
            # deleting the NOTE: Child Tables
            delete_transactions_query = "DELETE FROM transactions WHERE checkings_id = %s"
            cursor.execute(delete_transactions_query,(checkingsIDcontent,))

            delete_bank_asset_query = "DELETE FROM bank_asset WHERE checkings_id = %s"
            cursor.execute(delete_bank_asset_query,(checkingsIDcontent,))

            # deleting the NOTE: Parent Table
            delete_checkings_account_query = "DELETE FROM checkings_account WHERE checkings_id = %s"
            cursor.execute(delete_checkings_account_query,(checkingsIDcontent,))
            connection.commit()
            displayRowsAffected(cursor, "Checkings ID", checkingsIDcontent)
            
          except mysql.connector.Error as error:
            print(f"Error: {error}")

          finally:
            cursor.execute("SET foreign_key_checks = 1")
      
        else:
          print(f"Account {checkingsIDcontent} is non-existent...")
          
        if not continueSession():
          adminMain()


      elif action == 3: # [3] Bank Assets
        table = "bank_asset"
        selectAll_query(cursor, table) 
        assetIDcontent = int(input("\n\tAsset Account ID: "))
        account_exists = checkAcc_existence(cursor, table, "asset_id", assetIDcontent)
        confirmDeletion = int(input("\n\t-CONFIRM Deletion? |1|: "))
        
        if account_exists and confirmDeletion == 1:
          try:
            cursor.execute("SET foreign_key_checks = 0")
            
            delete_bank_asset_query = "DELETE FROM bank_asset WHERE asset_id = %s"
            cursor.execute(delete_bank_asset_query,(assetIDcontent,))
            connection.commit()
            displayRowsAffected(cursor, "Asset ID", assetIDcontent)
            
          except mysql.connector.Error as error:
            print(f"Error: {error}")
            

          finally:
            cursor.execute("SET foreign_key_checks = 1")

        else:
          print(f"Account {assetIDcontent} is non-existent...")
        
        if not continueSession():
          adminMain()


      elif action == 4: # [4] Transactions
        table = "transactions"
        selectAll_query(cursor, table) 
        transactionID_content = int(input("\n\tTransaction ID: "))
        account_exists = checkAcc_existence(cursor, table, "transactions_id", transactionID_content)
        confirmDeletion = int(input("\n\t-CONFIRM Deletion? |1|: "))
        
        if account_exists and confirmDeletion == 1:
          try:
            cursor.execute("SET foreign_key_checks = 0")
            
            delete_transactions_query = "DELETE FROM transactions WHERE transactions_id = %s"
            cursor.execute(delete_transactions_query,(transactionID_content,))
            connection.commit()
            displayRowsAffected(cursor, "Transaction ID", transactionID_content)

          except mysql.connector.Error as error:
            print(f"Error: {error}")
          
          finally:
            cursor.execute("SET foreign_key_checks = 1")

        else:
          print(f"Account {transactionID_content} is non-existent...")
        
        if not continueSession():
          adminMain()
        

    except ValueError as error:
      print(f"Invalid Input....{error}")



def admin_addUser(connection):
  cursor = connection.cursor()
  
  while True:
    os.system('cls')
    print("\n\t_______ADD USERS_______\n\n"
      "\t[1] Customer Information\n"
      "\t[2] Checkings Accounts\n"
      "\t[3] Bank Assets\n"
      "\t[4] Transactions\n")

    action = int(input("Add User To: "))

    
    if action == 1: # [1] Customer Information
      while True:
        os.system('cls')
        print("\n\t---Add New Customer Information---\n")
        
        try:
          cust_fname = input("\t\tFirst Name: ")
          cust_lname = input("\t\tLast Name: ")
          cust_email = input("\t\tEmail: ")
          cust_address = input("\t\tAddress: ")
          cust_idType = input("\t\tID Type: ")
          cust_occupation = input("\t\tOccupation: ")
          cust_annGrossIncome = Decimal(input("\t\tAnnual Gross Income: "))
          
          query = f"INSERT INTO customer_information (first_name, last_name, email, address, id_type, occupation, annual_gross_income) VALUES (%s, %s, %s, %s, %s, %s, %s)"
          values = (cust_fname, cust_lname, cust_email, cust_address, cust_idType, cust_occupation, cust_annGrossIncome)

          cursor.execute(query, values)
          connection.commit()
          displayRowsAffected(cursor, "customer_id", cursor.lastrowid)
          
        except ValueError as error:
          print(f"\t\tInvalid Input: {error}")
          
        break
      
      
    elif action == 2: # [2] Checkings Accounts
      table = "customer_information" # to check if the account is existent, NOTE that the customer_id MUST exist first in the PARENT TABLE(customer_info) because it is referenced as a foreign key to the CHILD TABLE(checkings_account)
      while True:
        os.system('cls')
        print("\n\t---Add New Checkings Account Info---\n")
        selectAll_query(cursor, table)
        
        try:
          customerIDcontent = int(input("\t\tCustomer ID: "))
          account_exists = checkAcc_existence(cursor, table, "customer_id", customerIDcontent )
          if account_exists:
            balance = Decimal(input(f"\t\tCustomer {customerIDcontent} Account Balance: "))
            query = "INSERT INTO checkings_account (customer_id, balance) VALUES(%s, %s)"
            values = (customerIDcontent, balance)
            
            cursor.execute(query, values)
            connection.commit()
            displayRowsAffected(cursor, "checkings_id", cursor.lastrowid)
          
          else:
            print(f"Customer {customerIDcontent} is non-existent...")
        
        except mysql.connector.Error as error:
          print(f"Error: {error}")
        
        break

        
    elif action == 3: # [3] Bank Assets
      table = "checkings_account" # NOTE: because the bank_asset table has a foreign key reference to the checkings_account table
      while True:
        os.system('cls')
        print("\n\t---Add New Bank Asset Info---\n")
        selectAll_query(cursor, table)
        
        try:
          checkingsIDcontent = int(input("\t\tCheckings ID: "))
          account_exists = checkAcc_existence(cursor, table, "checkings_id", checkingsIDcontent)

          if account_exists:
            checkings_balance = Decimal(input(f"\t\tChecking Account {checkingsIDcontent} Balance: "))
            query = "INSERT INTO bank_asset(checkings_id, checkings_balance) VALUES(%s, %s)"
            values = (checkingsIDcontent, checkings_balance)
            
            cursor.execute(query, values)
            connection.commit()
            displayRowsAffected(cursor, "asset_id", cursor.lastrowid)
          
          else:
            print(f"Account {checkingsIDcontent} is non-existent...")
        
        except mysql.connector.Error as error:
          print(f"Error: {error}")
        
        break
        
        
    elif action == 4: # [4] Transactions
      table = "checkings_account" # NOTE: because the transactions table has a foreign key reference to the checkings_account table
      while True:
        os.system('cls')
        print("\n\t---Add New Transaction Information---\n")
        selectAll_query(cursor, table)
        
        try:
          checkingsIDcontent = int(input("\t\tCheckings ID: "))
          account_exists = checkAcc_existence(cursor, table, "checkings_id", checkingsIDcontent)
          
          if account_exists:
            # transaction date
            transaction_date = input_date("Transaction")
            amount = Decimal(input(f"\n\t---- Checkings Account {checkingsIDcontent} Amount: "))
            transaction_type = input("\t\tTransaction Type: ")
            
            query = "INSERT INTO transactions(checkings_id, transaction_date, amount, transaction_type) VALUES (%s, %s, %s, %s)"
            values = (checkingsIDcontent, transaction_date, amount, transaction_type)
            
            cursor.execute(query, values)
            connection.commit()
            displayRowsAffected(cursor, "transactions_id", cursor.lastrowid)

          else:
            print(f"Checkings Account {checkingsIDcontent} is non-existent...")
        
        except mysql.connector.Error as error:
          print(f"Error: {error}")
        
        break


    else:
      continue
    
    if not continueSession():
      adminMain()
  
  
  
  
# Reusable functions for customer withdrawal | deposit | transfer
def customerSession(Balance, sessionType):
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


def displayTransaction_status(newBalance):
  print("\n\t___________________________\n"
            f"\n\tTransaction completed successfully, your new balance is {newBalance}.")
  input("\tPress Enter to Return to Customer Home Page...")



def customerMain():
  os.system('cls')
  connection = connectDatabase()
  cursor = connection.cursor()

  while True:
    checking_account_id = int(input("\n\tEnter your dedicate Checkings Account ID: "))
    account_exist = checkAcc_existence(cursor, "checkings_account", "checkings_id", checking_account_id)
    
    if account_exist:
      while True:
        try:
          os.system('cls')
          print("\n_______Customer Page_______\n"
          "\t[1] Withdraw Money\n"
          "\t[2] Deposit Amount\n"
          "\t[3] Transfer Money\n"
          "\t[4] Check Balance\n"
          "\t[5] Logout")
          
          action = int(input("\n\tAction: "))
          
          if action == 1:
            customerWithdraw(connection, checking_account_id)

          elif action == 2:
            customerDeposit(connection, checking_account_id)

          elif action == 3:
            customerTransfer(connection, checking_account_id)

          elif action == 4:
            customerCheckBal(connection, checking_account_id)
          
          elif action == 5:
            os.system('cls')
            break
          
          else:
            print("Invalid Input...")
            continue
            
        except ValueError as error:
          print(f"Invalid Input...{error}")
          
    else:
      os.system('cls')
      print(f"\n\t___________________________\n"
            f"\tInvalid Account Number...")

  
def customerWithdraw(connection, checking_account_id):
  os.system('cls')
  print("\n\t------WITHDRAWAL------\n")
  cursor = connection.cursor()
  table = "checkings_account"
  column = "balance"

  while True:
    Balance = fetch_singleValues(connection, cursor, table, column, "checkings_id", checking_account_id)
    withdraw_amount = customerSession(Balance, "withdraw")
    

    if withdraw_amount <= Balance:
      try:
        os.system('cls')
        print(f"\n\tThe amount you want to withdraw is {withdraw_amount}...\n")
        newBalance = Balance - withdraw_amount

        # Update the balance in the checkings_account table
        editUser_updatingQuery(connection, cursor, table, column, "checkings_id", checking_account_id, newBalance)

      except Exception as e:
        print(f"Transaction Failed: {e}")
        if not continueSession():
          return

      displayTransaction_status(newBalance)  # displays the transaction status
      break


    elif withdraw_amount > Balance:
      os.system('cls')
      print(f"\n\t___________________________\n"
            f"\n\tThe amount you want to withdraw exceeds your current balance ({Balance})")

    if not continueSession():
      break


def customerDeposit(connection, checking_account_id):
  os.system('cls')
  print("\n\t------DEPOSIT------\n")
  cursor = connection.cursor()
  table = "checkings_account"
  column = "balance"

  while True:
    Balance = fetch_singleValues(connection, cursor, table, column, "checkings_id", checking_account_id)
    deposit_amount = customerSession(Balance, "deposit")
    
    try:
      os.system('cls')
      print(f"\n\tThe amount you want to deposit is {deposit_amount}...\n")
      newBalance = Balance + deposit_amount
      
      editUser_updatingQuery(connection, cursor, table, column, "checkings_id", checking_account_id, newBalance)
    
    except Exception as e:
      print(f"Transaction Failed: {e}")
      if not continueSession():
        return
    
    displayTransaction_status(newBalance)
    break
    


def customerTransfer(connection, checking_account_id):
  os.system('cls')
  print("\n\t------TRANSFER------\n")
  cursor = connection.cursor()
  table = "checkings_account"
  column = "balance"
  
  while True:
    try:
      Balance = fetch_singleValues(connection, cursor, table, column, "checkings_id", checking_account_id)
      transfer_amount = customerSession(Balance, "transfer")

      if Balance >= transfer_amount:
        while True: 
          
          try:
            os.system('cls')
            recepient_checkAccID = int(input("\tEnter the Account Number of the account to transfer to: "))
            account_exists = checkAcc_existence(cursor, table, "checkings_id", recepient_checkAccID)

            if account_exists and recepient_checkAccID != checking_account_id: # NOTE: executing the transfer
              
              # NOTE: Updating the Sending User Account Balance 
              sender_newBalance = Balance - transfer_amount
              editUser_updatingQuery(connection, cursor, table, column, "checkings_id", checking_account_id, sender_newBalance) 
              
              # NOTE: Updating the Receiving User Account Balance
              recepient_currentBal = fetch_singleValues(connection, cursor, table, column, "checkings_id", recepient_checkAccID)
              recepient_newBalance = transfer_amount + recepient_currentBal
              editUser_updatingQuery(connection, cursor, table, column, "checkings_id", recepient_checkAccID, recepient_newBalance)

              displayTransaction_status(sender_newBalance)
              return # to the Main Menu
              
              
            if recepient_checkAccID == checking_account_id: # NOTE: Invalid Session
              print(f"\n\t___________________________\n"
                      f"\n\tInvalid Account Number..."
                      f"\n\tYou Entered your own Account Number which is invalid...")
              if not continueSession():
                return
              
            
          
          except mysql.connector.Error:
            os.system('cls')
            print(f"\n\t-------Account {checking_account_id} non-existent....-------")
            if not continueSession():
              return

      
      elif Balance < transfer_amount:
        os.system('cls') 
        print(f"\n\t___________________________\n" f"\n\tYou do not have the necessary funds to transfer that amount...")
        if not continueSession():
          return

    except ValueError:
      os.system('cls')
      print("\n\t___________________________\n" "\n\tError, please enter a valid amount...")
      if not continueSession():
        return
      

  
def customerCheckBal(connection, checking_account_id):
  os.system('cls')
  cursor = connection.cursor()
  Balance = fetch_singleValues(connection, cursor, "checkings_account", "balance", "checkings_id", checking_account_id) # passing all the credentials as parameters to access the Balance
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



