from os.path import *
from tkinter import *

_pathToSprites = "{0}{1}".format(dirname(__file__), "\\data\\pics\\")

class C_ITEM():

    def __init__(self,name = "bullet",speed = 5,firing = False, posX = 0, posY = 0):
        self.name = name
        self.moveSpeed = speed
        self.attack = 1
        self.firing = firing
        self.posX = posX
        self.posY = posY
        self.sprite = "{0}spr_{1}.png".format(_pathToSprites, name)
        self.screenImage = PhotoImage(file = self.sprite)
        self.screenObject = Label(image = self.screenImage)
        self.screenObject.place(x=posX, y=posY)


class C_BULLET(C_ITEM):
    def __init__(self,name = "bullet",speed = 5,firing = False, posX = 0, posY = 0,vx = 0,vy = 0):
        self.name = name
        self.moveSpeed = speed
        self.attack = 1
        self.firing = firing
        self.posX = posX
        self.posY = posY
        self.sprite = "{0}spr_{1}.png".format(_pathToSprites, name)
        self.screenImage = PhotoImage(file = self.sprite)
        self.screenObject = Label(image = self.screenImage)
        self.screenObject.place(x=posX, y=posY)
        self.vX = vx
        self.vY = vy

    def throw(self):
        if (self.firing):
            self.posX = self.posX + self.vX * self.moveSpeed
            self.posY = self.posY + self.vY * self.moveSpeed
            self.screenObject.place(x=self.posX,y=self.posY) 
            self.screenObject.update()   

