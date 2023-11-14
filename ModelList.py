import sqlite3

import ModelList

Player_List = []
def ConnectDatabase():
    sqlite = sqlite3.connect('Database/tower_defense_db.db')
    cursor = sqlite.cursor()

    query = "SELECT * FROM Player"
    cursor.execute(query)
    ModelList.Player_List = cursor.fetchall()
    for u in ModelList.Player_List:
        print(u[0])