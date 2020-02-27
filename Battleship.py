# Battleship
# By Joe Lux

import pygame, sys
from pygame.locals import *

from Player import Player
from Ship import Ship

pygame.init()

FPS = 30 # Frame rate for the game
fpsClock = pygame.time.Clock() # Clock 
turn = True
firstThree = True
initialized = False
wait = False
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 720 # size of window's height in pixels

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0, 40)
YELLOW = (255, 255, 0, 30)
BLUE = (0, 0, 255)
FOG = (255, 255, 255, 70)
HIT = (255, 0, 0, 30)

# Letters
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
letterObjectArray = []
letterObjectRectArray = []
numberObjectArray = []
numberObjectRectArray = []

DISPLAYSURF = pygame.display.set_mode((640, 720), 0, 32)
pygame.display.set_caption('Battleship')
BACKGROUNDIMAGE = pygame.image.load('Ocean.jpg')

# Render text for the user info screen
fontObj = pygame.font.Font('freesansbold.ttf', 32)

# Render all of the text for the letters and numbers along the sides
for l in range(10):
    letterTextSurfaceObj = fontObj.render(letters[l], True, WHITE)
    numberTextSurfaceObj = fontObj.render(str(l + 1), True, WHITE)

    letterTextRectObj = letterTextSurfaceObj.get_rect()
    letterTextRectObj.center = (70 + l * 60, 20)

    numberTextRectObj = numberTextSurfaceObj.get_rect()
    numberTextRectObj.center = (20, 70 + l * 60)

    letterObjectArray.append(letterTextSurfaceObj)
    letterObjectRectArray.append(letterTextRectObj)

    numberObjectArray.append(numberTextSurfaceObj)
    numberObjectRectArray.append(numberTextRectObj)


# Create the two player boards
playerOneBoard = Player()
playerTwoBoard = Player()

player = playerOneBoard

#The first ship assignment
ship = Ship("carrier", 5, None, "right")

# Mouse coordinates
mousex = 0
mousey = 0

def initialize():
    global mousex
    global mousey
    # Event Handling
    mouseClicked = False

    drawShips()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = True
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                if ship.direction == "right":
                    ship.direction = "down"
                else:
                    ship.direction = "right"
                

    mousedBox = getBoxAtMousePos(mousex, mousey)
    if mousedBox[0] != None and mousedBox[1] != None:
        handleInitializedEvent(mousedBox, mouseClicked)
    
def handleInitializedEvent(boxCoords, clicked):
    global ship

    posX = int((boxCoords[0] - 40) / 60)
    posY = int((boxCoords[1] - 40) / 60)

    if ship.direction == "right" and posX > 10 - ship.length:
        posX = 10 - ship.length
    if ship.direction == "down" and posY > 10 - ship.length:
        posY = 10 - ship.length

    if clicked:
        if canShipBePlaced(posX, posY):
            ship.pos = (posX, posY)
            player.addShip(ship)
            assignNextShip()
    else:
        highlightShip((40 + posX * 60, 40 + posY * 60))

def canShipBePlaced(posX, posY):
    for i in range(ship.length):
        if ship.direction == "right":
            if player.board[posX + i][posY] != 0:
                return False
        else:
            if player.board[posX][posY + i] != 0:
                False
    return True

def assignNextShip():
    global ship
    global firstThree
    global turn
    global player
    global initialized

    if ship.length > 2:
        
        if ship.length == 3 and firstThree:
                firstThree = False
                ship = Ship(getNameFromLength(ship.length), ship.length, None, "right") 
        else:
            ship = Ship(getNameFromLength(ship.length), ship.length - 1, None, "right")
    elif turn:
        turn = False
        player = playerTwoBoard
        firstThree = True
        ship = Ship("carrier", 5, None, "right")
    else:
        initialized = True
        turn = True

def getNameFromLength(length):
    if length == 5:
        return "carrier"
    elif length == 4:
        return "battleship"
    elif length == 3 and firstThree:
        return "cruiser"
    elif length == 3:
        return "submarine"
    else:
        return "destroyer"

