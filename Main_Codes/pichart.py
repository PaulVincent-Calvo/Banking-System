import matplotlib.pyplot as p
import mysql.connector

   
class Pie_Chart:
    def connect_database(self):
        try:                     
            host =  "localhost" 
            username = "root"
            password =  ""
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

    

    def fetch_count(self, connection, transac_type):
        cursor = connection.cursor()
        query = '''
        SELECT COUNT(transaction_type) AS occurrence_count
        FROM transactions
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

    def main(self):
        connection = self.connect_database()

        count_withdraw = self.fetch_count(connection, "Withdraw")
        count_deposit = self.fetch_count(connection, "Deposit")
        count_transfer = self.fetch_count(connection, "Transfer")
        print(count_withdraw)

        s = [count_withdraw, count_deposit, count_transfer,]
        l = ["Withdraw", "Deposit", "Transfer"]

        p.pie(s,labels=l)
        p.show()


# pie_chart = Pie_Chart()
# pie_chart.main()