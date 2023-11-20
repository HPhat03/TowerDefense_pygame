import pygame

from .core import Scene, Scenes
from src.controls import ItemBox, Label, PictureBox, Surface
from src.setting import WINDOW_WIDTH, WINDOW_HEIGHT
from src import db
from src.Tower import Tower


class Shop(Scene):
    #INIT CONTROLS
    background = pygame.image.load("src/assets/shop_bg.jpg")
    controls = pygame.sprite.Group()
    # list_towers = pygame.sprite.Group()

    btnBack = PictureBox(20, 20, 100, 50, "src/assets/Logo.png")
    title = Label((WINDOW_WIDTH - 100) / 2, 20, 100, 40, "SHOP",
                  color="white")

    surf = Surface(20, 80, WINDOW_WIDTH - 40, WINDOW_HEIGHT - 110,
                   (0, 0, 0, 128))
    lb_coin = Label(WINDOW_WIDTH-20-100,20,100,40, "", color="yellow")

    boxGr = []
    for i in range(2):
        for j in range(5):
            itembox = ItemBox(70 + 160 * j, 100 + 230 *i, 150,
                      image_path="src/assets/MediumLevelBG.png",
                      text="")
            boxGr.append(itembox)
    #Getting Towers data
    shop = []
    itemids = db.select("select id from Tower")
    for i in itemids:
        tower = Tower(i[0])
        shop.append(tower)

    controls.add(surf, btnBack, title, lb_coin)

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
        towers = [i for i in Shop.shop if i.in_shop_price > 0 and i not in
                  login.inventory]
        # towers = [i for i in Shop.shop if i.in_shop_price > 0 and not login.hadTower(i)]

        for i in range(len(towers)):
            Shop.boxGr[i].pictureBox.img_path = towers[i].img_src
            Shop.boxGr[i].mainText.text = towers[i].name
            Shop.boxGr[i].subText.text = f"${towers[i].in_shop_price}"
            Shop.boxGr[i].item = towers[i]

        #drawing session
        for c in Shop.controls:
            c.draw(screen)
        for b in Shop.boxGr:
            if b.item != None:
                b.draw(screen)

        #Event session
        for box in Shop.boxGr:
            if box.item != None:
                if box.isClicked() and login.coins>= box.item.in_shop_price:
                    login.coins -= box.item.in_shop_price
                    #login.update(Coins = True)
                    login.inventory.append(box.item)
                    Shop.boxGr[i].item = None


        if Shop.btnBack.isClicked():
            print(login)
            return Scenes.MENU

        return None
