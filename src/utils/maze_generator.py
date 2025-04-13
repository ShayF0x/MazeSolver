import random
from utils.tkinter_process import *
from widget.cell import CellState
from widget.cell import ViewMode
from model.model import Model

# random fusion

def breakWall(x1,y1,x2,y2, xMax, yMax):
    milieu = [ x1+x2+1, y1+y2+1 ]
    murs[milieu[1]][milieu[0]] = 1
    return (milieu[0],milieu[1])

def generate_labyrinthe(xMax, yMax, view_cells, model: Model):    
    global murs
    global cells
    global labyrinthe
    cells = view_cells

    directionX = {'N':0,'S':0,'E':1,'O':-1}
    directionY = {'N':1,'S':-1,'E':0,'O':0}

    labyrinthe = [[(x+xMax*y) for x in range(xMax)] for y in range(yMax)]

    murs = [[0 for x in range(2*xMax+1)] for y in range(2*yMax+1)]
    for y in range(len(murs)-1):
        for x in range(len(murs[y])-1):
            if x % 2 != 0 and y % 2 != 0:
                murs[y][x] = 1
                update_cell(x, y, xMax, yMax)

    openedWall = 0



    while openedWall < xMax*yMax-1:

        if(model.on_pause.get()):
            tkpause(model.on_pause)

        (rx, ry) = ((random.randrange(xMax)), (random.randrange(yMax)))
        direction = random.choice(['N','S','O','E'])
        nx = rx + directionX[direction]
        ny = ry + directionY[direction]
        if nx >= 0 and nx < xMax and ny >= 0 and ny < yMax:

            if labyrinthe[ny][nx] != labyrinthe[ry][rx]:

                wall_coord = breakWall(rx, ry, nx, ny, xMax, yMax)
                update_cell(wall_coord[0], wall_coord[1], xMax, yMax)
                var = labyrinthe[ny][nx]
                for y in range(yMax):
                    for x in range(xMax):
                        if labyrinthe[y][x] == var:
                            labyrinthe[y][x] = labyrinthe[ry][rx]
                rx, ry = nx, ny
                openedWall += 1

        if cells[(0,0)].mode is ViewMode.MUSEUM:
            tksleep(0.008*model.speed_var.get())
        elif cells[(0,0)].mode is ViewMode.CLASSIC:
            tksleep(0.05*model.speed_var.get())
            for y in range(len(murs)):             # update cells
                for x in range(len(murs[y])):
                    update_cell(x,y,xMax,yMax)

def update_cell(x, y, xMax, yMax):
    if murs[y][x] == 0:
        cells[(x,y)].set_cell_state(CellState.FILLED)
    elif murs[y][x] == 1:
        idx = labyrinthe[int((y-1)/2)][int((x-1)/2)]
        color = genColor(idx,xMax, yMax)
        cells[(x,y)].set_cell_state(CellState.EMPTY)
        cells[(x,y)].config(bg=color)

def genColor(idx, xMax, yMax):
    idxMax = xMax*yMax-1
    intColor = int((idx*(256**3-1))/idxMax)
    blue =  intColor & 255
    green = (intColor >> 8) & 255
    red =   (intColor >> 16) & 255
    rgbColor = red, green, blue
    hex_color = '#%02x%02x%02x' % rgbColor

    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + 100 for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])
