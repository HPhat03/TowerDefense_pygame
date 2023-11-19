import pygame as pg


class Record:
    def __init__(self, map, login):
        self.map = map
        self.login = login
        self.team = self.login.team.copy()
        self.HP = 100
        self.budget = 0
        self.towerGroup = pg.sprite.Group()
        self.enemyGroup = pg.sprite.Group()

    def loadMap(self, surface):
        self.map.load(surface)

