import pygame

from src import setting, db
from .core import Scene, Scenes
from src.controls import Button, PictureBox, TextBox, Label


class Menu(Scene):
    background = pygame.image.load("src/assets/bgMenu.png")

    PlayButton = Button(175, 300, 200, 50, "Play", color=setting.button_color)
    ShopButton = Button(PlayButton.rect.left,
                        PlayButton.rect.top + PlayButton.rect.height + 25,
                        PlayButton.rect.width, PlayButton.rect.height, "Shop",
                        color=setting.button_color)
    InventoryButton = Button(ShopButton.rect.left,
                             ShopButton.rect.top + ShopButton.rect.height + 25,
                             ShopButton.rect.width, ShopButton.rect.height,
                             "Inventory", color=setting.button_color)
    QuitButton = Button(InventoryButton.rect.left,
                        InventoryButton.rect.top +
                        InventoryButton.rect.height + 25,
                        InventoryButton.rect.width,
                        InventoryButton.rect.height, "Quit",
                        color=setting.button_color)

    LogoImage = PictureBox(100, 50, 360, 250, "src/assets/Logo.png")
    NameTextbox = TextBox(setting.WINDOW_WIDTH - 320, 20, 300, 50)
    NotiLabel = Label(NameTextbox.rect.left,
                      NameTextbox.rect.top + NameTextbox.rect.height + 10,
                      NameTextbox.rect.width, NameTextbox.rect.height,
                      text='', color="red")

    controls = pygame.sprite.Group()
    controls.add(PlayButton, LogoImage, ShopButton, InventoryButton,
                 QuitButton, NameTextbox, NotiLabel)

    @staticmethod
    def event_handler(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                return Scenes.GAME
        return None

    @staticmethod
    def game(screen, login):
        Menu.background = pygame.transform.scale(
            Menu.background, (setting.WINDOW_WIDTH, setting.WINDOW_HEIGHT))
        screen.blit(Menu.background, (0, 0))
        for c in Menu.controls:
            c.draw(screen)
            c.displayEffect()

        if Menu.QuitButton.isClicked():
            db.close()
            quit()
        if login.isAuth:
            if login.name != Menu.NameTextbox.text:
                login.update(coins=True, team=True, inventory=True)
                print("saved")
                login.isAuth = False
        if login.isAuth is False:
            login.authenticate(Menu.NameTextbox.text)

            Menu.NotiLabel.text = "USER IS NOT FOUND"
            Menu.NotiLabel.color = "red"
            Menu.NotiLabel.background_color = -1

        else:
            Menu.NotiLabel.text = f"Welcome {login.name}"
            Menu.NotiLabel.color = "green"
            Menu.NotiLabel.background_color = "black"

            if Menu.PlayButton.isClicked():
                return Scenes.GAME

            if Menu.ShopButton.isClicked():
                return Scenes.SHOP

            if Menu.InventoryButton.isClicked():
                return Scenes.INVENTORY
        return None
