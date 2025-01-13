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
# Сделайте выборку всех записей при помощи fetchall(), где
# возраст не равен 60 и выведите их в консоль в следующем
# формате (без id):
# Имя: <username> | Почта: <email> | Возраст: <age> | Баланс:
# <balance>
cursor.execute("SELECT * FROM users WHERE age <> 60")
rows = cursor.fetchall()
for row in rows:
    print(f'Имя: {row[0]} | Почта: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}')

connection.commit()
connection.close()
