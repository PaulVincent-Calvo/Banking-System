import mysql.connector

class DatabaseConnector():
    def __init__(self):
        self.connection = None

    def connect_database(self):
        try:
            connection = mysql.connector.connect(
                host="192.168.43.188",
                user="miguel",
                password="password",
                database="bankingoop"
            )
            self.connection = connection
            print("ace pogi tayo")

        except mysql.connector.Error as err:
            raise ConnectionError(f"Database Connection Error: {err}")

    def database_connection_error(self, message):
        print(message)

    def close_database(self):
        if self.connection is not None:
            self.connection.close()

