import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
import time

start_time = time.perf_counter()

# Налаштування підключення до основного MySQL-кластера
config = {
    "host": "localhost",  # IP SQL-ноди кластера
    "port": "3310",  # Порт SQL-ноди
    "user": "myapp",
    "password": "my-super-password",
    "database": "mydb",  # Назва бази даних
}

fake = Faker()

# Функція для підключення до бази даних


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
            print("Successfully connected to MySQL Cluster at localhost:3310")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# Функція для генерації та вставки коментарів


def insert_comments(connection, comment_id, comment_text):
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
        print(f"Comment inserted with comment_id {comment_id}")
    except Error as e:
        print(f"Error inserting comment: {e}")


# Головна функція для вставки коментарів


def main():
    connection = connect_to_db()
    if not connection:
        return

    comment_id = 1  # Починаємо з 1
    for _ in range(1000):  # Генеруємо 1000 коментарів
        comment_text = fake.text()  # Генеруємо випадковий текст
        insert_comments(connection, comment_id, comment_text)
        comment_id += 1  # Наступний ідентифікатор
        time.sleep(random.uniform(0.1, 0.2))  # Затримка для реалістичності

    connection.close()

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Час виконання: {execution_time:.4f} секунд")


if __name__ == "__main__":
    main()
