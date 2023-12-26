import pygame as pg
import hashlib

from .core import Scene, Scenes
from src.controls import Label, TextBox, Button
from src.setting import WINDOW_WIDTH, WINDOW_HEIGHT
from  src import db

class LogPage(Scene):
    background = pg.transform.scale(pg.image.load("src/assets/EasyLevelBG.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
    LogLabel = Label(WINDOW_WIDTH/2-150, WINDOW_HEIGHT/2-150, 300, 50, "Register / Login", color="white")
    uLb = Label(LogLabel.rect.left, LogLabel.rect.top + LogLabel.rect.height, 100, 50, "username:")
    username = TextBox(LogLabel.rect.left, LogLabel.rect.top + LogLabel.rect.height + 50,
                       300, 50,10)
    pwLb = Label(username.rect.left, username.rect.top + username.rect.height, 100, 50, "password:")
    password = TextBox(LogLabel.rect.left, username.rect.top + username.rect.height + 50,
                       300, 50,10)
    LoginBtn = Button(LogLabel.rect.left + 30, password.rect.top + password.rect.height+50, 100, 50, "LOGIN", bgcolor="green", color="white")
    ResgBtn = Button(LoginBtn.rect.left + LoginBtn.rect.width + 10, LoginBtn.rect.top, 150, 50, "REGISTER", bgcolor="red", color="white" )
    Controls = pg.sprite.Group()
    Controls.add(LogLabel, LoginBtn, ResgBtn, uLb, pwLb, username, password)
    @staticmethod
    def event_handler(event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen, login):
        #DRAWING SECTION
        screen.blit(LogPage.background, (0,0))
        for c in LogPage.Controls:
            c.draw(screen)

        #CHECKING
        username = LogPage.username.text
        password = LogPage.password.text
        if username != "" and password != "":
            enc_password = hashlib.md5(str(password).encode("utf-8")).hexdigest()
            if LogPage.LoginBtn.isClicked():
                login.authenticate(username, enc_password)
                if login.isAuth:
                    return Scenes.MENU
            if LogPage.ResgBtn.isClicked():
                db.execute("INSERT INTO Player(name, password, coins, active) VALUES(?, ?, 0, 1)", (username, enc_password))
                id = db.select("SELECT id FROM Player WHERE name = ?", (username, ))[0]
                print(id)
                db.execute("INSERT INTO Player_Towers(idPlayer, idTower) VALUES(?, 1)", id)
                db.execute("INSERT INTO Player_Towers(idPlayer, idTower) VALUES(?, 2)", id)
                db.execute("INSERT INTO Player_Team(idPlayer) VALUES(?)", id)
                login.authenticate(username, enc_password)
                if login.isAuth:
                    return Scenes.MENU