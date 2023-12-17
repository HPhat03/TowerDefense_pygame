import math

import pygame as pg
from src import db
from src.data.TowerLevelConfig import TowerStat
from src import setting
from abc import abstractmethod


class Towers:
    SCOUT = 1
    SNIPER = 2

    @staticmethod
    def get_all():
        return [{
            "id": data[0],
            "name": data[1],
            "img_src": data[2],
            "in_shop_price": data[3],
            "in_game_price": data[4]
        } for data in db.select("select * from Tower")]


class Tower:
    def __init__(self, id: int):
        data = db.select("select * from Tower where id=?", (id, ))[0]

        self.id, self.name, self.img_src, \
            self.in_shop_price, self.in_game_price = data
        self.OriginalImage = pg.image.load(self.img_src)

    def draw(self, surface):
        self.img = pg.image.load(self.img_src).convert_alpha()
        surface.blit(self.img, (10, 10))

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "img_src": self.img_src,
            "in_shop_price": self.in_shop_price,
            "in_game_price": self.in_game_price
        }

    def __eq__(self, other):
        if not isinstance(other, Tower):
            return NotImplemented
        return self.id == other.id

    def isPlaceable(self, record, x, y):
        if record.map.map_data[y * setting.MAP_WIDTH_TILE + x] == record.map.path:
            return False
        for i in record.towerGroup:
            if i.tile_x == x and i.tile_y == y:
                return False
        if len(record.towerGroup) >= 20:
            return False
        return True


class BattleTower(Tower):
    def __init__(self, id, tile_X, tile_Y):
        super().__init__(id)
        self.rect = self.OriginalImage.get_rect()
        self.tile_x = tile_X
        self.tile_y = tile_Y
        self.x = (self.tile_x + 0.5) * setting.MAP_TILE_SIZE
        self.y = (self.tile_y + 0.5) * setting.MAP_TILE_SIZE
        self.pos = (self.x, self.y)
        self.rect.center = self.pos
        self.angle = 0

    @abstractmethod
    def draw(self, screen):
        pass


class NormalScout(BattleTower):
    def __init__(self, id, tile_X, tile_Y):
        super().__init__(id, tile_X, tile_Y)
        # init stat
        self.level = 1
        stat = TowerStat[self.name]["1"]
        self.atk = stat["atk"]
        self.speed = stat["speed"]
        self.bound = stat["bound"]
        self.levelUp = stat["levelUp"]

        # transparent bound:
        self.isFocus = True
        # enemy queue
        self.enemyQueue = []
        # cooldown
        self.timeStart = pg.time.get_ticks()

    def updateTower(self):
        if self.level < 5:
            self.level += 1
            stat = TowerStat[self.name][f"{self.level}"]
            self.atk = stat["atk"]
            self.speed = stat["speed"]
            self.bound = stat["bound"]
            self.levelUp = stat["levelUp"]

    def draw(self, surface):
        self.image = pg.transform.rotate(self.OriginalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        surface.blit(self.image, (self.rect.left, self.rect.top))
        if self.isFocus:
            self.boundSf = pg.Surface((self.bound * 2, self.bound * 2))
            self.boundSf.fill((0, 0, 0))
            self.boundSf.set_colorkey((0, 0, 0))
            pg.draw.circle(self.boundSf, "white", (self.bound, self.bound),
                           self.bound)
            self.boundSf.set_alpha(100)
            self.boundRect = self.boundSf.get_rect()
            self.boundRect.center = self.pos
            surface.blit(self.boundSf, self.boundRect)

    def getEnemy(self, enemyGroup):
        for e in enemyGroup:
            dis = getDistance(self, e)
            if dis < self.bound and e not in self.enemyQueue:
                self.enemyQueue.append(e)
            if e in self.enemyQueue:
                if dis >= self.bound or e.HP == 0:
                    self.enemyQueue.remove(e)

    def resort(self):
        first = self.enemyQueue[0]
        for i in range(0, len(self.enemyQueue)):
            dis = getDistance(first, self.enemyQueue[i])
            if dis == 0 and i != self.enemyQueue.index(first):
                self.enemyQueue.insert(0, self.enemyQueue[i])
                self.enemyQueue.pop(i)

    def attack(self, enemyGroup):
        self.getEnemy(enemyGroup)

        if self.enemyQueue:
            self.resort()
            for t in self.enemyQueue:
                print(t.HP, t.type)
            print("end")
            target = self.enemyQueue[0]

            x = self.pos[0] - target.pos[0]
            y = self.pos[1] - target.pos[1]

            if pg.time.get_ticks() - self.timeStart > self.speed*1000:
                print(target.HP, target.type)
                self.angle = math.degrees(math.atan2(-y, x)) + 90
                self.timeStart = pg.time.get_ticks()
                if self.atk >= target.HP:
                    target.HP = 0
                    i = self.enemyQueue.index(target)
                    self.enemyQueue.pop(i)
                else:
                    target.HP -= self.atk


def getDistance(a, b):
    x = b.pos[0] - a.pos[0]
    y = b.pos[1] - a.pos[1]
    return math.sqrt(x*x + y*y)

