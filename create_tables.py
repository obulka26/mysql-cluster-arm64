import mysql.connector
from mysql.connector import Error

# Конфігурація підключення до SQL-ноди кластера
config = {
    "host": "localhost",  # IP SQL-ноди кластера
    "port": "3310",  # порт SQL-ноди
    "user": "myapp",
    "password": "my-super-password",
    "database": "mydb",  # Назва бази даних, яку будемо створювати/перезаписувати
}


# Функція для підключення до кластеру без вказання бази даних
def connect_to_cluster(config, use_database=False):
    try:
        connection_config = config.copy()
        if not use_database:
            # Підключення без конкретної бази
            connection_config.pop("database")
        connection = mysql.connector.connect(**connection_config)
        if connection.is_connected():
            db = config["database"] if use_database else "MySQL Cluster"
            print(
                f"Successfully connected to {db} at {
                    config['host']}:{config['port']}"
            )
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
        print(f"Database '{db_name}' created successfully")
    except Error as e:
        print(f"Error recreating database: {e}")
    finally:
        cursor.close()


# Функція для створення таблиці
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Comments (
            comment_id INT PRIMARY KEY,
            comment_text TEXT NOT NULL
        ) ENGINE=NDBCLUSTER;  -- Використовуємо NDBCLUSTER для розподілу даних
        """)
        print("Table 'Comments' created successfully in MySQL Cluster")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


# Основна функція для керування базою даних і таблицею
def manage_database():
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


if __name__ == "__main__":
    manage_database()
