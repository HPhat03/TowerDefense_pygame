import pygame
from src.Tower import Tower

from src.controls import ItemBox, PictureBox, Surface
from .core import Scene, Scenes
from src.setting import WINDOW_WIDTH, WINDOW_HEIGHT


class Inventory(Scene):

    background = pygame.image.load("src/assets/InventoryBG.png")

    btnBack = PictureBox(20, 20, 100, 50, "src/assets/Logo.png")
    surf = Surface(WINDOW_WIDTH / 2 - 280, 70, 560, 120,
                   (0, 0, 0, 128))
    surf2 = Surface(20, surf.rect.bottom + 20,
                    WINDOW_WIDTH - 40, WINDOW_HEIGHT -
                    (surf.rect.bottom + 40),
                    (0, 0, 0, 128))
    boxGr = []
    for i in range(2):
        for j in range(6):
            itembox = ItemBox( (j+1)*2*17 + 120 * j, 230 + 200 *i, 120,
                      image_path="src/assets/MediumLevelBG.png",
                      text="")
            boxGr.append(itembox)
    #towers = Tower.get_all()
    controls = pygame.sprite.Group()
    team_towers =[]

    for i in range(5):
        box = PictureBox(surf.rect.left + 10 + 110 * i,
                         surf.rect.top + 10, 100, 100,
                         "src/assets/towers/white.jpg")
        team_towers.append(box)


    # for i, t in enumerate(towers):
    #     tower = ItemBox(surf2.rect.left + 10 + i*160, surf2.rect.top + 10, 150,
    #                     t["img_src"], t["name"], f"{t['in_game_price']} $")
    #     list_towers.add(tower)

    controls.add(surf, surf2, btnBack)

    @staticmethod
    def event_handler(event, login):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        #drawing background
        Inventory.background = pygame.transform.scale(
            Inventory.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(Inventory.background, (0, 0))

        #drawing session
        for c in Inventory.controls:
            c.draw(screen)
        inventory = login.inventory

        for i in range(len(inventory)):
            Inventory.boxGr[i].pictureBox.img_path = inventory[i].img_src
            Inventory.boxGr[i].mainText.text = inventory[i].name
            Inventory.boxGr[i].subText.text = f"${inventory[i].in_shop_price}"
            Inventory.boxGr[i].item = inventory[i]
        team = login.team
        for b in Inventory.boxGr:
            b.draw(screen)
        for b in Inventory.boxGr:
            if b.isClicked():
                isFreeTeam = True
                for t in team:
                    if t.id == b.item.id or len(team)==5:
                        isFreeTeam = False
                if isFreeTeam:
                    item = Tower(b.item.id)
                    team.append(item)

        for t in range(len(team)):
            if Inventory.team_towers[t].isClicked():
                login.team.remove(team[t])
                for tt in Inventory.team_towers:
                    tt.img_path = "src/assets/towers/white.jpg"
        for t in range(len(team)):
            Inventory.team_towers[t].img_path = team[t].img_src

        for c in Inventory.team_towers:
            c.draw(screen)


        #get data
        # for i, t in enumerate(login.inventory):
        #     tower = ItemBox(Inventory.surf2.rect.left + 10 + i * 160, Inventory.surf2.rect.top + 10, 150,
        #                     t.img_src, t.name, f"{t.in_game_price} $")
        #     tower.draw(screen)
        #     if tower.isClicked():
        #         for c in Inventory.team_towers:
        #             if c.img_path.endswith("white.jpg"):
        #                 c.img_path = tower.img
        #                 break





        # for t in Inventory.list_towers:
        #     t.draw(screen)


        if Inventory.btnBack.isClicked():
            return Scenes.MENU

        return None
