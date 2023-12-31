from src import db
from src.Tower import Tower


class Player:
    def __init__(self):
        self.name = None
        self.password = None
        self.id = None
        self.coins = 0
        self.active = False
        self.isAuth = False
        self.team = []
        self.inventory = []

    def authenticate(self, name):
        if name == "":
            return

        players = db.select("select * from Player where name = ?", (name, ))

        if len(players) == 1 and players[0][4] == 1:
            player = players[0]
            self.isAuth = True
            self.id = player[0]
            self.name = player[1]
            self.password = player[2]
            self.coins = player[3]
            self.active = True

            idTeams = db.select("""
                SELECT idTower1, idTower2, idTower3, idTower4, idTower5
                FROM Player INNER JOIN Player_Team
                    ON Player_Team.idPlayer = Player.id WHERE Player.name = ?
            """, (self.name, ))
            if len(idTeams) == 0:
                db.execute("INSERT INTO Player_Team(idPlayer) VALUES(?)", (self.id, ))
                idTeams = (None, ) * 5
            else:
                idTeams = idTeams[0]

            self.idInventory = db.select("""
                SELECT idTower
                FROM Player INNER JOIN Player_Towers
                    ON Player.id = Player_Towers.idPlayer
                WHERE Player.name = ?
                """, (self.name, ))

            self.team = [Tower(idTeams[i]) for i in range(5)
                         if idTeams[i] is not None]
            self.inventory = [Tower(i[0]) for i in self.idInventory]

    def update(self, team: bool = True, inventory: bool = True,
               coins: bool = True):
        if self.id is None:
            return

        if coins:
            db.execute("UPDATE Player SET coins = ? WHERE Player.name = ?",
                       (self.coins, self.name))
        if team:
            for i in range(len(self.team)):
                db.execute(f"""
                    UPDATE Player_Team SET idTower{i+1} = ? WHERE idPlayer = ?
                """, (self.team[i].id, self.id))
        if inventory:
            insertable = False
            for i in range(len(self.inventory)):
                for j in self.idInventory:
                    if j[0] == self.inventory[i].id:
                        insertable = False
                        break
                    else:
                        insertable = True
                        print(j[0], self.inventory[i].id)
                if insertable:
                    db.execute(
                        ("INSERT INTO Player_Towers(idPlayer, idTower) "
                         "VALUES (?,?)"), (self.id, self.inventory[i].id))

    def __str__(self):
        return f"name: {self.name}\ncoins: {self.coins}"
