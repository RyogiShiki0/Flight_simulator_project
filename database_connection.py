import mysql.connector

def create_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        port='3306',
        database='flight_game',
        user='root',
        password='2004',
        autocommit=True
    )
    return connection
