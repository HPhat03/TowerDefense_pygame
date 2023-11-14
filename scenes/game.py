import pygame
from scenes import Scene, Scenes


class Game(Scene):
    @staticmethod
    def event_handler(event,login):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and login.isAuth:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        screen.fill("red")
