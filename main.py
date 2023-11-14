import pygame
from scenes import Scenes
from scenes.game import Game
from scenes.menu import Menu
from setting import *
import ModelList
pygame.init()


clock = pygame.time.Clock()
def main():
    ModelList.ConnectDatabase()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    scene = Scenes.MENU

    while True:
        match scene:
            case Scenes.MENU:
                scene = Menu.run(screen)
            case Scenes.GAME:
                scene = Game.run(screen)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
