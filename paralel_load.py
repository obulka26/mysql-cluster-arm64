import mysql.connector
from mysql.connector import Error
import pdb
import time
import threading
import sys
import os

# Database configuration for connecting to the main MySQL cluster
cluster_config = {
    "host": "localhost",  # IP of the SQL node in the cluster
    "port": "3310",  # Port of the SQL node
    "user": "myapp",
    "password": "my-super-password",
    "database": "mydb",  # Database name
}

node_configs = [
    {
        "host": "localhost",
        "port": "3307",
        "user": "user",
        "password": "password",
        "database": "shard1db",
    },
    {
        "host": "localhost",
        "port": "3308",
        "user": "user",
        "password": "password",
        "database": "shard2db",
    },
]

num_nodes = int(os.environ.get("num_nodes", "0"))
if num_nodes:
    print(f"\033[36mSeparate shards: {num_nodes} node(s)\033[0m")


if num_nodes:
    database_configs = node_configs[:num_nodes]
else:
    database_configs = [cluster_config]

empty_threads = os.environ.get("empty_threads", "false") != "false"
if empty_threads:
    print("\033[31mEmpty threads!\033[0m")

if len(sys.argv) < 2:
    print("Provide number of threads")
    sys.exit(1)

num_threads = int(sys.argv[1])
comments_per_thread = 1000 if len(sys.argv) < 3 else int(sys.argv[2])

# print(f"Number of threads {num_threads}")
# print(f"Comments per thread {comments_per_thread}")


# Function to connect to the database
def connect_to_db(config):
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
        # pdb.set_trace()
        return None


# Function to generate and insert comments
def insert_comments(connections, start_id):
    if empty_threads:
        return
    for i in range(comments_per_thread):
        comment_id = start_id + i
        comment_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        connection = connections[comment_id % num_nodes if num_nodes else 0]
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO Comments (comment_id, comment_text)
                VALUES (%s, %s)
                """,
                (comment_id, comment_text),
            )
            connection.commit()
        except Error as e:
            print(f"Error inserting comment: {e}")
        finally:
            cursor.close()


# Функція для підключення до кластеру без вказання бази даних
def connect_to_cluster(config, use_database=False):
    try:
        connection_config = config.copy()
        if not use_database:
            # Підключення без конкретної бази
            connection_config.pop("database")
        connection = mysql.connector.connect(**connection_config)
        if connection.is_connected():
            _ = config["database"] if use_database else "MySQL Cluster"
            # `print( f"Successfully connected to {db} at { config['host']}:{config['port']}")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL Cluster: {e}")
        return None


# Функція для створення бази даних
def recreate_database(connection, db_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        # print(f"Database '{db_name}' created successfully")
    except Error as e:
        print(f"Error recreating database: {e}")
    finally:
        cursor.close()


# Функція для створення таблиці
def create_table(connection):
    try:
        cursor = connection.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS Comments (
                comment_id INT PRIMARY KEY,
                comment_text TEXT NOT NULL
            )
            """
        if num_nodes == 0:  # cluster
            query += (
                " ENGINE=NDBCLUSTER;  -- Використовуємо NDBCLUSTER для розподілу даних"
            )
        cursor.execute(query)
        # print("Table 'Comments' created successfully in MySQL Cluster")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


# Основна функція для керування базою даних і таблицею


def manage_database():
    for config in database_configs:
        # Підключення без вибору бази, щоб мати змогу керувати самою базою
        connection = connect_to_cluster(config, use_database=False)
        if connection:
            # Дроп і створення бази даних
            recreate_database(connection, config["database"])
            connection.close()

        # Підключення до щойно створеної бази для створення таблиці
        connection = connect_to_cluster(config, use_database=True)
        if connection:
            # Створення таблиці
            create_table(connection)
        connection.close()


# Main function to create threads and insert comments
def main():
    manage_database()
    connections_per_thread = []

    for _ in range(num_threads):
        connections = []
        for config in database_configs:
            connection = connect_to_db(config)
            if connection:
                connections.append(connection)
            else:
                print("Could not connect to database")
                return
        connections_per_thread.append(connections)
    # Start each thread
    start_time = time.time()
    threads = []
    for thread_id in range(num_threads):
        start_id = thread_id * comments_per_thread + 1
        thread = threading.Thread(
            target=insert_comments, args=(
                connections_per_thread[thread_id], start_id)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    print(f"\033[32mTotal time taken to insert {comments_per_thread} comments by {num_threads} threads: {
          (total_time*1000):.2f} miliseconds\033[0m")


if __name__ == "__main__":
    main()
