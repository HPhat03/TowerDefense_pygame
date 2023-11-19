import math

import pygame as pg
import pygame.sprite

from src import setting, db

pg.font.init()

class Control(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(left,top,width,height)
        self.text = ''
        self.color = ''
        self.clicked = False

    class Meta:
        abstract = True

    def draw(self, surface):
        pass

    def displayEffect(self):
        pass

    def draw_text(self, surface, size = setting.DEFAULT_SIZE):
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
        if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked=True
            return True


class Button(Control):
    def __init__(self, left, top, width, height, text="new button", \
                 border_radius=5, bgcolor="white", color="black"):
        super().__init__(left, top, width, height)
        self.text = text
        self.color = color
        self.bgcolor=bgcolor
        self.radius = border_radius

        self.default_bg = bgcolor
        self.default_cl = color

    def draw(self, surface):
        pg.draw.rect(surface, self.bgcolor, self.rect, \
                     border_radius=self.radius)
        self.draw_text(surface)


    def isHovering(self):
        return self.rect.collidepoint(pg.mouse.get_pos()) and \
            pg.mouse.get_pressed()[0] == 0

    def displayEffect(self, HoverBGColor = setting.button_color, HoverColor = "white", ClickBGColor = "red", ClickColor = "white"):
        if self.isHovering():
            self.bgcolor = HoverBGColor
            self.color = HoverColor
        elif self.isClicked():
            self.clicked = False
            self.bgcolor = ClickBGColor
            self.color = ClickColor
        elif not self.rect.collidepoint(pg.mouse.get_pos()):
            self.bgcolor = self.default_bg
            self.color = self.default_cl

class TextBox(Control):
    def __init__(self, left, top, width, height, border_radius=3, \
                 bgcolor="white", color="black"):
        super().__init__(left, top, width, height)
        self.radius = border_radius
        self.text = ''
        self.bgcolor = bgcolor
        self.color = color
        self.focus = False

    def draw(self, surface):
        pg.draw.rect(surface, self.bgcolor, self.rect)
        self.setFocus()
        while self.focus:
            for e in pg.event.get():
                match e.type:
                    case pg.KEYDOWN:
                        if e.key == pg.K_BACKSPACE:
                            self.text = self.text[:-1]
                        elif self.text_rect.width < self.rect.width - setting.DEFAULT_SIZE and e.key not in {pg.K_TAB, pg.K_RETURN}:
                            self.text += e.unicode
                        if e.key == pg.K_RETURN:
                            self.focus = False
                        # self.focus = e.key in {pg.K_RETURN, pg.K_TAB}

                    case pg.QUIT:
                        db.close()
                        quit()
                        
            self.setFocus()
            pg.draw.rect(surface, self.bgcolor, self.rect, border_radius=self.radius)
            self.draw_text(surface)
            pg.display.update()
        self.draw_text(surface)

    def setFocus(self):
        if pg.mouse.get_pressed()[0] == 1:
            self.focus = self.rect.collidepoint(pg.mouse.get_pos())
        self.bgcolor = "grey" if self.focus else "white"


class PictureBox(Control):
    def __init__(self, left, top, width, height, img_path):
        super().__init__(left, top, width, height)
        self.img_path = img_path

    def draw(self, surface):
        if self.img_path != "":
            self.image = pg.image.load(self.img_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
            surface.blit(self.image, (self.rect.left, self.rect.top))
        else:
            pg.draw.rect(surface, "black", self.rect)
class Label(Control):
    def __init__(self, left, top, width, height, text="new label", bgcolor = None, color = "black", border_radius = 10, size = setting.DEFAULT_SIZE):
        super().__init__(left, top, width, height)
        self.text = text
        self.bgcolor = bgcolor
        self.color = color
        self.radius = border_radius
        self.font_size = size

    def draw(self, surface):
        if self.bgcolor != None:
            pg.draw.rect(surface, self.bgcolor, self.rect, border_radius=self.radius)
        self.draw_text(surface, self.font_size)
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
    def __init__(self, left, top, controls, padding, bgcolor = "Black"):
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
