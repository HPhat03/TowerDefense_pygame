from src import db


class Player:
    def __init__(self):
        self.name = None
        self.password = None
        self.coins = 0
        self.active = False
        self.isAuth = False
        self.team = []

    def authenticate(self, name):
        players = db.select("select * from Player where name = ?", (name, ))

        if len(players) != 1 or players[0][4] != 1:
            self.isAuth = False
            self.name = None
            self.password = None
            self.coins = 0
            self.active = False
            self.team = []
        else:
            player = players[0]
            self.isAuth = True
            self.name = player[1]
            self.password = player[2]
            self.coins = player[3]
            self.active = True
            self.team = db.select("""
                SELECT Tower.*
                FROM (
                    (Player INNER JOIN Player_Towers
                        ON Player.id = Player_Towers.idPlayer)
                    INNER JOIN Tower
                        ON Player_Towers.idTower = Tower.id
                )
                WHERE Player.name = ?""", (self.name, ))
