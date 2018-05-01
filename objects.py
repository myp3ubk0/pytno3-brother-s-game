from screen import *
from npc import *
from item import *
from random import *
from screen import *
from keys import keysDictionary

root = getScreenRoot()
npcCollection = {}
npcCollectionIndex = 0
itemCollection = {}
itemCollectionIndex = 0

def addNpc(npc):  
    global npcCollectionIndex
    npcCollection[npcCollectionIndex] = npc
    npcCollectionIndex = npcCollectionIndex + 1

def addItem(item):  
    global itemCollectionIndex
    itemCollection[itemCollectionIndex] = item
    itemCollectionIndex = itemCollectionIndex + 1


def checkObjectsCollision(obj1, obj2):
    if (obj1 == root):
        ax0 = obj1.winfo_x(); ay0 = obj1.winfo_y()
        ax1 = ax0 + obj1.winfo_width(); ay1 = ay0 + obj1.winfo_height()
    else:    
        ax0 = obj1.posX; ay0 = obj1.posY
        ax1 = ax0 + obj1.screenImage.width(); ay1 = ay0 + obj1.screenImage.height()
    bx0 = obj2.posX; by0 = obj2.posY
    bx1 = bx0 + obj2.screenImage.width(); by1 = by0 + obj2.screenImage.height()
    return (ax0 < bx0 and bx0 < ax1 and ay0 < by0 and by0 < ay1) or (ax0 < bx1 and bx1 < ax1 and ay0 < by1 and by1 < ay1)

def checkCollision():
    player = findPlayer()
    actionFlag = True
    if (type(player) == C_NPC and player.health > 0):
        for i in range(0, len (itemCollection)):
            obj = itemCollection[i]
            if (actionFlag):
                if (type(obj) == C_ITEM):
                    if (checkObjectsCollision(player,obj)):
                        itemCollection[i] = None
                        player.attack += 1  
                        actionFlag = False  
            for j in range(0, len (npcCollection)):
                if ((type(obj) == C_BULLET) and (type(npcCollection[j]) == C_NPC)):
                    if (obj.firing and checkObjectsCollision(npcCollection[j],obj) and npcCollection[j].name != "player"):
                        playerHit(j)
                        itemCollection[i] = None
        for i in range(0, len (npcCollection)):
            obj = npcCollection[i]
            if (actionFlag):
                if (type(npcCollection[i]) == C_NPC):
                    if (checkObjectsCollision(obj,player)):
                        playerHit()
                        actionFlag = False        

def playerHit(id = None):
    if (id == None):
        for i in range(0, len (npcCollection)):
            if ((type(npcCollection[i]) == C_NPC) and (npcCollection[i].name == "player")) : id = i
    npcCollection[id].health = npcCollection[id].health - 1
    if (npcCollection[id].health <= 0):
        npcCollection[id] = None

def findPlayer():
    for i in range(0, len (npcCollection)):
        if ((type(npcCollection[i]) == C_NPC) and (npcCollection[i].name == "player")):
            return npcCollection[i]
    return None

def _pressed(event):
    pressed[event.keysym] = True

def _released(event):
    pressed[event.keysym] = False

def playerMove(press):
    x=0;y=0
    if (press[keysDictionary["keyUp"]] and not press[keysDictionary["keyDown"]]): y=-1
    if (press[keysDictionary["keyDown"]] and not press[keysDictionary["keyUp"]]): y=1
    if (press[keysDictionary["keyLeft"]] and not press[keysDictionary["keyRight"]]): x=-1
    if (press[keysDictionary["keyRight"]] and not press[keysDictionary["keyLeft"]]): x=1
    findPlayer().playerGo(x,y)

def playerShoot(press):
    player = findPlayer()
    if (player.attack > 0):
        player.attack -=1; vx=0; vy=0
        if ((press[keysDictionary["keyUp"]] and not press[keysDictionary["keyDown"]]) or (player.spriteStand == player.spriteUpStand)): vy=-1
        if ((press[keysDictionary["keyDown"]] and not press[keysDictionary["keyUp"]]) or (player.spriteStand == player.spriteDownStand)): vy=1
        if ((press[keysDictionary["keyLeft"]] and not press[keysDictionary["keyRight"]]) or (player.spriteStand == player.spriteLeftStand)): vx=-1
        if ((press[keysDictionary["keyRight"]] and not press[keysDictionary["keyLeft"]]) or (player.spriteStand == player.spriteRightStand)): vx=1
        addItem(C_BULLET("bullet",5,True,player.posX,player.posY,vx,vy))
        
timeToCreateItem = 0; timeToShoot = 0; timeToCreateEnemy = 0
addNpc(C_NPC("player",3,500,500))
def animate():
    global timeToCreateItem, timeToShoot, timeToCreateEnemy
    player = findPlayer()
    if (pressed[keysDictionary["keyUp"]] or pressed[keysDictionary["keyDown"]] or pressed[keysDictionary["keyLeft"]] or pressed[keysDictionary["keyRight"]]): 
        if (type(player) == C_NPC): playerMove(pressed)
    if (pressed[keysDictionary["keyAttack"]]): 
        if ((type(player) == C_NPC) and (timeToShoot == 0)): playerShoot(pressed)
    for i in range(0, len (itemCollection)):
        if (type(itemCollection[i]) == C_BULLET):
            if (itemCollection[i].firing):
                itemCollection[i].throw() 
                timeToShoot +=1               
                if (not checkObjectsCollision(root,itemCollection[i])):
                    itemCollection[i] = None
    checkCollision()
    if (timeToCreateItem >= 100):
        timeToCreateItem = 0
        addItem(C_ITEM("bullet",randint(0,root.winfo_screenwidth()),randint(0,root.winfo_screenheight())))
    else: timeToCreateItem += 1
    if (timeToCreateEnemy >= 500):
        timeToCreateEnemy = 0
        rand = randint(0,1)
        if (rand == 0): 
            addNpc(C_NPC("wolf",1,randint(0,root.winfo_screenwidth()),randint(0,root.winfo_screenheight())))
        else: 
            addNpc(C_NPC("copy",1,randint(0,root.winfo_screenwidth()),randint(0,root.winfo_screenheight())))
    else: timeToCreateEnemy += 1
    if (timeToShoot >=10):
        timeToShoot = 0
    elif (timeToShoot !=0) : timeToShoot +=1
    #Update canvas
    canvas.delete("all")
    for i in range(0,len(itemCollection)):
        if ((type(itemCollection[i]) == C_ITEM) or (type(itemCollection[i]) == C_BULLET)): canvas.create_image(itemCollection[i].posX,itemCollection[i].posY,image = itemCollection[i].screenImage)
    for i in range(0,len(npcCollection)):
        if (type(npcCollection[i]) == C_NPC): canvas.create_image(npcCollection[i].posX,npcCollection[i].posY,image = npcCollection[i].screenImage)
    #End canvas update
    root.after(15, animate)
    
for char in [keysDictionary["keyUp"],keysDictionary["keyDown"],keysDictionary["keyLeft"], keysDictionary["keyRight"], keysDictionary["keyAttack"]]:
    root.bind("<KeyPress>", _pressed)
    root.bind("<KeyRelease>", _released)
    pressed[char] = False
  