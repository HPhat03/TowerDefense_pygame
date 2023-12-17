import pygame as pg
from pygame.math import Vector2
from src import db
import math
from src.data.EnemyConfig import ENEMY_TYPES


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoint):

        pg.sprite.Sprite.__init__(self)

        # print(ENEMY_TYPES[enemy_type]
        Enemy = db.select("SELECT * FROM ENEMY WHERE id = ?",
                          (ENEMY_TYPES[enemy_type], ))

        for type in Enemy:
            if type[1] == enemy_type:
                # print(type)
                self.type = type[1]
                self.img_src = type[2]
                self.HP = type[3]
                self.speed = type[4]
                self.price = type[5]
            else:
                return

        # position init
        self.originalImage = pg.image.load(self.img_src)
        self.angle = 0
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()

        # HP BAR
        self.curHPBar = pg.Rect(self.rect.left, self.rect.top - 50,
                                self.rect.width, 50)
        self.maxHPBar = self.curHPBar.copy()

        # waypoint init
        self.waypoint = waypoint
        self.waypointIndex = 0
        self.pos = Vector2(self.waypoint[0])

        # other init
        self.maxHP = self.HP
        self.rect.center = self.pos
        self.attack = False
        self.awarded = False

    def move(self):
        if (self.waypointIndex < len(self.waypoint)):
            self.target_destination = Vector2(self.waypoint[self.waypointIndex])
            # d = (xB-xA, yB-yA)
            self.distance = self.target_destination - self.pos
        else:
            if self.attack:
                self.kill()
            self.attack = True
        d = self.distance.length()  # tra ve do dai d^2= x^2 + y^2
        if (d > self.speed):
            self.pos += self.distance.normalize() * self.speed
        else:
            if d != 0:
                self.pos += self.distance.normalize() * d
            self.waypointIndex += 1
        self.rect.center = self.pos

    def rotate(self):
        self.distance = self.target_destination - self.pos
        self.angle = math.degrees(
            math.atan2(-self.distance[1], self.distance[0]))
        # rotate update
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, *args, **kwargs):
        if self.HP <= 0:
            if self.awarded:
                self.kill()
                return
            self.awarded = True
        self.move()
        self.rotate()

    def draw(self, surface):
        self.maxHPBar.update(self.rect.left + 10, self.rect.top + 17,
                             self.rect.width - 20, 5)
        self.curHPBar.update(self.rect.left + 10, self.rect.top + 17,
                             self.HP/self.maxHP * self.maxHPBar.width, 5)
        pg.draw.rect(surface, "red", self.maxHPBar)
        pg.draw.rect(surface, "green", self.curHPBar)
        surface.blit(self.image, self.rect)
