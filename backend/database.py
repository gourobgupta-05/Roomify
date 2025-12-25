import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    """Create a database connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'airbnb_booking')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return connection

def execute_query(query, params=None):
    """Execute a query (INSERT, UPDATE, DELETE)."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return False

def execute_read_query(query, params=None):
    """Execute a read query (SELECT) and return results."""
    connection = create_connection()
    result = None
    if connection:
        try:
            cursor = connection.cursor(dictionary=True) # Return results as dictionaries
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return result
