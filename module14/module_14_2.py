import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute('INSERT INTO users (name, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'Users{i}', f'example{i}@gmail.com', i * 10 , 1000))
# Обновите balance у каждой 2ой записи начиная с 1ой на 500:
cursor.execute('UPDATE users SET balance = 500 WHERE id % 2 <> 0')
# Удалите каждую 3ую запись в таблице начиная с 1ой:
cursor.execute("DELETE FROM users WHERE id % 3 == 1 ")

cursor.execute("SELECT * FROM users WHERE age <> 60")
rows = cursor.fetchall()
for row in rows:
    print(f'Имя: {row[0]} | Почта: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}')

# Удалите из базы данных not_telegram.db запись с id = 6.
cursor.execute("DELETE FROM users WHERE id = 6")
# Подсчитать общее количество записей.
cursor.execute("SELECT COUNT(*) FROM users")
# Посчитать сумму всех балансов.
cursor.execute("SELECT SUM(balance) FROM users")
# Вывести в консоль средний баланс всех пользователей.
cursor.execute("SELECT AVG(balance) FROM users")
average_balance = cursor.fetchone()[0]
print(f'Средний баланс всех пользователей: {average_balance}')

connection.commit()
connection.close()