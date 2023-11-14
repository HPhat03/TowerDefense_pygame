import pygame

from src import setting
from . import Scene, Scenes
from src.controls import Button, PictureBox, TextBox


class Menu(Scene):
    background = pygame.image.load("src/assets/bgMenu.png")
    PlayButton = Button(175, 300, 200, 50, "Play", color=setting.button_color)
    ShopButton = Button(PlayButton.rect.left, PlayButton.rect.top+PlayButton.rect.height+25, PlayButton.rect.width, PlayButton.rect.height, "Shop", color=setting.button_color)
    InventoryButton = Button(ShopButton.rect.left, ShopButton.rect.top+ShopButton.rect.height+25, ShopButton.rect.width, ShopButton.rect.height, "Inventory", color=setting.button_color)
    QuitButton = Button(InventoryButton.rect.left, InventoryButton.rect.top+InventoryButton.rect.height+25, InventoryButton.rect.width, InventoryButton.rect.height, "Quit", color=setting.button_color)
    LogoImage = PictureBox(100, 50, 360, 250, "src/assets/Logo.png")
    NameTextbox = TextBox(setting.WINDOW_WIDTH - 320, 20, 300, 50)
    
    controls = pygame.sprite.Group()
    controls.add(PlayButton, LogoImage, ShopButton, InventoryButton, QuitButton, NameTextbox)

    @staticmethod
    def event_handler(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen):
        Menu.background = pygame.transform.scale(Menu.background, (setting.WINDOW_WIDTH, setting.WINDOW_HEIGHT))
        screen.blit(Menu.background, (0, 0))
        for c in Menu.controls: c.draw(screen)

        #
        if Menu.PlayButton.isClicked():
            Menu.PlayButton.bgcolor = (213, 70, 55)
            Menu.PlayButton.color = "white"
            return Scenes.GAME

        #
        if Menu.ShopButton.isClicked():
            Menu.ShopButton.bgcolor = (213, 70, 55)
            Menu.ShopButton.color = "white"
            return Scenes.SHOP

        #
        if Menu.InventoryButton.isClicked():
            Menu.InventoryButton.bgcolor = (213, 70, 55)
            Menu.InventoryButton.color = "white"
            return Scenes.INVENTORY

        #
        if Menu.QuitButton.isClicked():
            Menu.QuitButton.bgcolor = (213, 70, 55)
            Menu.QuitButton.color = "white"
            quit()
        
        return None

