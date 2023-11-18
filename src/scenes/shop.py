import pygame

from src.controls import Label, PictureBox
from .core import Scene, Scenes
from src import setting


class Shop(Scene):
    background = pygame.image.load("src/assets/shop_bg.jpg")

    btnBack = PictureBox(20, 20, 100, 50, "src/assets/Logo.png")
    title = Label((setting.WINDOW_WIDTH - 100) / 2, 20, 100, 40, "SHOP",
                  color="white")

    surf = pygame.Surface((setting.WINDOW_WIDTH - 40,
                           setting.WINDOW_HEIGHT - 110))
    box = pygame.Rect(40, 100, 100, 150)

    controls = pygame.sprite.Group()
    controls.add(btnBack, title)

    @staticmethod
    def event_handler(event, login):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return Scenes.MENU
        return None

    @staticmethod
    def game(screen, login):
        Shop.background = pygame.transform.scale(
            Shop.background, (setting.WINDOW_WIDTH, setting.WINDOW_HEIGHT))
        screen.blit(Shop.background, (0, 0))
        screen.blit(Shop.surf, (20, 80))

        for c in Shop.controls:
            c.draw(screen)
            c.displayEffect()

        Shop.surf.fill((0, 0, 0))
        Shop.surf.set_alpha(128)
        pygame.draw.rect(screen, "white", Shop.box)

        if Shop.btnBack.isClicked():
            return Scenes.MENU

        return None
