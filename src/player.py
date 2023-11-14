from src import db


class Player:
    def __init__(self):
        self.name = None
        self.password = None
        self.coins = 0
        self.active = False
        self.isAuth = False

    def authenticate(self, name):
        players = db.select("select * from Player where name = ?", (name, ))

        if len(players) != 1:
            self.isAuth=False
            self.name = None
            self.password = None
            self.coins = 0
            self.active = False
        else:
            player = players[0]
            self.isAuth = True
            self.name = player[0]
            self.password = player[1]
            self.coins = player[2]
            self.active = True if player[3] == 1 else False
