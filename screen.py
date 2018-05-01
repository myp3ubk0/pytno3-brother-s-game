from tkinter import *

pressed = {}
screenRoot = Tk()

def getScreenRoot():
    return screenRoot

root = getScreenRoot()
root.title("GUI Test")
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))

canvas = Canvas(root, width = root.winfo_screenwidth(), height = root.winfo_screenheight(), bg = "green", bd=0, highlightthickness=0, relief='ridge')
canvas.pack()