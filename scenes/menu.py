import pygame

import setting
from scenes import Scene, Scenes
from Controls import Button, PictureBox, TextBox


class Menu(Scene):
    background = pygame.image.load("assets/bgMenu.png")
    PlayButton = Button(175, 300, 200, 50, "Play", color=setting.button_color)
    ShopButton= Button(PlayButton.rect.left, PlayButton.rect.top+PlayButton.rect.height+25, PlayButton.rect.width,PlayButton.rect.height, "Shop", color=setting.button_color)
    InventoryButton= Button(ShopButton.rect.left, ShopButton.rect.top+ShopButton.rect.height+25, ShopButton.rect.width,ShopButton.rect.height, "Inventory", color=setting.button_color)
    LogoImage = PictureBox(100, 50, 360, 250, "assets/Logo.png")
    NameTextbox = TextBox(setting.WINDOW_WIDTH-320,20,300,50)
    controls = pygame.sprite.Group()
    controls.add(PlayButton,LogoImage,ShopButton,InventoryButton, NameTextbox)
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
        for c in Menu.controls:
            c.draw(screen)
        # Menu.PlayButton.draw(screen)
        # Menu.LogoImage.draw(screen)
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

