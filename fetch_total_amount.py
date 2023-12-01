import mysql.connector



def connect_database():
    try:
        host = "localhost"
        username = "miguel"
        password = "password"
        database = "goods"

        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        print("Database Initialization Successful...")

    except mysql.connector.Error as error:
        print(error)
        connection = None

    return connection

def get_total_amount(checkings_id):
    connection = None  
    try:
        connection = connect_database()
        cursor = connection.cursor()

       
        deposit_query = """
            SELECT SUM(amount) 
            FROM transactions 
            WHERE checkings_id = %s AND transaction_type = 'deposit'
        """

        # Query to retrieve total amount for withdraws
        withdraw_query = """
            SELECT SUM(amount) 
            FROM transactions 
            WHERE checkings_id = %s AND transaction_type = 'withdrawal'
        """

        # Query to retrieve total amount for transfers
        transfer_query = """
            SELECT SUM(amount) 
            FROM transactions 
            WHERE checkings_id = %s AND transaction_type = 'transfer'
        """

        # Execute deposit query
        cursor.execute(deposit_query, (checkings_id,))
        total_deposit = cursor.fetchone()[0] or 0

        # Execute withdraw query
        cursor.execute(withdraw_query, (checkings_id,))
        total_withdraw = cursor.fetchone()[0] or 0

        # Execute transfer query
        cursor.execute(transfer_query, (checkings_id,))
        total_transfer = cursor.fetchone()[0] or 0

        print(f"Total Deposit amount for checkings_id {checkings_id}: {total_deposit}")
        print(f"Total Withdraw amount for checkings_id {checkings_id}: {total_withdraw}")
        print(f"Total Transfer amount for checkings_id {checkings_id}: {total_transfer}")

        return total_deposit, total_withdraw, total_transfer

    except mysql.connector.Error as error:
        print(error)

  

checkings_id = 1  
total_deposit, total_withdraw, total_transfer = get_total_amount(checkings_id)



