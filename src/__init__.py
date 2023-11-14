import pygame

from .scenes import Scenes
from .scenes.game import Game
from .scenes.menu import Menu

pygame.init()
clock = pygame.time.Clock()


def main():
    from .setting import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    scene = Scenes.MENU

    while True:
        clock.tick(FPS)
        match scene:
            case Scenes.MENU:
                scene = Menu.run(screen)
            case Scenes.GAME:
                scene = Game.run(screen)
            case Scenes.SHOP:
                scene = Game.run(screen)
            case Scenes.INVENTORY:
                scene = Game.run(screen)
