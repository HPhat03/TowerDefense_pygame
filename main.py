import pygame
from scenes import Scenes
from scenes.game import Game
from scenes.menu import Menu

pygame.init()


def main():
    screen = pygame.display.set_mode((1280, 720))
    scene = Scenes.MENU

    while True:
        match scene:
            case Scenes.MENU:
                scene = Menu.run(screen)
            case Scenes.GAME:
                scene = Game.run(screen)


if __name__ == "__main__":
    main()
