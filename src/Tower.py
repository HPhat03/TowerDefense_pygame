import pygame as pg
from src import db
class Tower(pg.sprite.Sprite):
    def __init__(self, id):
        pg.sprite.Sprite.__init__(self)
        self.getTowerbyID(id)
    def getTowerbyID(self, id):
        tower = db.select("Select * from Tower where id = ?", (id, ))[0]
        self.id = id
        self.name = tower[1]
        self.img_src = tower[2]
        self.in_shop_price = tower[3]
        self.in_game_price = tower[4]
