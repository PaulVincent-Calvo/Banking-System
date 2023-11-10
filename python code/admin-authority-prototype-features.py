import mysql.connector
import os
from decimal import Decimal # for Decimal datatype input in mysql
from tabulate import tabulate # for precise (& effortless lol) tables & columns formatting 
from datetime import datetime


# NOTE: to finish (bukas ko gawin pagod na q)
#       1. Add User 
#       2. Adapt Customer Functionalities to the "bankingoop" -- dinuplicate ko kase database ni paul 


def connectDatabase():
  connection = None
  try:                     # NOTE: all users who will access the database must be connected to the same network
    host = "192.168.1.45"  # Set to this according to your internet's ipv4 address (to check the ip address, go to the terminal and type: ipconfig)
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
  print(f"\n\t{cursor.rowcount} row/s affected| {ID}: {IDContent}")


# function for FLEXIBLE updating the query in the admin_editUser function
def editUser_updatingQuery(connection, cursor, table, column, ID, IDcontent, value):
  main_query = f"UPDATE {table} SET {column} = %s WHERE {ID} = %s"
  cursor.execute(main_query, (value, IDcontent)) 
  connection.commit() # a must
  print(f"\n\t{cursor.rowcount} row/s affected| ID: {IDcontent}")
  if not continueSession(): # looping
    adminMain()


# function for DISPLAYING single values:                 primary key       value
def fetch_singleValues(connection, cursor, table, column,    ID,         IDcontent):
  cursor = connection.cursor()
  query = f"SELECT {column} FROM {table} WHERE {ID} = %s"
  value = IDcontent
  cursor.execute(query,(value,))
  Result = cursor.fetchone()
  return Result
  

# deletion query:
def deleteQuery(connection, cursor, table, ID, IDcontent, accountExistent):
  if accountExistent:
    query = f"DELETE FROM {table} WHERE {ID} = %s"
    try: 
      cursor.execute(query, (IDcontent,))
      connection.commit()
      print(cursor.rowcount, "row/s deleted....", cursor.lastrowid)
      
    except mysql.connector.Error as error:
      print(f"Deletion Error: {error}")
    
    if not continueSession():
      adminMain()
  
  else:
    print("Account Non-Existent")
    raise ValueError("Account does not exist")


def adminMain():
  os.system('cls')
  connection = connectDatabase()
  
  while True:
    try:
      print("\n_______ADMIN AUTHORIZED_______\n"
      "\t[1] View Users\n"
      "\t[2] Edit Users\n"
      "\t[3] Delete Users")
      
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
        # admin_addUser
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
      
      if action == 1:
        query = "SELECT * from customer_information"
        cursor.execute(query)
        tableFormatter(cursor) # formats the data
        if not continueSession(): # returns to home if continue_session ==0
          adminMain()
           
      elif action == 2:
        query = "SELECT * FROM checkings_account"
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()

      elif action == 3:
        query = "SELECT * FROM bank_asset"
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()
        
      elif action == 4:
        query = "SELECT * FROM transactions"
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()
      
      elif action == 5:
        
        query = "SELECT * FROM all_records" # using a VIEW to access the JOINED statements
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()
     
      else:
        print("Invalid Input...")
        
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
      "\t[4] Transactions\n"
      "\t[5] All Records")

      action = int(input("\n\tEdit From: "))
      
      if action == 1: # for Customer Information
        print("\n---Customer Information---")
        customerIDcontent = int(input("\n\tCustomer ID: "))
        table = "customer_information"
        account_exists = checkAcc_existence(cursor, table, "customer_id", customerIDcontent)
        
        
        if account_exists:  
          print("\n\t [1] Customer ID\n\t [2] Customer Password\n\t [3] First Name\n\t [4] Last Name\n\t [5] Email\n\t [6] Address\n\t [7] ID Type\n\t [8] Occupation\n\t [9] Annual Gross Income\n\t")
          attribute = int(input("Choose Account Attribute: "))
          
          if attribute == 1:
            # Assuming customer_id is not something the user should update
            print("Customer ID is not editable.")

          elif attribute == 2:
            column = "customer_password" # both are to be passed as arguments
            # fetching the current password
            current_pass = fetch_singleValues(connection, cursor, table, column, "customer_id", customerIDcontent) 
            print(f"\t---Current Password: {current_pass}")
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
        checkingsIDcontent = int(input("\n\tCheckings ID: "))
        table = "checkings_account"
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
        bankAsset_ID = int(input("Bank Asset ID: "))
        table = "bank_asset"
        account_exists = checkAcc_existence(cursor, table, "asset_id", bankAsset_ID)

        if account_exists:
          print("\n\t[1] Checkings Balance\n")
          attribute = int(input("\tChoose Account Attribute: "))

          if attribute == 1:
            column = "checkings_balance"
            current_checkingsBal = fetch_singleValues(connection, cursor, table, column, "asset_id", bankAsset_ID)
            print(f"\n\t--Current Checkings Balance: {current_checkingsBal}")
            new_checkingsBal = Decimal(input("New Checkings Balance: "))
          
          else:
            print("Account Attribute Non-existent")
            return

          editUser_updatingQuery(connection, cursor, table, column, "asset_id", bankAsset_ID, new_checkingsBal)
          

      
      elif action == 4: # [4] Transactions
        print("\n\t---User Transactions")
        table = "transactions"
        transactionID_content = int(input("\n\tTransaction ID: "))
        account_exists = checkAcc_existence(cursor, table, "transactions_id", transactionID_content)

        if account_exists:
          print("\n\t[1] Transaction Date\n\t[2] Amount\n\t[3] Transaction Type\n")
          attribute = int(input("Choose Account Attribute: "))

          if attribute == 1:
            column = "transaction_date"
            current_transacDate = fetch_singleValues(connection, cursor, table, column, "transactions_id", transactionID_content)
            print(f"\n\t---Current Transaction Date: {current_transacDate}")
            year = input("\n\t----Enter the year (YYYY): ")
            month = input("\n\t----Enter the month (MMMM): ")
            day = input("\n\t----Enter the day (DDDD): ")
            
            date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"  # Ensure two-digit month and day
            value = datetime.strptime(date_str, "%Y-%m-%d").date() # converting into date format
          
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
        customerIDcontent = int(input("\n\tCustomer ID: "))
        table = "customer_information"
        account_exists = checkAcc_existence(cursor, table, "customer_id", customerIDcontent)
        confirmDeletion = int(input("\n\t-CONFIRM Deletion? |1|: "))
        
        # NOTE: Foreign key constraints maintain referential integrity, ensuring that a user can only be deleted
        # IF AND ONLY IF its references in related tables have been addressed appropriately.

        if account_exists and confirmDeletion == 1:
          try: 
            cursor.execute("SET foreign_key_checks = 0") # disabling foreign key checks temporarily
            
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
        checkingsIDcontent = int(input("\n\tCheckings Account ID: "))
        table = "checkings_account"
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
        assetIDcontent = int(input("\n\tCheckings Account ID: "))
        table = "bank_asset"
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
        transactionID_content = int(input("\n\tCustomer ID: "))
        table = "transactions"
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






