import pygame
from .utils.database import Database


pygame.init()
clock = pygame.time.Clock()
db = Database()


def main():
    from .setting import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
    from .player import Player
    from .scenes import Scenes, Game, Menu, Shop, Inventory

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    scene = Scenes.MENU

    pygame.display.set_caption("Towe Defense 2D")
    icon = pygame.image.load('src/assets/icon.jpg').convert_alpha()
    pygame.display.set_icon(icon)
    login = Player()

    while True:
        clock.tick(FPS)
        match scene:
            case Scenes.MENU:
                scene = Menu.run(screen, login)
            case Scenes.GAME:
                scene = Game.run(screen, login)
            case Scenes.SHOP:
                scene = Shop.run(screen, login)
            case Scenes.INVENTORY:
                scene = Inventory.run(screen, login)
