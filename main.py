from tkinter import *
from random import randrange as rnd, choice, randint
import time
import tkinter.font
import tkinter.messagebox

root = Tk()
root.geometry('540x760')
canv = Canvas(root, bg='black')
canv.grid(row=0, column=0)
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")
otherFont = tkinter.font.Font(family="OCR-A II", size=20)
menuFont = tkinter.font.Font(family="Fixedsys", size=30)
canv.pack(fill=BOTH, expand=1)

shots = []
# canv = Canvas(root, bg="blue", height=760, width=540)
# filename = PhotoImage(file="D:\\python\\lopatich_hood\\star wars\\space11.png")
# background_label = Label(root, image=filename)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)


class spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship = PhotoImage(file='spaceship.png')
        self.timer = 0
        self.tPeriod = 0
        self.period = 3
        self.left = False
        self.right = False
        self.hp = 3
        # self.autofire = False
        canv.bind("<Left>", self.moveLeft)
        canv.bind("<Right>", self.moveRight)
        canv.bind("<KeyRelease-Left>", self.stopLeft)
        canv.bind("<KeyRelease-Right>", self.stopRight)

    # canv.bind("<KeyRelease-space>", self.spawnBullet)
    # canv.bind("<KeyRelease-Shift_L>", self.toggleAutoFire)

    def draw(self):
        canv.create_image(self.x, self.y,
                          image=self.ship,
                          anchor=NW)


        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= 2
        canv.create_text(self.x + 25, self.y - 20, text="HP: " + str(self.hp),
                         fill="white", font=otherFont)

    def update(self):
        # if self.hp > 0:
        if self.left and self.x >= 0:
            self.x -= 10
        if self.x < 0:
            self.x = 0
        if self.right and self.x + 50 <= canv.winfo_width():
            self.x += 10
        if self.x + 50 > canv.winfo_width():
            self.x = canv.winfo_width() - 50
        self.draw()
        if self.tPeriod == 1 and self.timer == 1:
            self.spawnBullet(False)

    def moveLeft(self, event):
        self.left = True

    def moveRight(self, event):
        self.right = True

    def stopLeft(self, event):
        self.left = False

    def stopRight(self, event):
        self.right = False

    def spawnBullet(self, event):
        if self.hp > 0:
            global shots
            shots.append(bullet(self.x + 25, self.y, 0, -20))

class bullet:
    def __init__(self, x, y, xVel, yVel):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.view = PhotoImage(file='bullet1.png')
        self.bullet = True
        self.laser = False
        canv.bind("<space>", self.change_weapon)
        canv.bind("<KeyRelease-space>", self.change_weapon_back)

    def change_weapon(self, event):
        self.view = PhotoImage(file='laser1.png')
        self.bullet = False
        self.laser = True


    def change_weapon_back(self, event):
        self.view = PhotoImage(file='bullet1.png')
        self.laser = False
        self.bullet = True

    def draw(self):
        canv.create_image(self.x, self.y - 25,
                          image=self.view,
                          anchor=NW)

    def update(self):
        self.draw()
        self.x += self.xVel
        self.y += self.yVel
        if self.x >= canv.winfo_width() or self.x <= 0:
            self.xVel *= -1

p = spaceship(150, 660)


def startGame(event):
    global gameState
    gameState = 1


# MAKING SURE THAT THE CANVAS ACTUALLY RECEIVES KEYBOARD INPUT!!!!
canv.focus_set()
canv.bind("<Return>", startGame)

def drawShots():
    for i in range(len(shots)):
        try:
            shots[i].update()
        except:
            pass

def drawBackground():
    pass


def draw():
    canv.delete("all")
    drawBackground()
    p.update()
    drawShots()

    root.after(25, draw)



draw()
mainloop()
