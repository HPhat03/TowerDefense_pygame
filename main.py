import pygame
from scenes import Scenes
from scenes.game import Game
from scenes.menu import Menu
from setting import *
import ModelList
from Player import Player
pygame.init()


clock = pygame.time.Clock()
def main():
    ModelList.ConnectDatabase()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Towe Defense 2D")
    icon = pygame.image.load('Assets/icon.jpg').convert_alpha()
    pygame.display.set_icon(icon

                            )
    scene = Scenes.MENU
    login = Player()

    while True:
        match scene:
            case Scenes.MENU:
                scene = Menu.run(screen, login)
            case Scenes.GAME:
                scene = Game.run(screen, login)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
