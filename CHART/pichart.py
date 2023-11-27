import matplotlib.pyplot as p
import mysql.connector

   
def connect_database():
    try:                     
      host =  "192.168.1.19" 
      username = " user_treasury_citadel"
      password =  "tC23_oop_dbms_pRoj2023"
      database = "treasury_citadel_database"

      connection = mysql.connector.connect(
          host= host,
          user= username,
          password= password,
          database= database)
    
      print("Database Initialization Successful...")
    
    except mysql.connector.Error as error:
      print(error)
      
    return connection

connection = connect_database()
cursor = connection.cursor()



def fetch_count(connection, transac_type):
    cursor = connection.cursor()
    query = '''
    SELECT COUNT(transaction_type) AS occurrence_count
    FROM your_table_name
    WHERE transaction_type = %s
    '''
    
    cursor.execute(query, (transac_type,))
    result = cursor.fetchone()

    # If there are no results, set default values
    if result:
        count_transac = result[0]
    else:
        count_transac = 0

    return count_transac

count_withdraw = fetch_count(connection, "Withdraw")
print(count_withdraw)




s = [40, 30, 10,]
l = ["transfer", "deposit", "Withdraw"]

p.pie(s,labels=l)
p.show()