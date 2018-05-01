from os.path import *
from tkinter import *
from screen import *
from PIL import Image, ImageTk

_pathToSprites = "{0}{1}".format(dirname(__file__), "\\data\\pics\\")

class C_ITEM():

    def __init__(self,name = "bullet", posX = 0, posY = 0):
        self.name = name
        self.attack = 1
        self.posX = posX
        self.posY = posY
        self.sprite = "{0}spr_{1}.png".format(_pathToSprites, name)
        self.screenImage = ImageTk.PhotoImage(Image.open(self.sprite))


class C_BULLET(C_ITEM):
    def __init__(self,name = "bullet",speed = 5,firing = False, posX = 0, posY = 0,vx = 0,vy = 0):        
        super(C_BULLET, self).__init__(name,posX,posY)
        self.moveSpeed = speed
        self.firing = firing
        self.vX = vx
        self.vY = vy

    def throw(self):
        if (self.firing):
            self.posX = self.posX + self.vX * self.moveSpeed
            self.posY = self.posY + self.vY * self.moveSpeed

