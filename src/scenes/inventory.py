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

    towers = Tower.get_all()
    controls = pygame.sprite.Group()
    list_towers = pygame.sprite.Group()
    inventory = pygame.sprite.Group()

    for i in range(5):
        box = PictureBox(surf.rect.left + 10 + 110 * i,
                         surf.rect.top + 10, 100, 100,
                         "src/assets/towers/white.jpg")
        inventory.add(box)

    for i, t in enumerate(towers):
        tower = ItemBox(surf2.rect.left + 10 + i*160, surf2.rect.top + 10, 150,
                        t["img_src"], t["name"], f"{t['in_game_price']} $")
        list_towers.add(tower)

    controls.add(surf, surf2, btnBack)

    @staticmethod
    def event_handler(event, login):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        Inventory.background = pygame.transform.scale(
            Inventory.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(Inventory.background, (0, 0))

        for c in Inventory.controls:
            c.draw(screen)
            c.displayEffect()

        for c in Inventory.inventory:
            c.draw(screen)
            if c.isClicked():
                c.img_path = "src/assets/towers/white.jpg"

        for t in Inventory.list_towers:
            t.draw(screen)
            if t.isClicked():
                for c in Inventory.inventory:
                    if c.img_path.endswith("white.jpg"):
                        c.img_path = t.img
                        break

        if Inventory.btnBack.isClicked():
            return Scenes.MENU

        return None
