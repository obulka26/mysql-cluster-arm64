import mysql.connector
import time

# Конфігурація бази даних кластера
config = {
    "host": "localhost",  # IP SQL-ноди кластера
    "port": "3310",  # Порт SQL-ноди
    "user": "myapp",
    "password": "my-super-password",
    "database": "mydb",  # Назва бази даних
}


# Функція для витягування коментарів з бази даних
def fetch_comments():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT comment_id, comment_text FROM Comments ORDER BY comment_id DESC LIMIT 50"
        )
        comments = cursor.fetchall()
        cursor.close()
        connection.close()
        return comments
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []


# Витягування даних і перевірка неконсистентності
def fetch_and_detect_inconsistencies():
    comments = fetch_comments()

    # Перевірка наявності коментарів для подальших дій
    if not comments:
        print("No comments found.")
        return []

    # Сортуємо коментарі за comment_id
    comments.sort(key=lambda x: x["comment_id"])

    # Перевірка неконсистентності (пропущені ідентифікатори)
    missing_ids = []
    for i in range(comments[0]["comment_id"], comments[-1]["comment_id"]):
        if i not in [c["comment_id"] for c in comments]:
            missing_ids.append(i)

    if missing_ids:
        print(f"Inconsistencies found! Missing comment IDs: {missing_ids}")
    else:
        print("No inconsistencies detected")

    return comments


# Безперервне витягування коментарів
def continuous_fetch():
    while True:
        print("\nFetching all comments...")
        comments = fetch_and_detect_inconsistencies()
        print("\nFetched comments:")
        for comment in comments:
            print(comment)
        time.sleep(5)


if __name__ == "__main__":
    continuous_fetch()
