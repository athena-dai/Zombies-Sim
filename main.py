import random

def makeModel(data):
    '''each component goes into dictionary data by setting:
    data["name of component"] = component

    each creature will be stored in a 3 element list: [row, col, human/zombie]
    this way, we know the creature's position and their status
    '''

    data["size"] = 20 #represents size of dimensions (# of rows and columns)
    data["creatures"]=[]
    for i in range(20): #make 20 humans
        human = [   random.randint(0,data["size"]-1),
                    random.randint(0,data["size"]-1),
                    "human"]
        data["creatures"].append(human)

    for i in range(1): #make 1 zombie
        zombie = [  random.randint(0, data["size"]-1),
                    random.randint(0, data["size"]-1),
                    "zombie"]
        data["creatures"].append(zombie)

def runRules(data, call):
    #Move zombies: Zombies can move 1 unit up, down, left or right
    for creature in data["creatures"]:
        if creature[2]=="zombie":
            moves = [ [-1,0], [1,0], [0,-1], [0,1] ] #up, down, left, right
            move = random.choice(moves)

            #update position based on move
            creature[0] += move[0]
            creature[1] += move[1]

            if not onscreen(creature,data):
                creature[0] -= move[0]
                creature[1]-= move[1]

    #Check if human becomes infected
    for creature in data["creatures"]:
        if creature[2] == "human":
            if borderingZombie(creature, data["creatures"]):
                creature[2] = "zombie"

def borderingZombie(human, creatureList):
    for creature in creatureList:
        if creature[2]=="zombie":
            #same row, bordering cols
            if creature[0]==human[0] and \
                abs(creature[1]-human[1])==1:
                    return True
            #same col, bordering rows
            elif creature[1]==human[1] and \
                abs(creature[0]-human[0])==1:
                    return True
    return False


def onscreen(creature, data): #returns True or False, checking if creature is in a legal row and a legal column
    return (0 <= creature[0] <= data["size"]-1) and \
            (0 <= creature[1] <= data["size"]-1)

def makeView(data, canvas):

    #Grid
    cellSize = 400 / data["size"]
    for row in range(data["size"]):
        for col in range(data["size"]):
            left = col * cellSize
            top = row * cellSize
            canvas.create_rectangle(left, top, left + cellSize, top + cellSize)

    #Draw Creatures
    for creature in data["creatures"]:
        [row, col, type]= creature
        left = col * cellSize
        top = row * cellSize
        if type == "human":
            color = "pink"
        elif type == "zombie":
            color = "green"
        canvas.create_rectangle(left, top, left + cellSize, top + cellSize, fill=color)

from tkinter import *
def timeLoop(data, canvas, call):
    runRules(data, call)

    canvas.delete(ALL)
    makeView(data, canvas)
    canvas.update()

    canvas.after(data["timeRate"], timeLoop, data, canvas, call+1)

def runSimulation(w, h, timeRate):
    data= {}
    data["timeRate"] = int(timeRate * 1000)
    makeModel(data)

    root = Tk()
    canvas = Canvas(root, width=w, height=h)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    makeView(data, canvas)

    canvas.after(data["timeRate"],timeLoop, data, canvas, 1)

    root.mainloop()

runSimulation(400,400,0.01)



