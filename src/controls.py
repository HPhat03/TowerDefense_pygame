import math

import pygame as pg
import pygame.sprite
from abc import abstractmethod
from typing import cast

from src import setting
from src.types import ColorValue, RGBAOutput

pg.font.init()


class Control(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, text: str = '',
                 background_color: ColorValue = "white",
                 color: ColorValue = "black"):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.color = color
        self.background_color = background_color
        self.rect = pg.Rect(left, top, width, height)
        self.clicked = False

    class Meta:
        abstract = True

    @abstractmethod
    def draw(self, surface):
        pass

    def displayEffect(self):
        pass

    def draw_text(self, surface, size=setting.DEFAULT_SIZE):
        size = math.floor(size)
        pen = pg.font.Font("src/fonts/Baloo2.ttf", size=size)
        self.text_display = pen.render(self.text, True, self.color)
        self.text_rect = self.text_display.get_rect(center=self.rect.center)
        surface.blit(self.text_display, self.text_rect)

    def isClicked(self):
        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return False

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        elif pg.mouse.get_pressed()[0] == 1 and self.clicked is False:
            self.clicked = True
            return True
        return False


class Button(Control):
    def __init__(self, left, top, width, height, text: str = "new button",
                 border_radius: int = 5, bgcolor: ColorValue = "white",
                 color: ColorValue = "black"):
        super().__init__(left, top, width, height, text, bgcolor, color)
        self.radius = border_radius
        self.default_bg = bgcolor
        self.default_cl = color

    def draw(self, surface):
        pg.draw.rect(surface, self.background_color, self.rect,
                     border_radius=self.radius)
        self.draw_text(surface)

    def isHovering(self):
        return self.rect.collidepoint(pg.mouse.get_pos()) and \
            pg.mouse.get_pressed()[0] == 0

    def displayEffect(self, HoverBGColor: ColorValue = setting.button_color,
                      HoverColor: ColorValue = "white",
                      ClickBGColor: ColorValue = "red",
                      ClickColor: ColorValue = "white"):
        if self.isHovering():
            self.background_color = HoverBGColor
            self.color = HoverColor
        elif self.isClicked():
            self.clicked = False
            self.background_color = ClickBGColor
            self.color = ClickColor
        elif not self.rect.collidepoint(pg.mouse.get_pos()):
            self.background_color = self.default_bg
            self.color = self.default_cl


class TextBox(Control):
    def __init__(self, left, top, width, height, border_radius: int = 3,
                 bgcolor="white", color="black"):
        super().__init__(left, top, width, height, background_color=bgcolor,
                         color=color)
        self.radius = border_radius
        self.focus = False

    def draw(self, surface):
        pg.draw.rect(surface, self.background_color, self.rect)
        self.setFocus()
        while self.focus:
            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif self.text_rect.width < self.rect.width - \
                            setting.DEFAULT_SIZE and \
                            e.key not in {pg.K_TAB, pg.K_RETURN}:
                        self.text += e.unicode
                    if e.key == pg.K_RETURN:
                        self.focus = False

            self.setFocus()
            pg.draw.rect(surface, self.background_color, self.rect,
                         border_radius=self.radius)
            self.draw_text(surface)
            pg.display.update()
        self.draw_text(surface)

    def setFocus(self):
        if pg.mouse.get_pressed()[0] == 1:
            self.focus = self.rect.collidepoint(pg.mouse.get_pos())
        self.background_color = "grey" if self.focus else "white"


class PictureBox(Control):
    def __init__(self, left, top, width, height, img_path):
        super().__init__(left, top, width, height)
        self.img_path = img_path

    def draw(self, surface):
        if self.img_path != "":
            self.image = pg.image.load(self.img_path).convert_alpha()
            self.image = pg.transform.scale(self.image,
                                            (self.rect.width,
                                             self.rect.height))
            surface.blit(self.image, (self.rect.left, self.rect.top))
        else:
            pg.draw.rect(surface, "black", self.rect)


class Label(Control):
    def __init__(self, left, top, width, height, text: str = "new label",
                 bgcolor: ColorValue = -1, color: ColorValue = "black",
                 border_radius: int = 10, size=setting.DEFAULT_SIZE):
        super().__init__(left, top, width, height, text, bgcolor, color)
        self.radius = border_radius
        self.font_size = size

    def draw(self, surface):
        if self.background_color != -1:
            pg.draw.rect(surface, self.background_color, self.rect,
                         border_radius=self.radius)
        self.draw_text(surface, self.font_size)


class Surface(Control):
    def __init__(self, left, top, width, height, background_color: RGBAOutput):
        super().__init__(left, top, width, height,
                         background_color=background_color)
        self.surf = pg.Surface((width, height))

    def draw(self, surface):
        surface.blit(self.surf, (self.rect.left, self.rect.top))
        *rgb, a = cast(RGBAOutput, self.background_color)
        self.surf.fill(rgb)
        self.surf.set_alpha(a)


class ItemBox(Control):
    def __init__(self, left, top, width, image_path: str,
                 text: str = "Item Box", subtext: str = "",
                 bgcolor: ColorValue = "black",
                 color: ColorValue = "white", subcolor: ColorValue = "yellow",
                 padding: int = 5, boder_radius: int = 0, item=None):
        super().__init__(left, top, width, width, text, bgcolor, color)
        self.img = image_path
        self.subtext = subtext
        self.subcolor = subcolor
        self.padding = padding
        box = width - 2 * padding
        self.pictureBox = PictureBox(left + padding, top + padding, box, box,
                                     self.img)
        self.mainText = Label(left + padding, self.pictureBox.rect.bottom,
                              box, width / 4, self.text,
                              color=self.color, size=width/5)
        self.subText = Label(left + padding, self.mainText.rect.bottom +
                             padding, box, width / 4, self.subtext,
                             color=self.subcolor, size=width/6)
        self.rect = pygame.Rect(left, top, width, self.pictureBox.rect.height +
                                self.mainText.rect.height +
                                self.subText.rect.height + padding)
        self.radius = boder_radius
        self.controls = pg.sprite.Group()
        self.item = item
        self.controls.add(self.pictureBox, self.mainText, self.subText)
        self.clicked = True

    def update_box(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        padding = self.padding
        box = width - 2 * padding
        self.pictureBox.rect = pg.Rect(left + padding, top + padding, box, box)
        self.mainText.rect = pg.Rect(left + padding,
                                     self.pictureBox.rect.bottom, box, width/4)
        self.subText.rect = pg.Rect(left + padding, self.mainText.rect.bottom -
                                    padding, box, width / 4)

    def draw(self, surface):
        self.update_box()
        pg.draw.rect(surface, self.background_color, self.rect,
                     border_radius=self.radius)
        for c in self.controls:
            c.draw(surface)


class ControlsContainer(Control):
    def __init__(self, left, top, controls, padding,
                 bgcolor: ColorValue = "black"):
        super().__init__(left, top, 100, 100, background_color=bgcolor)
        width = height = 2 * padding
        maxl = maxt = 0
        w = h = 0
        self.controls = controls
        for c in controls:
            c.rect.top += top
            c.rect.left += left
            if c.rect.left > maxl:
                maxl, w = c.rect.left, c.rect.width
            if c.rect.top > maxt:
                maxt, h = c.rect.top, c.rect.height
        width = 2 * padding + maxl - left + w
        height = 2 * padding + maxt - top + h
        self.rect = pg.Rect(left, top, width, height)

    def draw(self, surface):
        pg.draw.rect(surface, self.background_color, self.rect)
        for c in self.controls:
            c.draw(surface)
