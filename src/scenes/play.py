from typing import Any
import pygame as pg

from .core import Scene, Scenes
from src.controls import Button, Label, ItemBox, PictureBox, ControlsContainer
from src import setting
from src.Tower import *
from src.Enemy import Enemy
from src.data.EnemyConfig import WAVE_STAT


class Play(Scene):
    recording: Any = None
    count = Label(setting.WINDOW_WIDTH, 100, 100, 100, "")

    # TOWERS PANEL
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
    # teamTowers.append(sellingBT)
    container = ControlsContainer(setting.WINDOW_WIDTH - setting.RIGHT_BAR, 0,
                                  teamTowers, padding=padding,
                                  bgcolor=(113, 112, 113))
    sellingBT = Button(4 * padding + width + container.rect.left,
                       3 * padding + 2 * (width + 4 * padding), width,
                       50, "SELL", 20, setting.button_color, "white")

    # UPGRADE PANEL
    UGPs = pg.sprite.Group()
    UGLb = Label(30, 10, 50, 50, "UPGRADE", color="white", size=20)
    UGPbx = PictureBox(UGLb.rect.left, UGLb.rect.top + UGLb.rect.height, 100,
                       100, "src/assets/MediumLevelBG.png")
    UGBT = Button(UGPbx.rect.width + UGPbx.rect.left + 10,
                  UGLb.rect.top + UGLb.rect.height + 40,
                  150, 50, "upgrade", 20, (255, 237, 41), "white")
    UGPrice = Label(UGPbx.rect.width + UGPbx.rect.left + 10,
                    UGLb.rect.top + UGLb.rect.height, 150, 50,
                    "$0", color="yellow")
    UGPs.add(UGPbx, UGLb, UGBT, UGPrice)
    upgradePanel = ControlsContainer(setting.WINDOW_WIDTH - setting.RIGHT_BAR,
                                     container.rect.height, UGPs,
                                     10, (113, 112, 113))

    # STATE PANEL
    statePs = pg.sprite.Group()
    waveLabel = Label(10, 60, 150, 50, "Wave 0", color="white")
    MaxHPBar = Label(10, 10, setting.WINDOW_WIDTH - 30 - setting.RIGHT_BAR, 50,
                     "", "red", border_radius=10)
    CurHPBar = Label(10, 10, setting.WINDOW_WIDTH - 30 - setting.RIGHT_BAR, 50,
                     "", "green", border_radius=10)
    statePs.add(MaxHPBar, waveLabel, CurHPBar)
    statePanel = ControlsContainer(0, setting.WINDOW_HEIGHT - setting.BOT_BAR,
                                   statePs, 10, (113, 112, 113))

    # BUDGET
    BudgetLabel = Label(setting.WINDOW_WIDTH + 50 - setting.RIGHT_BAR,
                        setting.WINDOW_HEIGHT + 10 - setting.BOT_BAR,
                        200, 100, "$0", color="white", size=40)

    # END
    EndLb = Label(175, 100, 600, 200, "YOU'RE LOST!", bgcolor="black",
                  color="red", size=90)
    BackBtn = Button(EndLb.rect.left + EndLb.rect.width / 4 + 50,
                     EndLb.rect.top + EndLb.rect.height + 50, 200, 50,
                     "Back to home", 10, "red", "white")
    endPanel = [EndLb, BackBtn]

    # Controls group
    panels = pg.sprite.Group()
    panels.add(container, sellingBT, upgradePanel, BudgetLabel, statePanel)

    # Flags
    isPlacing = False
    isDeleting = False
    isClicked = False
    al = False

    # Other
    towerSpawning = None
    towerUpdating = None
    time_goal, spawned = 0, 0
    spawner = pg.sprite.Group()

    @staticmethod
    def event_handler(event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen, login):
        screen.fill("black")

        # draw session
        Play.recording.loadMap(screen)
        Play.recording.LoadTowers(Play.teamTowers)
        for tower in Play.recording.towerGroup:
            tower.draw(screen)
        for c in Play.panels:
            c.draw(screen)
        for e in Play.spawner:
            e.update()
            e.draw(screen)

        # update session
        Play.BudgetLabel.text = f"${Play.recording.budget}"
        Play.CurHPBar.rect.width = Play.recording.HP / 100 * \
            Play.MaxHPBar.rect.width
        Play.waveLabel.text = f"Wave {Play.recording.curWave}"
        for e in Play.spawner:
            if e.attack:
                Play.recording.HP -= e.HP
            if e.awarded:
                Play.recording.budget += e.price

        Play.CurHPBar.rect.width = Play.recording.HP / 100 * \
            Play.MaxHPBar.rect.width

        if Play.recording.HP <= 0 or Play.recording.curWave > len(WAVE_STAT[Play.recording.mode]):
            if Play.recording.HP <= 0:
                Play.EndLb.text = "YOU'RE LOST!"
                Play.EndLb.color = "red"
            else:
                Play.EndLb.text = "YOU'RE WON"
                Play.EndLb.color = "green"
            for e in Play.spawner:
                e.kill()
            for c in Play.endPanel:
                c.draw(screen)
            if Play.BackBtn.isClicked():
                login.coins += Play.recording.curWave * 10
                return Scenes.MENU
        else:
            if pg.time.get_ticks() - Play.time_goal > setting.spawn_cooldown:
                if Play.spawned < len(Play.recording.enemyGroup):
                    e1 = Enemy(str(Play.recording.enemyGroup[Play.spawned]),
                               Play.recording.map.waypoints)
                    Play.spawner.add(e1)
                    Play.spawned += 1
                    Play.time_goal = pg.time.get_ticks()
                if len(Play.spawner) == 0 or Play.waveLabel.isClicked():
                    Play.recording.curWave += 1
                    Play.recording.budget += (Play.recording.curWave - 1) * 75
                    Play.recording.process_enemies()

            mousePos = pg.mouse.get_pos()
            tile_x = mousePos[0] // setting.MAP_TILE_SIZE
            tile_y = mousePos[1] // setting.MAP_TILE_SIZE

            # Placing Tower event
            for c in Play.teamTowers:
                if c.item is None:
                    continue

                credentials = (
                    c.isClicked(),
                    not Play.isPlacing, not Play.isDeleting,
                    c.item.in_game_price <= Play.recording.budget
                )
                if all(credentials):
                    Play.isPlacing = True
                    Play.towerSpawning = c.item

            if Play.isPlacing:
                if mousePos[0] < setting.WINDOW_WIDTH - setting.RIGHT_BAR and \
                        mousePos[1] <= setting.WINDOW_HEIGHT - setting.BOT_BAR:
                    rect = pg.Rect(tile_x * setting.MAP_TILE_SIZE,
                                   tile_y * setting.MAP_TILE_SIZE,
                                   setting.MAP_TILE_SIZE,
                                   setting.MAP_TILE_SIZE)
                    screen.blit(Play.towerSpawning.OriginalImage, rect)
                    pg.draw.rect(screen, "blue" if Play.towerSpawning.isPlaceable(Play.recording, tile_x, tile_y) else "red", rect, width=2)

                    # MOUSE CLICKED TO PLACE
                    if pg.mouse.get_pressed()[0] == 1 and \
                            len(Play.recording.towerGroup) < 20:
                        if Play.towerSpawning.isPlaceable(Play.recording, tile_x, tile_y):
                            tower = NormalScout(Play.towerSpawning.id,
                                                tile_x, tile_y)
                            Play.recording.budget -= Play.towerSpawning.in_game_price
                            Play.recording.towerGroup.append(tower)
                            Play.isPlacing = False

                # Make a Cancel Button without creating new button
                Play.sellingBT.text = "CANCEL"
                Play.sellingBT.background_color = "red"
                if Play.sellingBT.isClicked():
                    Play.isPlacing = False
            else:
                Play.sellingBT.text = "SELL"
                Play.sellingBT.background_color = setting.button_color

            # Selling tower and pick tower to upgrade
            if Play.sellingBT.isClicked() and not Play.isPlacing:
                Play.isDeleting = not Play.isDeleting

            if pg.mouse.get_pressed()[0] == 1 and not Play.isClicked:
                Play.isClicked = True
                if mousePos[0] < setting.WINDOW_WIDTH - setting.RIGHT_BAR and \
                        mousePos[1] <= setting.WINDOW_HEIGHT - setting.BOT_BAR:
                    Play.towerUpdating = None

                for i in range(len(Play.recording.towerGroup)):
                    if Play.recording.towerGroup[i]:
                        t = Play.recording.towerGroup[i]
                        if t.tile_x == tile_x and t.tile_y == tile_y:
                            if Play.isDeleting:
                                Play.recording.budget += int(0.7 * t.level * t.in_game_price)
                                Play.recording.towerGroup.pop(i)
                                break
                            if not Play.isPlacing:
                                Play.UGPbx.img_path = t.img_src
                                Play.UGPrice.text = f"${t.levelUp}"
                                Play.towerUpdating = t
            if pg.mouse.get_pressed()[0] == 0:
                Play.isClicked = False

            if Play.isDeleting:
                Play.sellingBT.background_color = (255, 218, 3)
                Play.sellingBT.text = "SELLING"

            if len(Play.recording.towerGroup) == 0:
                Play.towerUpdating = None

            # show the the bound
            for t in Play.recording.towerGroup:
                t.isFocus = False
            if Play.towerUpdating is not None:
                Play.towerUpdating.isFocus = True

            # Tower attacking
            for t in Play.recording.towerGroup:
                t.attack(Play.spawner)

            if Play.towerUpdating is None:
                Play.UGPbx.img_path = "src/assets/EasyLevelBG.png"
                Play.UGPrice.text = "$$$"
            elif Play.towerUpdating.levelUp == "MAX":
                Play.UGPrice.text = "LV. MAX"
            elif Play.UGBT.isClicked() and \
                    Play.recording.budget >= int(Play.towerUpdating.levelUp):
                Play.recording.budget -= Play.towerUpdating.levelUp
                Play.towerUpdating.updateTower()
                Play.UGPrice.text = f"${Play.towerUpdating.levelUp}"
        return None

    @staticmethod
    def reset(record):
        Play.time_goal = pg.time.get_ticks()
        Play.recording = record
        Play.spawned = 0
        Play.spawner = pg.sprite.Group()
        Play.recording.process_enemies()
