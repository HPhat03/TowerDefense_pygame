import pygame
from . import Scene, Scenes


class Menu(Scene):
    @staticmethod
    def event_handler(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen):
        screen.fill("green")
