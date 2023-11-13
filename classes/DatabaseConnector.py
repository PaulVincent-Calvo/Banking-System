import mysql.connector

class DatabaseConnector():
    def __init__(self):
        self.connection = None

    def connect_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="banking_system"
            )
            self.connection = connection

        except mysql.connector.Error as err:
            raise ConnectionError(f"Database Connection Error: {err}")

    def database_connection_error(self, message):
        print(message)

    def close_database(self):
        if self.connection is not None:
            self.connection.close()

