import pygame
from abc import abstractmethod


class Scenes:
    MENU = 1
    GAME = 2


class Scene:
    @staticmethod
    @abstractmethod
    def event_handler(event):
        pass

    @staticmethod
    @abstractmethod
    def game(screen):
        pass

    @classmethod
    def run(cls, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.mod & pygame.KMOD_CTRL and \
                            (event.key == pygame.K_w or
                                event.key == pygame.K_q):
                        pygame.quit()
                    else:
                        if (tmp := cls.event_handler(event)) is not None:
                            return tmp
            cls.game(screen)
            pygame.display.update()