# TO FINISH


def admin_addUser(connection):
  cursor = connection.cursor()
  # customer_id (PK) AUTO-GENERATED/INCREMENT?
  # customer_password
  # first_name
  # last_name
  # email
  # address
  # id_type
  # occupation
  # annual_gross_income
  
  cust_fname = input("First Name: ")
  cust_lname = input("Last Name: ")
  cust_email = input("Email: ")
  cust_address = input("Address: ")
  cust_idType = input("ID Type: ")
  cust_occupation = input("Occupation: ")
  cust_annGrossIncome = Decimal(input("Annual Gross Income: "))

  query = f"INSERT INTO customer_information (first_name, last_name, email, address, id_type, occupation, annual_gross_income) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  values = (cust_fname, cust_lname, cust_email, cust_address, cust_idType, cust_occupation, cust_annGrossIncome)

  cursor.execute(query, values)
  connection.commit()






def checkCosAcc_existence(cursor, accnum): #only checks account number, may need password, non case sensitive
  query = f"SELECT * FROM customermainaccount WHERE AccountNumber = %s"
  cursor.execute(query, (accnum,))
  account_exists = cursor.fetchone()
  return account_exists


def customerWith(connection, accnum):
  os.system('cls')
  cursor = connection.cursor()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]

  while True:
    while True:
      try:
        os.system('cls')
        print("\n\t___________________________\n"
            f"\n\tYour cerrent balance is {Balance:.2f}\n")
        amount = int(input("\tEnter the amount you want to withdraw: "))
        break
      except ValueError:
        os.system('cls')
        print("\n\t___________________________\n"
              "\n\tError, please enter a valid integer")
        if not continueSession():
          return
      
    if amount <= Balance:
      os.system('cls')
      print(f"\n\tThe amount you want to withdraw is {amount}...\n")
      newbal = Balance - amount
      query = "UPDATE customermainaccount SET Balance = %s where AccountNumber = %s"
      cursor.execute(query, (newbal, accnum))
      connection.commit()

      query = "SELECT Balance from customermainaccount where AccountNumber = %s"
      cursor.execute(query,(accnum,))
      result = cursor.fetchone()
      Balance = result[0]
    
      print("\n\t___________________________\n"
            f"\n\tTransaction completed successfully, your new balance is {newbal:.2f}.")
      input("\tPress Enter to Return to Customer Home Page...")
      break

    elif amount > Balance:
      os.system('cls')
      print(f"\n\t___________________________\n"
            "\n\tThe amount you want to withdraw exceeds your current balnce")
      if not continueSession():
          break


