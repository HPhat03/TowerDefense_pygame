import pygame as pg

from .core import Scene, Scenes
from src.controls import Button, Label, ItemBox, PictureBox, ControlsContainer
from src.setting import WINDOW_WIDTH, WINDOW_HEIGHT, button_color
from src.gamePlay import Record
from .play import Play
from src import Maps


class GameMode:
    EASY = 0
    MEDIUM = 1


class Game(Scene):

    EzBg = pg.image.load("src/assets/EasyLevelBG.png")
    MdBg = pg.image.load("src/assets/MediumLevelBG.png")
    background = EzBg

    Backpic = PictureBox(20, 20, 100, 50, "src/assets/Logo.png")
    EzBt = Button(20, 250, 150, 50, "EASY", 10, (112, 187, 68), "white")
    MdBt = Button(20, 320, 150, 50, "MEDIUM", 10, (183, 51, 62), "white")
    PlayBt = Button(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 60,
                    100, 50, "Play", 20, (112, 187, 68), "white")
    isEnabled = True
    LvLabel = Label(20, 180, 100, 50, "MODE:")

    teamTowers = []
    padding = 5
    for c in range(0, 5):
        box = ItemBox((c+1)*2*padding + c*100, 2 * padding,
                      100, "src/assets/MediumLevelBG.png", "NONE", "")
        teamTowers.append(box)
    container = ControlsContainer(350, 100, teamTowers, padding, "grey")

    Map_Loader = PictureBox(350, container.rect.top + 200,
                            container.rect.width, 300, "")
    nextBt = Button(Map_Loader.rect.left + Map_Loader.rect.width/2 + 175,
                    Map_Loader.rect.top + Map_Loader.rect.height + 10,
                    50, 50, ">", 25, button_color, "white")

    preBt = Button(Map_Loader.rect.left + Map_Loader.rect.width/2 - 225,
                   Map_Loader.rect.top + Map_Loader.rect.height + 10,
                   50, 50, "<", 25, button_color, "white")
    MapNameLb = Label(preBt.rect.right, nextBt.rect.top,
                      nextBt.rect.left - preBt.rect.right, 50,
                      text="", bgcolor="white")
    controls = pg.sprite.Group()
    map_index = 0

    panel = pg.Rect(container.rect.left - 25, container.rect.top - 10,
                    container.rect.width + 50, nextBt.rect.bottom - 80)
    panel_color = EzBt.background_color
    controls.add(Backpic, LvLabel, EzBt, MdBt, PlayBt, container,
                 Map_Loader, nextBt, preBt, MapNameLb)

    # other
    mode = GameMode.EASY

    @staticmethod
    def event_handler(event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        Game.background = pg.transform.scale(
            Game.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # Get list of tower set in player's team
        for t in range(5):
            if t < len(login.team):
                Game.teamTowers[t].pictureBox.img_path = login.team[t].img_src
                Game.teamTowers[t].mainText.text = login.team[t].name
                Game.teamTowers[t].subText.text = f"${login.team[t].in_game_price}"
            else:
                Game.teamTowers[t].pictureBox.img_path = "src/assets/MediumLevelBG.png"
                Game.teamTowers[t].mainText.text = "NONE"
                Game.teamTowers[t].subText.text = ""
        # Get map loaded on map_loader
        cur_map = Maps[Game.map_index]
        Game.Map_Loader.img_path = cur_map.img_path
        Game.MapNameLb.text = cur_map.name

        # Drawing session
        screen.blit(Game.background, (0, 0))
        pg.draw.rect(screen, color=Game.panel_color, rect=Game.panel,
                     border_radius=15)
        for c in Game.controls:
            c.draw(screen)

        # clicked events
        for s in Game.teamTowers:
            if s.isClicked():
                return Scenes.INVENTORY
        if Game.nextBt.isClicked():
            if Game.map_index < len(Maps)-1:
                Game.map_index += 1
        if Game.preBt.isClicked():
            if Game.map_index > 0:
                Game.map_index -= 1
        if Game.Backpic.isClicked():
            return Scenes.MENU
        if Game.EzBt.isClicked():
            Game.background = Game.EzBg
            Game.panel_color = Game.EzBt.background_color
            Game.isEnabled = True
            Game.mode = GameMode.EASY
        if Game.MdBt.isClicked():
            Game.background = Game.MdBg
            Game.panel_color = Game.MdBt.background_color
            Game.mode = GameMode.MEDIUM
            Game.isEnabled = False
        if not Game.isEnabled:
            Game.PlayBt.background_color = "grey"
            Game.PlayBt.text = "COMMING SOON"
        else:
            Game.PlayBt.background_color = button_color
            Game.PlayBt.text = "Play"

        Game.PlayBt.rect.width = Game.PlayBt.text_rect.width + 20
        Game.PlayBt.rect.left = WINDOW_WIDTH - \
            Game.PlayBt.rect.width - 20

        if Game.PlayBt.isClicked() and Game.isEnabled:
            record = Record(Game.mode, cur_map, login)
            Play.reset(record)
            return Scenes.PLAY
        return None
