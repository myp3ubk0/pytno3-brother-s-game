from os.path import *
from tkinter import *

_pathToSprites = "{0}{1}".format(dirname(__file__), "\\data\\pics\\")
class C_NPC():
    def __init__(self,name = "copy",speed = 1):
        self.name = name
        self.moveSpeed = speed
        self.attack = 0
        self.health = 1
        self.exp = 0
        self.expNext = 50
        self.posX = 0
        self.posY = 0
        self.spriteDownStand = "{0}spr_{1}_down.png".format(_pathToSprites, name)
        self.spriteUpStand = "{0}spr_{1}_up.png".format(_pathToSprites, name)
        self.spriteLeftStand = "{0}spr_{1}_left.png".format(_pathToSprites, name)
        self.spriteRightStand = "{0}spr_{1}_right.png".format(_pathToSprites, name)
        self.spriteStand = self.spriteDownStand
        self.screenImage = PhotoImage(file = self.spriteStand)
        self.screenObject = Label(image = self.screenImage)
    
    def movePosition(self,x,y):
        self.posX += x * self.moveSpeed
        self.posY += y * self.moveSpeed
        if (y>0): self.spriteStand = self.spriteDownStand
        elif (y<0): self.spriteStand = self.spriteUpStand
        elif (x>0): self.spriteStand = self.spriteRightStand
        elif (x<0): self.spriteStand = self.spriteLeftStand

    def getPosition(self,x,y):
        self.posX = x
        self.posY = y

    def playerGo(self,X,Y):
        self.getPosition(self.screenObject.winfo_rootx(),self.screenObject.winfo_rooty())
        self.movePosition(X,Y)
        self.screenImage = PhotoImage(file = self.spriteStand)
        self.screenObject.configure(image = self.screenImage)
        self.screenObject.image = self.screenImage
        self.screenObject.place(x = self.posX,y = self.posY)

class C_ENEMY(C_NPC):
    def __init__(self,name,speed,routine = None):
        super(C_ENEMY, self).__init__(name,speed)
        self.routine = routine