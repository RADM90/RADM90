import mariadb

USER = 'USER_ID'
PASSWORD = 'USER_PASSWORD'
HOST_NAME = 'DBMS_URL'
PORT = 3306  # Default Port
DB = 'DB_'
CHARSET = 'utf8'


def connect_database():
    try:
        Connection = mariadb.connect(user=USER, password=PASSWORD, host=HOST_NAME, port=PORT, database=DB)
        Connection.autocommit = True
        return Connection
    except mariadb.Error as e:
        print(f"Error Connecting to Database: {e}")
        return None
