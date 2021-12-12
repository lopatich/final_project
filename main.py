from tkinter import *
from random import randrange as rnd, choice, randint
import time
import tkinter.font
import tkinter.messagebox
import random
root = Tk()
root.geometry('550x760')
canv = Canvas(root, bg='black')
canv.grid(row=0, column=0)
gOver = tkinter.font.Font(family="Chiller", size=30, weight="bold")
otherFont = tkinter.font.Font(family="OCR-A II", size=20)
menuFont = tkinter.font.Font(family="Fixedsys", size=30)
canv.pack(fill=BOTH, expand=1)


aliens = []
wavesSurvived = 0
shots = []
dead = False
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
        global dead
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
        for i in aliens:
            if i.x + 50 >= self.x and i.x <= self.x + 50 and i.y + 50 >= self.y \
                and i.y <= self.y + 50:
                self.hp = -1

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
        self.dead = False
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
    def checkCollisions(self):
        for i in aliens:

            if i.x + 50 >= self.x and i.x <= self.x + 25 and i.y + 50 >= self.y \
               and i.y <= self.y + 40:
                if self.laser:
                    i.hp -= 1
                if self.bullet:
                    i.hp -= 0.5
                self.dead = True

    def update(self):
        self.draw()
        self.x += self.xVel
        self.y += self.yVel
        if self.x >= canv.winfo_width() or self.x <= 0:
            self.xVel *= -1
        if self.y + 25 >= canv.winfo_height() or self.y <= 0:
            self.dead = True

        self.checkCollisions()


class alien():
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.dead = False
        # One-hit wonder alien, no attack
        if self.t == 1:
            self.sprites = [PhotoImage(file="1HitAlien1.gif"),
                            PhotoImage(file="1HitAlien2.gif")]
            self.period = 15
            self.moveSpeed = 3
            self.hp = 1
        # 3-hit alien, no attack
        if self.t == 2:
            self.sprites = [PhotoImage(file="MultiHitAlien1.gif"),
                            PhotoImage(file="MultiHitAlien2.gif")]
            self.period = 12
            self.moveSpeed = 3
            self.hp = 2.5
        self.xVel = self.moveSpeed
        self.timer = 0
        self.tPeriod = 0
        self.moveDownTimer = 0
        self.moveNext = True
    def draw(self):
        canv.create_image(self.x, self.y - 25,
                          image=self.sprites[self.tPeriod],
                          anchor=NW)
        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= len(self.sprites)
    def update(self):
        self.draw()
        self.x += self.xVel
        if self.x <= 0 or self.x + 50 >= canv.winfo_width():
            # Speed up, move down
            self.xVel *= -1.15
            self.y += 50
        if self.hp <= 0:
            self.dead = True
# Make a 8rowx6column grid of aliens.
def spawnAliens():
    global p
    global aliens
    global wavesSurvived
    for i in range(0, 550, 50):
        for j in range(0, 350, 50):
            if wavesSurvived <= 2:
                aliens.append(alien(i, j, 1))
            elif wavesSurvived <= 4:
                aliens.append(alien(i, j, random.randint(1, 2)))
            elif wavesSurvived <= 5:
                aliens.append(alien(i, j, 2))
    p.hp = 3
    wavesSurvived += 1
p = spaceship(150, 660)


def startGame(event):
    global gameState
    gameState = 1


# MAKING SURE THAT THE CANVAS ACTUALLY RECEIVES KEYBOARD INPUT!!!!
canv.focus_set()
canv.bind("<Return>", startGame)

def drawShots():
    todes = []
    for i in range(len(shots)):
        shots[i].update()
        if shots[i].dead:
            todes.append(i)
    for i in range(len(todes)):
        shots.pop(todes[i] - i)
def drawAliens():
    todel = []
    for i in range(len(aliens)):

        aliens[i].update()
        if aliens[i].dead:
            todel.append(i)
    for i in range(len(todel)):
        aliens.pop(todel[i]-i)


def drawBackground():
    pass


def draw():
    canv.delete("all")
    drawBackground()
    p.update()
    drawShots()
    drawAliens()
    if len(aliens) == 0:
        spawnAliens()
    root.after(25, draw)

draw()
mainloop()
