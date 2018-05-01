from screen import *
from C_NPC import *
from C_ITEM import *
from random import *
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

addNpc(C_ENEMY("copy",4))
addNpc(C_ENEMY("wolf",4))
addNpc(C_ENEMY("copy",4))
addNpc(C_ENEMY("copy",4))
addNpc(C_ENEMY("copy",4))
addNpc(C_ENEMY("wolf",4))
addNpc(C_NPC("player",5))

def initAllObjects():
    for i in range(0, len(npcCollection)):
        npcCollection[i].screenObject.pack()
        npcCollection[i].screenObject.place(x = i*root.winfo_screenwidth()/len(npcCollection),y = i*root.winfo_screenheight()/len(npcCollection))
    for i in range(0,len(itemCollection)):
        itemCollection[i].screenObject.pack()
        itemCollection[i].screenObject.place(x = itemCollection[i].posX,y = itemCollection[i].posY)

def checkObjectsCollision(obj1, obj2):    
    ax0 = obj1.winfo_rootx(); ay0 = obj1.winfo_rooty()
    ax1 = ax0 + obj1.winfo_width(); ay1 = ay0 + obj1.winfo_height()
    bx0 = obj2.winfo_rootx(); by0 = obj2.winfo_rooty()
    bx1 = bx0 + obj2.winfo_width(); by1 = by0 + obj2.winfo_height()
    return (ax0 < bx0 and bx0 < ax1 and ay0 < by0 and by0 < ay1) or (ax0 < bx1 and bx1 < ax1 and ay0 < by1 and by1 < ay1)

def checkCollision():
    player = findPlayer()
    actionFlag = True
    if (not (player is None) and player.health > 0):
        for i in range(0, len (itemCollection)):
            if (actionFlag):
                if (not (itemCollection[i] is None)):
                    obj = itemCollection[i]
                    if (checkObjectsCollision(player.screenObject,obj.screenObject)):
                        if (not obj.firing):
                            obj.screenObject.destroy()
                            itemCollection[i] = None
                            player.attack += 1  
                            actionFlag = False  
            for j in range(0, len (npcCollection)):
                if ((not (itemCollection[i] is None)) and (not (npcCollection[j] is None))):
                    if (itemCollection[i].firing and checkObjectsCollision(npcCollection[j].screenObject,itemCollection[i].screenObject) and npcCollection[j].name != "player"):
                        playerHit(j)
                        obj.screenObject.destroy()
                        itemCollection[i] = None

        for i in range(0, len (npcCollection)):
            if (actionFlag):
                if (not (npcCollection[i] is None)):
                    obj = npcCollection[i]
                    if (checkObjectsCollision(player.screenObject,obj.screenObject)):
                        playerHit()
                        actionFlag = False        

def playerHit(id = -1):
    if (id == -1):
        for i in range(0, len (npcCollection)):
            if ((not (npcCollection[i] is None)) and (npcCollection[i].name == "player")) : id = i
    npcCollection[id].health = npcCollection[id].health - 1
    if (npcCollection[id].health <= 0):
        npcCollection[id].screenObject.destroy()
        npcCollection[id] = None

def findPlayer():
    for i in range(0, len (npcCollection)):
        if (not(npcCollection[i] is None) and (npcCollection[i].name == "player")):
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
        
timeToCreate = 0
timeToShoot = 0
def _animate():
    global timeToCreate, timeToShoot
    if (pressed[keysDictionary["keyUp"]] or pressed[keysDictionary["keyDown"]] or pressed[keysDictionary["keyLeft"]] or pressed[keysDictionary["keyRight"]]): 
        if not (findPlayer() is None): playerMove(pressed)
    if (pressed[keysDictionary["keyAttack"]]): 
        if ((not (findPlayer() is None)) and (timeToShoot == 0)): playerShoot(pressed)
    for i in range(0, len (itemCollection)):
        if (not (itemCollection[i] is None)):
            if (itemCollection[i].firing):
                itemCollection[i].throw()                
                if (not checkObjectsCollision(root,itemCollection[i].screenObject)):
                    itemCollection[i].screenObject.destroy()
                    itemCollection[i] = None
    checkCollision()
    if (timeToCreate >= 100):
        timeToCreate = 0
        addItem(C_ITEM("bullet",5,False,randint(0,root.winfo_screenwidth()),randint(0,root.winfo_screenheight())))
    else: timeToCreate += 1
    if (timeToShoot >=10 and timeToShoot != 0):
        timeToShoot = 0
    else: timeToShoot += 1
    weaponLabel.configure(text = "You DEAD" if (findPlayer() is None) else findPlayer().attack)
    weaponLabel.update()
    root.after(15, _animate)
    
for char in [keysDictionary["keyUp"],keysDictionary["keyDown"],keysDictionary["keyLeft"], keysDictionary["keyRight"], keysDictionary["keyAttack"]]:
    root.bind("<KeyPress>", _pressed)
    root.bind("<KeyRelease>", _released)
    pressed[char] = False

_animate()   