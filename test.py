import sqlite3

connect = sqlite3.connect("src/data/tower_defense.db")
cursor = connect.cursor()

cursor.execute("SELECT * FROM Player")
print(cursor.fetchone())