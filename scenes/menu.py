import pygame

import setting
from scenes import Scene, Scenes
from Controls import Button, PictureBox, TextBox, Label
from Player import Player


class Menu(Scene):
    background = pygame.image.load("Assets/bgMenu.png")


    PlayButton = Button(175, 300, 200, 50, "Play", color=setting.button_color)
    ShopButton= Button(PlayButton.rect.left, PlayButton.rect.top+PlayButton.rect.height+25, PlayButton.rect.width,PlayButton.rect.height, "Shop", color=setting.button_color)
    InventoryButton= Button(ShopButton.rect.left, ShopButton.rect.top+ShopButton.rect.height+25, ShopButton.rect.width,ShopButton.rect.height, "Inventory", color=setting.button_color)
    LogoImage = PictureBox(100, 50, 360, 250, "Assets/Logo.png")
    NameTextbox = TextBox(setting.WINDOW_WIDTH-320,20,300,50)
    NotiLabel = Label(NameTextbox.rect.left,NameTextbox.rect.top+NameTextbox.rect.height+10,NameTextbox.rect.width,NameTextbox.rect.height,text='',color= "red")

    login = Player()

    controls = pygame.sprite.Group()
    controls.add(PlayButton,LogoImage,ShopButton,InventoryButton, NameTextbox, NotiLabel)

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
            c.displayEffect()
        Menu.login.authenticate(Menu.NameTextbox.text)
        if Menu.login.isAuth:
            Menu.NotiLabel.text = f"Welcome {Menu.login.name}"
            Menu.NotiLabel.color = "yellow"
            Menu.NotiLabel.bgcolor= "black"
            if Menu.PlayButton.isClicked():
                print("play clicked")
            if Menu.ShopButton.isClicked():
                print("shop clicked")
            if Menu.InventoryButton.isClicked():
                print("Inventory clicked")
        else:
            Menu.NotiLabel.text = f"USER IS NOT FOUND"
            Menu.NotiLabel.color = "red"
            Menu.NotiLabel.bgcolor = None


