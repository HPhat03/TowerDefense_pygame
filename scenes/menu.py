import pygame

import setting
from scenes import Scene, Scenes
from Controls import Button, PictureBox


class Menu(Scene):
    background = pygame.image.load("Assets/bgMenu.png")
    PlayButton = Button(175, 300, 200, 50, "Play", color=(42,186,103))
    LogoImage = PictureBox(100, 50, 360, 250, "Assets/Logo.png")
    @staticmethod
    def event_handler(event):
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen):
        Menu.background = pygame.transform.scale(Menu.background,(setting.WINDOW_WIDTH,setting.WINDOW_HEIGHT))
        screen.blit(Menu.background,(0,0))
        Menu.PlayButton.draw(screen)
        if Menu.PlayButton.isClicked():
            print("clicked")
            Menu.PlayButton.bgcolor = (213,70,55)
            Menu.PlayButton.color = "white"
        elif Menu.PlayButton.isHovering():
            Menu.PlayButton.bgcolor = (42,186,103)
            Menu.PlayButton.color = "white"
        elif not Menu.PlayButton.rect.collidepoint(pygame.mouse.get_pos()):
            Menu.PlayButton.bgcolor = "white"
            Menu.PlayButton.color = (42,186,103)
        Menu.LogoImage.draw(screen)
