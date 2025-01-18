import sqlite3


def initiate_db():
    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance INTEGER NOT NULL DEFAULT 1000
            )
        ''')
        conn.commit()

def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute("SELECT title, description, price FROM Products")
    products = cursor.fetchall()
    connection.commit()
    return products

def add_user(username, email, age):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)", (username, email, age, 1000))
    connection.commit()
    return cursor.lastrowid

def is_included(username):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.commit()
    return result is not None


