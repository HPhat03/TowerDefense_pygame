import pygame
from src.Tower import Tower

from src.controls import ItemBox, Label, PictureBox, Surface
from .core import Scene, Scenes
from src.setting import WINDOW_WIDTH, WINDOW_HEIGHT


class Shop(Scene):
    background = pygame.image.load("src/assets/shop_bg.jpg")
    controls = pygame.sprite.Group()
    list_towers = pygame.sprite.Group()

    btnBack = PictureBox(20, 20, 100, 50, "src/assets/Logo.png")
    title = Label((WINDOW_WIDTH - 100) / 2, 20, 100, 40, "SHOP",
                  color="white")

    surf = Surface(20, 80, WINDOW_WIDTH - 40, WINDOW_HEIGHT - 110,
                   (0, 0, 0, 128))
    lb_coin = Label(WINDOW_WIDTH - 20 - 100, 20, 100, 40, "", color="yellow")

    towers = Tower.get_all()

    controls.add(surf, btnBack, title, lb_coin)

    for i, t in enumerate(towers):
        box = ItemBox(40 + 160*i, 100, 150,
                      t["img_src"], t["name"], f"{t['in_shop_price']} $")
        list_towers.add(box)

    @staticmethod
    def event_handler(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        Shop.background = pygame.transform.scale(
            Shop.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(Shop.background, (0, 0))

        Shop.lb_coin.text = f"Coins: {login.coins}"

        for c in Shop.controls:
            c.draw(screen)
            c.displayEffect()

        for t in Shop.list_towers:
            t.draw(screen)

        if Shop.btnBack.isClicked():
            return Scenes.MENU

        return None
