import pygame
from abc import abstractmethod

from src import db


class Scenes:
    MENU = 1
    GAME = 2
    SHOP = 3
    INVENTORY = 4


class Scene:
    @staticmethod
    @abstractmethod
    def event_handler(event, login):
        pass

    @staticmethod
    @abstractmethod
    def game(screen, login):
        pass

    @classmethod
    def run(cls, screen, login):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    db.close()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.mod & pygame.KMOD_CTRL and \
                            (event.key == pygame.K_w or
                                event.key == pygame.K_q):
                        db.close()
                        quit()
                    else:
                        if (t := cls.event_handler(event, login)) is not None:
                            return t

            if (t := cls.game(screen, login)) is not None:
                return t
            pygame.display.update()
