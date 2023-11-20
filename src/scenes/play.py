from typing import Any
import pygame as pg

from .core import Scene, Scenes
from src.controls import Button, Label, ItemBox, PictureBox, ControlsContainer
from src import setting


class Play(Scene):

    recording: Any = None
    count = Label(setting.WINDOW_WIDTH, 100, 100, 100, "")

    teamTowers = []
    padding = 17
    width = 100
    count = 0
    for i in range(3):
        for c in range(2):
            if count < 5:
                box = ItemBox((c + 1) * 2 * padding + c * width,
                              (i+1) * padding + i * (width+2*padding),
                              100, "src/assets/MediumLevelBG.png", "NONE", "")
                teamTowers.append(box)
                count += 1
    sellingBT = Button(4*padding+width, 3*padding+2*(width+4*padding), width,
                       50, "SELL", 20, setting.button_color, "white")
    teamTowers.append(sellingBT)
    container = ControlsContainer(setting.WINDOW_WIDTH, 0, teamTowers,
                                  padding=padding, bgcolor=(113, 112, 113))

    UGPs = pg.sprite.Group()
    UGLb = Label(30, 10, 50, 50, "UPGRADE", color="white", size=20)
    UGPbx= PictureBox(UGLb.rect.left, UGLb.rect.top + UGLb.rect.height, 100, 100,
                      "src/assets/MediumLevelBG.png")
    UGBT = Button(UGPbx.rect.width + UGPbx.rect.left + 10,
                  UGLb.rect.top + UGLb.rect.height + 40,
                  150, 50, "upgrade", 20, (255, 237, 41), "white")
    UGPrice = Label(UGPbx.rect.width + UGPbx.rect.left + 10, UGLb.rect.top+UGLb.rect.height , 150, 50, "$200", color="yellow")
    UGPs.add(UGPbx, UGLb, UGBT, UGPrice)
    upgradePanel = ControlsContainer(setting.WINDOW_WIDTH, container.rect.height, UGPs, 10, (113, 112, 113))

    statePs = pg.sprite.Group()
    waveLabel = Label(10, 60, 150, 50, "Wave 0", color="white")
    MaxHPBar = Label(10, 10, setting.WINDOW_WIDTH-30, 50, "", "red", border_radius=10)
    CurHPBar = Label(10, 10, setting.WINDOW_WIDTH - 30, 50, "", "green", border_radius=10)
    statePs.add(MaxHPBar, waveLabel, CurHPBar)
    statePanel = ControlsContainer(0, setting.WINDOW_HEIGHT, statePs, 10, (113, 112, 113))
    BudgetLabel = Label(setting.WINDOW_WIDTH+50, setting.WINDOW_HEIGHT+10, 200, 100, f"$0", color="white", size=40)
    panels = pg.sprite.Group()
    panels.add(container, upgradePanel, BudgetLabel, statePanel)

    @staticmethod
    def event_handler(event, login):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen, login):
        screen.fill("black")
        Play.recording.loadMap(screen)
        for c in Play.panels:
            c.draw(screen)
        return None
