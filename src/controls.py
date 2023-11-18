import math

import pygame as pg
import pygame.sprite
from abc import abstractmethod

from src import setting
from src.types import ColorValue

pg.font.init()


class Control(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, text: str = '',
                 background_color: ColorValue = "white",
                 color: ColorValue = "black"):
        pygame.sprite.Sprite.__init__(self)
        self.pos = (left, top)
        self.size = (top, width)
        self.text = text
        self.color = color
        self.background_color = background_color
        self.rect: pg.Rect = pg.Rect(left, top, width, height)
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
        pen = pg.font.Font("src/fonts/Baloo2.ttf",size=size)
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


class Button(Control):
    def __init__(self, left, top, width, height, text: str = "new button",
                 border_radius: int = 5, bgcolor: str = "white",
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

    def displayEffect(self, HoverBGColor = setting.button_color,
                      HoverColor = "white", ClickBGColor = "red",
                      ClickColor = "white"):
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
                            setting.FONT.__sizeof__() and \
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
        self.image = pg.image.load(self.img_path).convert_alpha()
        self.image = pg.transform.scale(self.image,
                                        (self.rect.width, self.rect.height))
        surface.blit(self.image, (self.rect.left, self.rect.top))


class Label(Control):
    def __init__(self, left, top, width, height, text: str = "new label",
                 bgcolor=-1, color="black", border_radius: int = 10,
                 size=setting.DEFAULT_SIZE):
        super().__init__(left, top, width, height, text, bgcolor, color)
        self.radius = border_radius
        self.font_size = size

    def draw(self, surface):
        if self.background_color != -1:
            pg.draw.rect(surface, self.background_color, self.rect,
                         border_radius=self.radius)
        self.draw_text(surface)


class Surface(Control):
    def __init__(self, left, top, width, height, background_color):
        super().__init__(left, top, width, height,
                         background_color=background_color)
        self.surf = pg.Surface((width, height))

    def draw(self, surface):
        surface.blit(self.surf, (self.pos[0], self.pos[1]))


class ItemBox(Control):
    def __init__(self,left,top,width,image_path, text = "Item Box", subtext = "", bgcolor = "black", color = "White", subcolor = "yellow", padding = 5, boder_radius = 0):
        super().__init__(left, top, width, width)
        self.img = image_path
        self.text = text
        self.subtext = subtext
        self.color = color
        self.subcolor = subcolor
        self.padding = padding
        box = width - 2 * padding
        self.pictureBox = PictureBox(left + padding, top + padding, box, box, image_path)
        self.MainText = Label(left + padding, self.pictureBox.rect.top + self.pictureBox.rect.height,
                              width - 2 * padding, width / 4, self.text, color=self.color, size=width / 5)
        self.SubText = Label(left + padding, self.MainText.rect.top + self.MainText.rect.height - padding,
                             width - 2 * padding, width / 4, self.subtext, color=self.subcolor, size=width / 6)
        self.rect = pygame.Rect(left,top,width,self.pictureBox.rect.height+self.MainText.rect.height+self.SubText.rect.height+padding)
        self.bgColor = bgcolor
        self.radius = boder_radius
        self.controls = pg.sprite.Group(self.pictureBox,self.MainText,self.SubText)

    def update_box(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        padding = self.padding
        box = width -2 * padding
        self.pictureBox.rect = pg.Rect(left + padding, top + padding, box, box)
        self.MainText.rect = pg.Rect(left + padding, self.pictureBox.rect.top + self.pictureBox.rect.height,
                          width - 2 * padding, width / 4)
        self.SubText.rect = pg.Rect(left + padding, self.MainText.rect.top + self.MainText.rect.height - padding,
                             width - 2 * padding, width / 4)


    def draw(self, surface):
        self.update_box()
        pg.draw.rect(surface,self.bgColor,self.rect, border_radius=self.radius)
        for c in self.controls:
            c.draw(surface)


class ControlsContainer(Control):
    def __init__(self, left, top, controls, padding, bgcolor = "grey"):
        super().__init__(left, top, 100, 100)
        width = height = 2*padding
        maxl = maxt = 0
        w=h=0
        self.controls = controls
        for c in controls:
            c.rect.top = c.rect.top + top
            c.rect.left = c.rect.left + left
            if c.rect.left > maxl:
                maxl = c.rect.left
                w = c.rect.width
            if c.rect.top > maxt:
                maxt = c.rect.top
                h = c.rect.height
        width = 2*padding + maxl - left + w
        height = 2*padding + maxt - top + h
        self.rect = pg.Rect(left,top,width,height)
        self.bgcolor = bgcolor

    def draw(self, surface):
        pg.draw.rect(surface,self.bgcolor,self.rect)
        for c in self.controls:
            c.draw(surface)
