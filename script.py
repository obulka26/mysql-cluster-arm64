import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name=None):
    connection = None
    try:
        if db_name:
            connection = mysql.connector.connect(
                host=host_name, user=user_name, password=user_password, database=db_name
            )
        else:
            connection = mysql.connector.connect(
                host=host_name, user=user_name, password=user_password
            )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def main():
    # Replace with your MySQL Cluster credentials
    host = "localhost"  # Use your actual host, e.g., 'ndb-mgmd' or 'localhost'
    user = "mysql"  # MySQL user
    password = ""  # MySQL password (if any)

    # Create connection
    connection = create_connection(host, user, password)

    # Create database
    create_database_query = "CREATE DATABASE IF NOT EXISTS test_db"
    execute_query(connection, create_database_query)

    # Connect to the newly created database
    connection = create_connection(host, user, password, "test_db")

    # Create table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT NOT NULL
    )
    """
    execute_query(connection, create_table_query)

    # Insert data
    insert_data_query = """
    INSERT INTO users (name, age) VALUES 
    ('Alice', 30),
    ('Bob', 25),
    ('Charlie', 35)
    """
    execute_query(connection, insert_data_query)

    # Simple query
    select_users_query = "SELECT * FROM users"
    cursor = connection.cursor()
    cursor.execute(select_users_query)
    rows = cursor.fetchall()

    print("Users:")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
