import pygame as pg
from Controls import *
pg.init()

screen = pg.display.set_mode((500,500))
clock = pg.time.Clock()


#Cau Hinh Control
testButton = Button(100,100,200,100, border_radius=25)
# testTxtBox = TextBox(100,250,300,100)
testPB = PictureBox(100, 200, 100, 100, "Assets/png/Default size/towerDefense_tile250.png")
testlabel = Label(200,200, 200, 50, "Hello")

running =True
while running:
    clock.tick(60)
    screen.fill('green')
    #testButton.draw(screen)
    # testTxtBox.draw(screen)
    #testPB.draw(screen)
    testlabel.draw(screen)
    #if testButton.isClicked():
     #   print("clicked")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    pg.display.flip()