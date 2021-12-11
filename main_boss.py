import random
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
boss_shots = []
explosions = []
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
        self.hp3_draw = PhotoImage(file='hp3.png')
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
        canv.create_image(self.x + 25, self.y - 20, image=self.hp3_draw, anchor=NW)

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

        for j in boss_shots:
            if j.x + 15 >= self.x and j.x <= self.x + 50 and j.y + 25 >= self.y \
                    and j.y <= self.y + 50:
                self.hp -= 1
                j.dead = True
                explosions.append(explosion(self.x + 7.5, self.y))


    def moveLeft(self, event):
        self.left = True

    def moveRight(self, event):
        self.right = True

    def stopLeft(self, event):
        self.left = False

    def stopRight(self, event):
        self.right = False

    def spawnBullet(self, event):
        #if self.hp > 0:
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
        self.dead = False
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
        if self.y >= 760 or self.y <= 0:
            self.dead = True
        self.check_collision()

    def check_collision(self):
        if self.y <= 200:
            self.dead = True
            explosions.append(explosion(self.x + 7.5, self.y))


class boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 400
        self.hp = 100
        self.tPeriod = 0
        self.period = 8
        self.timer = 0
        self.ship = PhotoImage(file='boss1.png')


    def draw(self):
        canv.create_image(self.x, self.y,
                          image=self.ship,
                          anchor=NW)

        self.timer += 1
        self.timer %= self.period
        if self.timer == 0:
            self.tPeriod += 1
            self.tPeriod %= 2
        #canv.create_oval(self.x +320 - self.r, self.y +150 - self.r, self.x + 270 + self.r, self.y +150 + self.r, fill='white')

    def update(self):
        # if self.hp > 0:
        self.draw()
        if self.tPeriod == 1 and self.timer == 1:
            self.spawnBullet(False)

    def spawnBullet(self, event):
        if self.hp > 0:
            global boss_shots
            #time.sleep(3)
            if random.random() < 0.5:
                for i in range(3):
                    boss_shots.append(boss_bullet(p.x - 200, self.y, 0, 20))
                    boss_shots.append(boss_bullet(p.x - 340, self.y, 0, 20))
            else:
                for i in range(3):
                    boss_shots.append(boss_bullet(self.x + 25, self.y, 20, 20))
                    boss_shots.append(boss_bullet(self.x + 25, self.y, 10, 20))
                    boss_shots.append(boss_bullet(self.x + 25, self.y, -20, 20))
                    boss_shots.append(boss_bullet(self.x + 25, self.y, -10, 20))





class boss_bullet:
    def __init__(self, x, y, xVel, yVel):
        self.x = x + 360
        self.y = y + 500
        self.xVel = xVel
        self.yVel = yVel
        self.dead = False
        self.view = PhotoImage(file='bullet (2).png')

    def draw(self):
        canv.create_image(self.x, self.y,
                          image=self.view,
                          anchor=NW)

    def update(self):
        self.draw()
        self.x += self.xVel
        self.y += self.yVel
        if self.y + 25 >= canv.winfo_height() or self.y <= 0:
            self.dead = True

class explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dead = False
        self.sprites = [PhotoImage(file="explosion1.png"),
                        PhotoImage(file="explosion2.png"),
                        PhotoImage(file="explosion4.png"),
                        PhotoImage(file="explosion6.png"),
                        PhotoImage(file="explosion7.png"),
                        PhotoImage(file="explosion8.png"),
                        PhotoImage(file="explosion11.png"),
                        PhotoImage(file="explosion13.png"),
                        PhotoImage(file="explosion14.png"),
                        PhotoImage(file="explosion16.png"),
                        PhotoImage(file="explosion17.png"),
                        PhotoImage(file="explosion19.png"),
                        PhotoImage(file="explosion22.png"),
                        PhotoImage(file="explosion23.png"),]
        self.timer = 0
        # os.system("start Explosion.wav")

    def draw(self):
        canv.create_image(self.x, self.y - 25,
                          image=self.sprites[self.timer % len(self.sprites)],
                          anchor=NW)
        self.timer += 1
        # Killing the animation
        if self.timer >= len(self.sprites):
            self.dead = True




b = boss(-90, -200)

p = spaceship(0, 660)


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
            if shots[i].dead:
                del shots[i]
        except:
            pass

def drawShots_boos():
    for i in range(len(boss_shots)):
        try:
            boss_shots[i].update()
            if boss_shots[i].dead:
                del boss_shots[i]
        except:
            pass

def drawExplosions():
    for i in range(len(explosions)):
        try:
            explosions[i].draw()
            if explosions[i].dead:
                del explosions[i]
        except:
            pass

def drawBackground():
    pass


def draw():
    canv.delete("all")
    drawBackground()
    p.update()
    b.update()
    drawShots()
    drawShots_boos()
    drawExplosions()

    root.after(25, draw)



draw()
mainloop()
