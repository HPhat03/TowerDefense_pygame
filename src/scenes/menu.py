import pygame

from src import setting, db
from . import Scene, Scenes
from src.controls import Button, PictureBox, TextBox, Label


class Menu(Scene):
    background = pygame.image.load("src/assets/bgMenu.png")
    
    PlayButton = Button(175, 300, 200, 50, "Play", color=setting.button_color)
    ShopButton = Button(PlayButton.rect.left, PlayButton.rect.top+PlayButton.rect.height+25, PlayButton.rect.width, PlayButton.rect.height, "Shop", color=setting.button_color)
    InventoryButton = Button(ShopButton.rect.left, ShopButton.rect.top+ShopButton.rect.height+25, ShopButton.rect.width, ShopButton.rect.height, "Inventory", color=setting.button_color)
    QuitButton = Button(InventoryButton.rect.left, InventoryButton.rect.top+InventoryButton.rect.height+25, InventoryButton.rect.width, InventoryButton.rect.height, "Quit", color=setting.button_color)
    
    LogoImage = PictureBox(100, 50, 360, 250, "src/assets/Logo.png")
    NameTextbox = TextBox(setting.WINDOW_WIDTH - 320, 20, 300, 50)
    NotiLabel = Label(NameTextbox.rect.left,NameTextbox.rect.top+NameTextbox.rect.height+10,NameTextbox.rect.width,NameTextbox.rect.height,text='',color= "red")
    
    controls = pygame.sprite.Group()
    controls.add(PlayButton, LogoImage, ShopButton, InventoryButton, \
                 QuitButton, NameTextbox, NotiLabel)

    @staticmethod
    def event_handler(event, login):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen, login):
        Menu.background = pygame.transform.scale(Menu.background, (setting.WINDOW_WIDTH, setting.WINDOW_HEIGHT))
        screen.blit(Menu.background, (0, 0))
        for c in Menu.controls:
            c.draw(screen)
            c.displayEffect()
        
        login.authenticate(Menu.NameTextbox.text)

        if Menu.PlayButton.isClicked():
            return Scenes.GAME

        if Menu.QuitButton.isClicked():
            db.close()
            quit()

        if login.isAuth:
            Menu.NotiLabel.text = f"Welcome {login.name}"
            Menu.NotiLabel.color = "yellow"
            Menu.NotiLabel.bgcolor= "black"

            if Menu.ShopButton.isClicked():
                return Scenes.SHOP

            if Menu.InventoryButton.isClicked():
                return Scenes.INVENTORY
        else:
            Menu.NotiLabel.text = f"USER IS NOT FOUND"
            Menu.NotiLabel.color = "red"
            Menu.NotiLabel.bgcolor = None
        return None
