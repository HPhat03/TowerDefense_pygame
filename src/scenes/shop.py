import pygame

from src.controls import ItemBox, Label, PictureBox, Surface
from .core import Scene, Scenes
from src.setting import WINDOW_WIDTH, WINDOW_HEIGHT


class Shop(Scene):
    background = pygame.image.load("src/assets/shop_bg.jpg")
    controls = pygame.sprite.Group()

    btnBack = PictureBox(20, 20, 100, 50, "src/assets/Logo.png")
    title = Label((WINDOW_WIDTH - 100) / 2, 20, 100, 40, "SHOP",
                  color="white")

    surf = Surface(20, 80, WINDOW_WIDTH - 40, WINDOW_HEIGHT - 110,
                   (0, 0, 0, 128))

    towers = [
        {
            "name": "scout",
            "price": 200
        },
        {
            "name": "sniper",
            "price": 250
        }
    ]

    controls.add(surf, btnBack, title)

    for i, t in enumerate(towers):
        box = ItemBox(40 + 160*i, 100, 150,
                      "src/assets/towers/towerDefense_tile250.png",
                      t["name"], f"{t['price']} $")
        controls.add(box)

    @staticmethod
    def event_handler(event, login):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        Shop.background = pygame.transform.scale(
            Shop.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(Shop.background, (0, 0))

        for c in Shop.controls:
            c.draw(screen)
            c.displayEffect()

        if Shop.btnBack.isClicked():
            return Scenes.MENU

        return None
