from src.data.EnemyConfig import WAVE_STAT
from src import db


class Record:
    def __init__(self, mode, map, login):
        self.map = map
        self.login = login
        self.team = self.login.team.copy()
        self.HP = 100
        self.budget = 500
        self.curWave = 1
        self.towerGroup = []
        self.mode = mode
        self.enemyGroup = []
        self.isSave: bool = False

    def loadMap(self, surface):
        self.map.load(surface)

    def LoadTowers(self, box):
        for b in range(len(self.team)):
            box[b].pictureBox.img_path = self.team[b].img_src
            box[b].mainText.text = str(self.team[b].name)
            box[b].subText.text = str(self.team[b].in_game_price)
            box[b].item = self.team[b]

    def process_enemies(self):
        if self.curWave <= len(WAVE_STAT[self.mode]):
            enemyAmount = WAVE_STAT[self.mode][self.curWave - 1]
            for enemy_type in enemyAmount:
                self.enemyGroup.extend([enemy_type] * enemyAmount[enemy_type])

    def save(self):
        if self.isSave:
            return

        db.execute("insert into Record values (?, ?, ?, ?)",
                   (self.map.id, self.login.id, self.curWave, self.mode))
        self.isSave = True
