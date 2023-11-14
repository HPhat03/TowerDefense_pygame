import pygame
from . import Scene, Scenes


class Game(Scene):
    @staticmethod
    def event_handler(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen):
        screen.fill("red")
        return None
