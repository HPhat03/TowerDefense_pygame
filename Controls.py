
import pygame as pg
import sys

pg.font.init()
FONT = pg.font.Font("Fonts/font.ttf", 32)
class Control:
    def __init__(self):
        self.text = ''
        self.color = ''
    class Meta:
        abstract = True
    def draw_text(self,surface):
        self.text_display = FONT.render(self.text, True, self.color)
        self.text_rect = self.text_display.get_rect(center=self.rect.center)
        surface.blit(self.text_display, self.text_rect)
        pg.display.flip()
class Button(Control):
    def __init__(self, left,top,width,height,text="new button",border_radius=5,bgcolor="white",color="black"):
        self.rect = pg.Rect(left,top,width,height)
        self.text = text
        self.color = color
        self.bgcolor=bgcolor
        self.radius = border_radius
        self.clicked = False

    def draw(self, surface):
        pg.draw.rect(surface,self.bgcolor,self.rect,border_radius=self.radius)
        self.draw_text(surface)

    def isClicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
            if pg.mouse.get_pressed()[0] == 1 and self.clicked ==False:
                self.clicked=True
                return True
        else:
            return False
    def isHover(self,mouse_pos):
        if(self.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]==0):
            return True
        else:
            return False

class TextBox(Control):
    def __init__(self, left,top,width,height,border_radius=3,bgcolor="white",color="black"):
        self.rect = pg.Rect(left,top,width,height)
        self.radius = border_radius
        self.text = ''
        self.bgcolor = bgcolor
        self.color = color
        self.focus = False
    def draw(self,surface):
        pg.draw.rect(surface, self.bgcolor, self.rect)
        self.setFocus()
        while self.focus:
            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif(self.text_rect.width < self.rect.width-FONT.__sizeof__() and e.key not in {pg.K_TAB,pg.K_RETURN}):
                        self.text+= e.unicode
                    print(self.focus)
                if e.type == pg.QUIT:
                    pg.quit()
                if e.type == pg.KEYDOWN:
                    if e.key in {pg.K_RETURN, pg.K_TAB}:
                        self.focus = False
            self.setFocus()
            pg.draw.rect(surface, self.bgcolor, self.rect)
            self.draw_text(surface)
        self.draw_text(surface)
        pg.display.flip()
    def setFocus(self):
            if pg.mouse.get_pressed()[0] == 1:
                if(self.rect.collidepoint(pg.mouse.get_pos())):
                    self.focus = True
                else:
                    self.focus = False
            if self.focus:
                self.bgcolor = "grey"
            else:
                self.bgcolor = "white"



