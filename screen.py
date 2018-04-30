from tkinter import *

pressed = {}
screenRoot = Tk()

def getScreenRoot():
    return screenRoot

root = getScreenRoot()
root.title("GUI Test")
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))

weaponLabel = Label(text = "")
weaponLabel.pack(side = BOTTOM)

def exitButtonAction():
    exit()

exitButton = Button(text = "Exit", command=exitButtonAction)
exitButton.pack()