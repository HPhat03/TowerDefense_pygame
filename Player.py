import pygame as pg

import ModelList


class Player:
    def __init__(self):
        self.name = None
        self.password = None
        self.coins = 0
        self.active = False
        self.isAuth= False

    def authenticate(self, name):
        for us in ModelList.Player_List:
            if us[0] == name:
                self.isAuth = True
                self.name = us[0]
                self.password = us[1]
                self.coins = us[2]
                self.active = True if us[3] == 1 else False
                return
            else:
                self.isAuth=False
                self.name = None
                self.password = None
                self.coins = 0
                self.active = False
