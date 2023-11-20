import pygame
from src.Tower import Tower

from src.controls import ItemBox, Label, PictureBox, Surface
from .core import Scene, Scenes
from src.setting import WINDOW_WIDTH, WINDOW_HEIGHT
from src import db
from src.Tower import Tower

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
    shop = []
    itemids = db.select("select id from Tower")
    for i in itemids:
        tower = Tower(i[0])
        shop.append(tower)

    controls.add(surf, btnBack, title, lb_coin)
    boxGr = pygame.sprite.Group()

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
        towers = [i for i in Shop.shop if i.in_shop_price > 0 and i not in \
            login.inventory]

        for i in range(len(towers)):
            box = ItemBox(40 + 160 * i, 100, 150,
                          image_path=towers[i].img_src,
                          text=towers[i].name, subtext=f"{towers[i].in_shop_price} $")
            Shop.boxGr.add(box)

        for c in Shop.controls:
            c.draw(screen)
        for b in Shop.boxGr:
            b.draw(screen)
        for t in Shop.list_towers:
            t.draw(screen)

        if Shop.btnBack.isClicked():
            return Scenes.MENU

        return None
