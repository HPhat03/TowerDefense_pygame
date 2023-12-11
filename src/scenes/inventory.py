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
    team_towers = []

    for i in range(5):
        box = PictureBox(surf.rect.left + 10 + 110 * i,
                         surf.rect.top + 10, 100, 100,
                         "src/assets/towers/white.jpg")
        team_towers.append(box)

    controls.add(surf, surf2, btnBack)

    @staticmethod
    def event_handler(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        # drawing background
        Inventory.background = pygame.transform.scale(
            Inventory.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(Inventory.background, (0, 0))

        # drawing session
        for c in Inventory.controls:
            c.draw(screen)
        inventory = login.inventory

        for i in range(12):
            if i < len(inventory):
                Inventory.boxGr[i].pictureBox.img_path = inventory[i].img_src
                Inventory.boxGr[i].mainText.text = inventory[i].name
                Inventory.boxGr[i].subText.text = f"${inventory[i].in_game_price}"
                Inventory.boxGr[i].item = inventory[i]
            else:
                Inventory.boxGr[i].pictureBox.img_path = "src/assets/MediumLevelBG.png"
                Inventory.boxGr[i].mainText.text = ""
                Inventory.boxGr[i].subText.text = ""
                Inventory.boxGr[i].item = None

        team = login.team
        for b in Inventory.boxGr:
            b.draw(screen)
            
            if b.isClicked():
                isFreeTeam = True

                if b.item is None:
                    continue

                for t in team:
                    if t.id == b.item.id or len(team) == 5:
                        isFreeTeam = False
                if isFreeTeam:
                    item = Tower(b.item.id)
                    team.append(item)

        for t in range(len(team)):
            if Inventory.team_towers[t].isClicked():
                team.remove(team[t])

        for i, t in enumerate(Inventory.team_towers):
            t.img_path = team[i].img_src if i < len(team) else \
                "src/assets/towers/white.jpg"

        for c in Inventory.team_towers:
            c.draw(screen)

        if Inventory.btnBack.isClicked():
            # print(login)
            return Scenes.MENU

        return None
