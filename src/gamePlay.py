import pygame as pg
from src.data.EnemyConfig import WAVE_STAT

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

    def loadMap(self, surface):
        self.map.load(surface)

    def LoadTowers(self, surface, box):
        for b in range(len(self.team)):
            box[b].pictureBox.img_path = self.team[b].img_src
            box[b].mainText.text = str(self.team[b].name)
            box[b].subText.text = str(self.team[b].in_game_price)
            box[b].item = self.team[b]
    def process_enemies(self):
        if self.curWave <= len(WAVE_STAT[self.mode]):
            enemyAmount = WAVE_STAT[self.mode][str(self.curWave)]
            for enemy_type in enemyAmount:
                for i in range(enemyAmount[enemy_type]):
                    self.enemyGroup.append(enemy_type)