def highlightShip(boxCoords):
    alphaSurface = DISPLAYSURF.convert_alpha()
    for i in range(ship.length):
        if ship.direction == "right":
            pygame.draw.rect(alphaSurface, YELLOW, (boxCoords[0] + i * 60, boxCoords[1], 60, 60))
        else:
            pygame.draw.rect(alphaSurface, YELLOW, (boxCoords[0], boxCoords[1] + i * 60, 60, 60))
    DISPLAYSURF.blit(alphaSurface, (0,0))

def playerTurn():
    # Player Turn Assignment
    global mousex, mousey
    global player
    mouseClicked = False

    drawFogAndHits()

    if turn:
        player = playerTwoBoard
    else: 
        player = playerOneBoard

    # Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = True

    mousedBox = getBoxAtMousePos(mousex, mousey)
    if mousedBox[0] != None and mousedBox[1] != None:
        handleEvent(mousedBox, mouseClicked)

def handleEvent(boxCoords, clicked):
    global turn 
    posX = int((boxCoords[0] - 40) / 60)
    posY = int((boxCoords[1] - 40) / 60)
    #if player.board[posX][posY] >= 0:
    
    if clicked:
        
        if player.checkHit((posX, posY)):
            drawText("Hit!")
        else:
            drawText("Miss...")
        turn = not turn
    else:
        highlightBox(boxCoords)

def highlightBox(boxCoords):
    alphaSurface = DISPLAYSURF.convert_alpha()
    pygame.draw.rect(alphaSurface, YELLOW, (boxCoords[0], boxCoords[1], 60, 60))
    DISPLAYSURF.blit(alphaSurface, (0,0))

def getBoxAtMousePos(mousex, mousey):
    for boxx in range(40, 640, 60):
        for boxy in range(40, 640, 60):
            boxRect = pygame.Rect(boxx, boxy, 60, 60)
            if boxRect.collidepoint(mousex, mousey):
                return (boxx, boxy)
    return (None, None)

def drawText(text):
    pygame.draw.rect(DISPLAYSURF, BLACK, (0, 640, 640, 80))
    pygame.draw.rect(DISPLAYSURF, WHITE, (5, 645, 630, 70))

    textSurfaceObj = fontObj.render(text, True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (320, 680)

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def drawInitialBoard():
    # Draw Background
    DISPLAYSURF.blit(BACKGROUNDIMAGE, (0, 0))

    # Draw lines 
    for i in range(40, 640, 60):
        pygame.draw.line(DISPLAYSURF, BLACK, (i, 0), (i, 640))
        pygame.draw.line(DISPLAYSURF, BLACK, (0, i), (640, i))

    # Draw letters and numbers
    for t in range(10):
        DISPLAYSURF.blit(letterObjectArray[t], letterObjectRectArray[t])
        DISPLAYSURF.blit(numberObjectArray[t], numberObjectRectArray[t])

    # Draw the bottom User Info Screen
    if turn:
        drawText("Player  One\'s  Turn")
    else:
        drawText("Player  Two\'s  Turn")

def drawShips():
    alphaSurface = DISPLAYSURF.convert_alpha()
    for row in range(10):
        for col in range(10):
            if player.board[row][col] > 0:
                pygame.draw.rect(alphaSurface, GREEN, (40 + row * 60, 40 + col * 60, 60, 60))
    DISPLAYSURF.blit(alphaSurface, (0,0))

def drawFogAndHits():
    alphaSurface = DISPLAYSURF.convert_alpha()
    for row in range(10):
        for col in range(10):
            if player.board[row][col] >= 0:
                pygame.draw.rect(alphaSurface, FOG, (40 + row * 60, 40 + col * 60, 60, 60))
            elif player.board[row][col] > -6:
                pygame.draw.rect(alphaSurface, HIT, (40 + row * 60, 40 + col * 60, 60, 60))
                
    DISPLAYSURF.blit(alphaSurface, (0,0))

# main game loop
while True:
    drawInitialBoard()

    if initialized:
        playerTurn()
    else:
        initialize()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
    pygame.display.update()
    fpsClock.tick(FPS)  