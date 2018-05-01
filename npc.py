from os.path import *
from tkinter import *
from screen import *
from PIL import Image, ImageTk

_pathToSprites = "{0}{1}".format(dirname(__file__), "\\data\\pics\\")
class C_NPC():
    def __init__(self,name = "copy",speed = 1, posX = 0, posY = 0):
        self.name = name
        self.moveSpeed = speed
        self.attack = 0
        self.health = 1
        self.exp = 0
        self.expNext = 50
        self.posX = posX
        self.posY = posY
        self.spriteDownStand = "{0}spr_{1}_down.gif".format(_pathToSprites, name)
        self.spriteUpStand = "{0}spr_{1}_up.gif".format(_pathToSprites, name)
        self.spriteLeftStand = "{0}spr_{1}_left.gif".format(_pathToSprites, name)
        self.spriteRightStand = "{0}spr_{1}_right.gif".format(_pathToSprites, name)
        self.spriteStand = self.spriteDownStand
        self.screenImage = ImageTk.PhotoImage(Image.open(self.spriteStand))
    
    def movePosition(self,x,y):
        self.posX += x * self.moveSpeed
        self.posY += y * self.moveSpeed
        if (y>0): self.spriteStand = self.spriteDownStand
        elif (y<0): self.spriteStand = self.spriteUpStand
        elif (x>0): self.spriteStand = self.spriteRightStand
        elif (x<0): self.spriteStand = self.spriteLeftStand
        self.screenImage = ImageTk.PhotoImage(Image.open(self.spriteStand))

    def playerGo(self,X,Y):
        self.movePosition(X,Y)

class C_ENEMY(C_NPC):
    def __init__(self,name,speed,pX = 0,pY = 0,routine = None):
        super(C_ENEMY, self).__init__(name,speed,pX,pY)
        self.routine = routine