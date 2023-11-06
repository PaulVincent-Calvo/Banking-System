import mysql.connector # for connecting to mysql
import sys # for exiting the program
import os # for clearing the terminal

def line_printer():
    for x in range(100):
        print("=", end = "")

def header():
    line_printer()
    print("\n                                             Treasury Citadel")
    line_printer()

def home_page(connection):
    os.system('cls')
    header()
    print("\n                                                Home Page")
    line_printer()   

    print("\n\nWelcome to Treasury Citadel! How may we help you?\n")
    
    print("[1] Login as Employee\n[2] Login as Customer\n[3] Exit")

    while True:
        user_input = input("\nEnter your choice: ")
        try:
            check_user_input = int(user_input)
            if check_user_input < 1 or check_user_input > 3: 
                print ("Invalid input. Please enter a number from the given choices.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    if check_user_input == 1:
        employee_login_page(connection)
    elif check_user_input == 2:
        customer_login_page(connection)
    else:
        exit_page(connection)

def employee_login_page(connection):
    os.system('cls')
    header()
    print("\n                                            Employee Login Page")
    line_printer()   

    while True:
        employee_id = input("\n\nPlease enter your Employee ID: ")
        employee_password = input("\nPlease enter your Password: ")
        try:
            check_num = int(employee_id)
            if check_num < 1:
                print("Invalid Employee ID. Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    cursor = connection.cursor()
    employee_login_query = "SELECT employee_id, employee_password FROM employees WHERE employee_id = %s"
    cursor.execute(employee_login_query, (employee_id,))

    el_query_result = cursor.fetchone() 

    if el_query_result:
        stored_user_id, stored_user_password = el_query_result
        if employee_password == stored_user_password:
            cursor.close()
            employee_main_page(connection, employee_id)
            return
        else:
            cursor.close()
            print("Incorrect password")
    else:
        cursor.close()
        print("User not found")

    print("\nPlease choose an option.")
    print("[1] Retry \n[2] Return to Home Page \n[3] Exit")

    while True:
        retry = input("\nEnter your choice: ")
        try:
            check_retry = int(retry)
            if check_retry < 1 or check_retry > 3: 
                print ("Invalid input. Please enter a number from the given choices.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    if check_retry == 1:
        employee_login_page(connection)
    elif check_retry == 2:
        home_page(connection)
    else:
        exit_page(connection)

def check_customer_accounts(connection, employee_id):
    os.system('cls')
    header()
    print("\n                                            Check Accounts")
    line_printer()  

    print("\nPlease choose an option.")
    print("[1] Print all Customer Information\n[2] Print a specific customer's information\n[3] Return to Employee Main Page\n[4] Exit")

    while True:
        check_acc_choice = input("\nEnter your choice: ")
        try:
            int_check_acc_choice = int(check_acc_choice)
            if int_check_acc_choice < 1 or int_check_acc_choice > 4: 
                print ("Invalid input. Please enter a number from the given choices.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    if int_check_acc_choice == 1:
        os.system('cls')
        header()
        print("\n                                            Check Accounts")
        line_printer()

        # cursor = connection.cursor()

        # check_all_customer_info_query = """
        #     SELECT ci.customer_id, ci.customer_password, ci.first_name, ci.last_name, ci.email, ci.address, ci.id_type, ci.occupation, ci.annual_gross_income, ca.checkings_id, ca.balance 
        #     FROM customer_information ci
        #     LEFT JOIN checkings_account ca ON ci.customer_id = ca.customer_id
        #     WHERE ci.customer_id = %s
        # """
        # cursor.execute(check_all_customer_info_query, (customer_id,))
    
        # results = cursor.fetchall()
    
        # if results:
        #     customer_info = results[0]
        #     print(f"Customer ID: {customer_info[0]}")
        #     print(f"Customer Name: {customer_info[1]} {customer_info[2]}")
        #     print("Orders:")
        #     for result in results:
        #         order_id, order_date, product_name, quantity = result[3], result[4], result[5], result[6]
        #         print(f"  - Order ID: {order_id}")
        #         print(f"    Date: {order_date}")
        #         print(f"    Product: {product_name}")
        #         print(f"    Quantity: {quantity}")
        # else:
        #     print("Customer not found or has no orders")
    elif int_check_acc_choice == 2:
        print("Create Customer Account")
    elif int_check_acc_choice == 3:
        print("View Transactions")
    elif int_check_acc_choice == 4:
        home_page(connection)
    else:
        exit_page(connection)
def employee_main_page(connection, employee_id):
    os.system('cls')
    header()
    print("\n                                            Employee Main Page")
    line_printer()   

    cursor = connection.cursor()
    employee_name_query = "SELECT first_name, last_name FROM employees WHERE employee_id = %s"
    cursor.execute(employee_name_query, (employee_id,))

    en_query_result = cursor.fetchone()

    if en_query_result:
        first_name, last_name = en_query_result
        print(f"\n\nWelcome {first_name} {last_name}!\n")
    else:
        # for instances where there is an employee id and password in the database but the name isn't added
        print("\nEmployee Name not found")

    print("Please choose an option.")
    employee_choices = ["Check Customer Accounts", "Create New Customer Accounts", "View Transactions", "Logout", "Exit"]  # Use a list instead of a set for ordered choices

    for idx, choice in enumerate(employee_choices, 1):
        print(f"[{idx}] {choice}")

    while True:
        emp_main_choice = input("\nEnter your choice: ")
        try:
            int_emp_main_choice = int(emp_main_choice)
            if int_emp_main_choice < 1 or int_emp_main_choice > 5: 
                print ("Invalid input. Please enter a number from the given choices.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    if int_emp_main_choice == 1:
        print("Check Customer Accounts")
    elif int_emp_main_choice == 2:
        print("Create Customer Account")
    elif int_emp_main_choice == 3:
        print("View Transactions")
    elif int_emp_main_choice == 4:
        home_page(connection)
    else:
        exit_page(connection)
    

def customer_login_page(connection):
    os.system('cls')
    header()
    print("\n                                            Customer Login Page")
    line_printer()   

    while True:
        customer_id = input("\n\nPlease enter your Customer ID: ")
        customer_password = input("\nPlease enter your Password: ")
        try:
            check_num = int(customer_id)
            if check_num < 1:
                print("Invalid Customer ID. Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    cursor = connection.cursor()
    customer_login_query = "SELECT customer_id, customer_password FROM customer_information WHERE customer_id = %s"
    cursor.execute(customer_login_query, (customer_id,))

    cl_query_result = cursor.fetchone() 

    if cl_query_result:
        stored_user_id, stored_user_password = cl_query_result
        if customer_password == stored_user_password:
            cursor.close()
            customer_main_page(connection, customer_id)
            return
        else:
            cursor.close()
            print("Incorrect password")
    else:
        cursor.close()
        print("User not found")

    print("\nPlease choose an option.")
    print("[1] Retry \n[2] Return to Home Page \n[3] Exit")

    while True:
        retry = input("\nEnter your choice: ")
        try:
            check_retry = int(retry)
            if check_retry < 1 or check_retry > 3: 
                print ("Invalid input. Please enter a number from the given choices.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    if check_retry == 1:
        customer_login_page(connection)
    elif check_retry == 2:
        home_page(connection)
    else:
        exit_page(connection)

def customer_main_page(connection, customer_id):
    os.system('cls')
    header()
    print("\n                                            Customer Main Page")
    line_printer()   

    cursor = connection.cursor()
    customer_name_balance_query = """
            SELECT customer_information.first_name, customer_information.last_name, checkings_account.balance
            FROM customer_information 
            LEFT JOIN checkings_account ON customer_information.customer_id = checkings_account.customer_id
            WHERE customer_information.customer_id = %s
            """

    cursor.execute(customer_name_balance_query, (customer_id,))
    cb_query_result = cursor.fetchone()

    if cb_query_result:
        first_name, last_name, balance = cb_query_result
        print(f"\n\nWelcome {first_name} {last_name}!")
        
        if balance is not None:
            print(f"\nYour Balance: {balance:.2f}") 
        else:
            print("\nBalance information not found")
    else:
        # for instances where there is a customer id and password in the database but the name isn't added
        print("\nCustomer name not found")

def exit_page(connection):
    os.system('cls')
    header()
    print("\n                                                Exit Page")
    line_printer()   

    print("\n\nThank you for using Treasury Citadel's Banking System! We hope you have a wonderful day!")

    connection.close()
    sys.exit()

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root", # put user that you used when you were setting up MySQL (default is root)
        password="password", # put password that you used when you were setting up mysql
        database="banking_system"
    )

    home_page(connection)

except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
