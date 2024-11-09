import mysql.connector
from mysql.connector import Error

# Connection parameters
config = {
    "host": "localhost",
    "port": "3310",  # Replace with your actual port if different
    "user": "myapp",
    "password": "my-super-password",
    "database": "mydb",
}

connection = None

try:
    # Connect to the database
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Connected to MySQL Cluster")

        cursor = connection.cursor()

        # Create a database (if not exists) and use it
        cursor.execute("CREATE DATABASE IF NOT EXISTS mydb;")
        cursor.execute("USE mydb;")

        # Create a sample table in the database
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            age INT
        );
        """)
        print("Table 'users' created successfully.")

        # Insert sample data into the table
        insert_query = "INSERT INTO users (name, age) VALUES (%s, %s);"
        values = [("Alice", 30), ("Bob", 24), ("Charlie", 28)]
        cursor.executemany(insert_query, values)
        connection.commit()
        print(f"{cursor.rowcount} records inserted.")

        # Perform a simple select query
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        print("Data in 'users' table:")
        for row in results:
            print(row)

except Error as e:
    print("Error connecting to MySQL Cluster:", e)

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")
