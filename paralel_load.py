import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
import time
import threading

# Database configuration for connecting to the main MySQL cluster
config = {
    "host": "localhost",  # IP of the SQL node in the cluster
    "port": "3310",  # Port of the SQL node
    "user": "myapp",
    "password": "my-super-password",
    "database": "mydb",  # Database name
}

fake = Faker()


# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# Function to generate and insert comments
def insert_comments(connection, start_id, num_comments):
    try:
        cursor = connection.cursor()
        for i in range(num_comments):
            comment_id = start_id + i
            comment_text = fake.text()
            cursor.execute(
                """
                INSERT INTO Comments (comment_id, comment_text)
                VALUES (%s, %s)
                """,
                (comment_id, comment_text),
            )
            connection.commit()
            time.sleep(random.uniform(0.1, 0.2))  # Delay for realism
    except Error as e:
        print(f"Error inserting comment: {e}")
    finally:
        cursor.close()


# Main function to create threads and insert comments
def main():
    threads = []
    num_threads = 10
    comments_per_thread = 10000
    start_time = time.time()

    # Start each thread
    for thread_id in range(num_threads):
        connection = connect_to_db()
        if connection:
            start_id = thread_id * comments_per_thread + 1
            thread = threading.Thread(
                target=insert_comments, args=(
                    connection, start_id, comments_per_thread)
            )
            threads.append(thread)
            thread.start()
        else:
            print(f"Thread {thread_id}: Could not connect to database")

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    print(f"Total time taken: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()
