import sqlite3


def create_connection():
    connection = sqlite3.connect("baza.db")  # Baza faylining nomi
    return connection


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT NOT NULL,
                        familya TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        phone TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()


def add_user_to_db(full_name, familya, age, phone):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO users (full_name, familya, age, phone)
                      VALUES (?, ?, ?, ?)''', (full_name, familya, age, phone))

    conn.commit()
    conn.close()


# def get_user_from_db(phone):
#     connection = create_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT full_name, familya, age, phone FROM users WHERE phone = ?", (phone,))
#     result = cursor.fetchone()
#     connection.close()
#     return result
    