def customerDpst(connection, accnum):
  os.system('cls')
  cursor = connection.cursor()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]

  while True:
    try:
      os.system('cls')
      print("\n\t___________________________\n"
          f"\n\tYour cerrent balance is {Balance:.2f}\n")
      amount = int(input("\tEnter the amount you want to deposit: "))
      break
    except ValueError:
        os.system('cls')
        print("\n\t___________________________\n"
              "\n\tError, please enter a valid integer")
        if not continueSession():
          return
    
  os.system('cls')
  print(f"\n\tThe amount you want to deposit is {amount}...\n")
  newbal = Balance + amount
  query = "UPDATE customermainaccount SET Balance = %s where AccountNumber = %s"
  cursor.execute(query, (newbal, accnum))
  connection.commit()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]

  print("\n\t___________________________\n"
        f"\n\tTransaction completed successfully, your new balance is {newbal:.2f}.")
  input("\tPress Enter to Return to Customer Home Page...")


def customerTrans(connection, accnum):
  os.system('cls')
  cursor = connection.cursor()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]
  
  while True: #Checks all possible errors first before proceeding, loops back at any point whenever it encounters an error.
    try:
      os.system('cls')
      print("\n\t___________________________\n"
          f"\n\tYour cerrent balance is {Balance:.2f}\n")
      amount = int(input("\n\tEnter the amount you want to transfer: "))
      if Balance >= amount:

        while True:
          try:
            targaccnum = str(input("\tEnter the Account Number of the account to transfer to: "))
            account_exist = checkCosAcc_existence(cursor, targaccnum)
  
            if account_exist and targaccnum!=accnum:
              break
            elif account_exist and targaccnum==accnum:
              os.system('cls')
              print(f"\n\t___________________________\n"
                    f"\n\tInvalid Account Number..."
                    f"\n\tYou Entered your own Account Number which is invalid...")
              if not continueSession():
                return
              break
            else:
              os.system('cls')
              print(f"\n\t___________________________\n"
                    f"\n\tInvalid Account Number...")
              if not continueSession():
                return
              break
          except ValueError:
              os.system('cls')
              print(f"\n\t___________________________\n"
                    f"\n\tError, please enter a valid Account Number")
              if not continueSession():
                return
              
        if account_exist and targaccnum!=accnum:
          break
      
      elif Balance < amount:
        os.system('cls')
        print(f"\n\t___________________________\n"
              f"\n\tYou do not have the necessary funds to transfer that amount...")
        if not continueSession():
                return
    except ValueError:
        os.system('cls')
        print("\n\t___________________________\n"
              "\n\tError, please enter a valid integer")
        if not continueSession():
          return

  #Transferring Amount from Source to Target
  newbalsrc = Balance - amount #Minuses amount from source
  query = "UPDATE customermainaccount SET Balance = %s where AccountNumber = %s"
  cursor.execute(query, (newbalsrc, accnum))
  connection.commit()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s" #Captures Target Balance
  cursor.execute(query,(targaccnum,))
  result = cursor.fetchone()
  Balance = result[0]

  newbaltarg = Balance + amount #Adds amount to target
  query = "UPDATE customermainaccount SET Balance = %s where AccountNumber = %s"
  cursor.execute(query, (newbaltarg, targaccnum))
  connection.commit()

  os.system('cls')
  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]
  print("\n\t___________________________\n"
        f"\n\tTransaction completed successfully, your new balance is {newbalsrc:.2f}.")
  input("\tPress Enter to Return to Customer Home Page...")


def customerBal(connection, accnum):
  os.system('cls')
  cursor = connection.cursor()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]
  print("\n\t___________________________\n")
  print(f"\tYour Current Balance is {Balance:.2f}.")
  input("\tPress Enter to Return to Customer Home Page...")


def customerMain():
  os.system('cls')
  connection = connectDatabase()
  cursor = connection.cursor()

  while True:
    accnum = input(str("\n\tEnter you dedicated account number: "))
    account_exist = checkCosAcc_existence(cursor, accnum)
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
            customerWith(connection, accnum)

          elif action == 2:
            customerDpst(connection, accnum)

          elif action == 3:
            customerTrans(connection, accnum)

          elif action == 4:
            customerBal(connection, accnum)
          
          elif action == 5:
            os.system('cls')
            break
          
          else:
            print("Invalid Input...")
            
        except ValueError as error:
          print(f"Invalid Input...")
    else:
      os.system('cls')
      print(f"\n\t___________________________\n"
            f"Invalid Account Number...")

  
# program entrance
adminMain()
#customerMain() # for customer page














# def fetchValues(cursor): # user-defined function to avoid reps in implementing the fetch_all function
#   results = cursor.fetchall()
#   for rows in results:
#     print(rows)
