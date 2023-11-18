import pygame
from .core import Scene, Scenes


class Inventory(Scene):
    @staticmethod
    def event_handler(event, login):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and login.isAuth:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        screen.fill("red")
        return None
