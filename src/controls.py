import pygame as pg
import pygame.sprite

from src import setting

class Control(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ''
        self.color = ''

    class Meta:
        abstract = True

    def draw(self, surface):
        pass

    def draw_text(self, surface):
        self.text_display = setting.FONT.render(self.text, True, self.color)
        self.text_rect = self.text_display.get_rect(center=self.rect.center)
        surface.blit(self.text_display, self.text_rect)

    def isHovering(self):
        return self.rect.collidepoint(pg.mouse.get_pos()) and \
            pg.mouse.get_pressed()[0] == 0


class Button(Control):
    def __init__(self, left, top, width, height, text="new button", border_radius=5, bgcolor="white", color="black"):
        super().__init__()
        self.rect = pg.Rect(left, top, width, height)
        self.text = text
        self.color = color
        self.bgcolor = bgcolor
        self.radius = border_radius
        self.clicked = False

    def draw(self, surface):
        pg.draw.rect(surface, self.bgcolor, self.rect, border_radius=self.radius)
        self.draw_text(surface)
        self.handle()

    def isClicked(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                return True
        else:
            return False
        
    def handleHover(self, newHandle=None):
        def inner():
            if newHandle is not None:
                newHandle()
            else:
                if self.isHovering():
                    self.bgcolor = (42, 186, 103)
                    self.color = "white"

        return inner
    
    def handle(self):
        self.handleHover()

        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.bgcolor = "white"
            self.color = (42, 186, 103)


class TextBox(Control):
    def __init__(self, left, top, width, height, border_radius=3, \
                bgcolor="white", color="black"):
        super().__init__()
        self.rect = pg.Rect(left, top, width, height)
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
                        elif self.text_rect.width < self.rect.width - \
                                setting.FONT.__sizeof__() and e.key \
                                    not in {pg.K_TAB, pg.K_RETURN}:
                            self.text += e.unicode
                    case pg.QUIT:
                        pg.quit()
                    case pg.KEYDOWN:
                        if e.key in {pg.K_RETURN, pg.K_TAB}:
                            self.focus = False
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
        super().__init__()
        self.rect = pg.Rect(left, top, width, height)
        self.img_path = img_path

    def draw(self, surface):
        self.image = pg.image.load(self.img_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
        surface.blit(self.image, (self.rect.left, self.rect.top))
