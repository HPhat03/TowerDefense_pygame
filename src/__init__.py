import pygame
from .utils.database import Database
import os
from .Map import Map

pygame.init()
clock = pygame.time.Clock()
db = Database()

Maps = []
for map in db.select("SELECT * FROM Map"):
    mapItem = Map(map)
    Maps.append(mapItem)


def main():
    from .setting import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
    from .player import Player
    from .scenes import Scenes, Game, Menu, Shop, Inventory, Play
    from .Tower import Tower
    scene = Scenes.MENU

    pygame.display.set_caption("Tower Defense 2D")
    icon = pygame.image.load('src/assets/icon.jpg')
    pygame.display.set_icon(icon)
    login = Player()
    while True:
        clock.tick(FPS)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
        match scene:
            case Scenes.MENU:
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                scene = Menu.run(screen, login)
            case Scenes.GAME:
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                scene = Game.run(screen, login)
            case Scenes.SHOP:
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                scene = Shop.run(screen, login)
            case Scenes.INVENTORY:
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                scene = Inventory.run(screen, login)
            case Scenes.PLAY:
                screen = pygame.display.set_mode((WINDOW_WIDTH + 300,
                                                  WINDOW_HEIGHT + 180))
                scene = Play.run(screen, login)
