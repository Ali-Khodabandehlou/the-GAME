#==========================================
#
# project name: the GAME
# 
# developers: 
#   dev1name
#   dev2name
#   dev3name
#
# supervisor:
#   sup1name
#   sup2name
#
# project start date: 27/01/2020
# last edited:        30/01/2020
#
# Tehran University, statistics department
#
#==========================================

#import requiered libraries
import pygame
import sys, os, copy

#run pygame engine
pygame.init()


#global variables
#states variables save old grid and player states
gridMoves = []
playerMoves = []
#level
level = 0
winState = False
colors = {'RED':(255, 0, 0),
          'GREEN':(0, 255, 0),
          'BLUE':(0, 0, 255),
          'CYAN':(0, 255, 255),
          'VIOLET':(255, 0, 255),
          'YELLOW':(255, 255, 0),
          'WHITE':(255, 255, 255),
          'BLACK':(0, 0, 0),}
"""this part was used for basic graphics
gridColor = {-1:colors['BLACK'],
             0:colors['GREEN'],
             1:colors['BLUE'],
             2:colors['VIOLET'],
             3:colors['YELLOW']}
"""
directions = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UNDO']
#font face
fontFile = 'files/fonts/timesi.ttf'
basicFont = pygame.font.Font(fontFile, 48)
#board size
gameBoardSize = [10, 10]
tileSize = [60, 60]
isRunning = True
#files
levelMapDir = 'files/maps/'
#graphics
logoIcon = pygame.image.load('files/image/player.png')
wallImage = pygame.image.load('files/image/wall.png')
wallStretchedImage = pygame.transform.scale(wallImage, tileSize)
tileImage = pygame.image.load('files/image/groundtile.png')
tileStretchedImage = pygame.transform.scale(tileImage, tileSize)
boxImage = pygame.image.load('files/image/box.png')
boxStretchedImage = pygame.transform.scale(boxImage, tileSize)
platformImage = pygame.image.load('files/image/platform.png')
platformStretchedImage = pygame.transform.scale(platformImage, tileSize)
playerImage = pygame.image.load('files/image/player.png')
playerStretchedImage = pygame.transform.scale(playerImage, tileSize)


#this function reads <level>.txt file and gets data for each level
def load():
    global isRunning
    levelMapFile = levelMapDir + str(level) + '.txt'
    if os.path.exists(levelMapFile):
        file = open(levelMapFile, 'r')
        lines = file.readlines()
        data = []
        grid = []
        player = []
        win = []
        
        for line in lines:
            data.append(line.split())
        
        for i in range(len(data)):
            if data[i][0] == 'l':
                pass
            elif data[i][0] == 'g':
                tempLine = []
                for j in range(len(data[i])):
                    if j == 0:
                        continue
                    tempLine.append(int(data[i][j]))
                grid.append(tempLine)
            elif data[i][0] == 'p':
                tempLine = []
                for j in range(len(data[i])):
                    if j == 0:
                        continue
                    player.append(int(data[i][j]))
            elif data[i][0] == 'w':
                tempLine = []
                for j in range(len(data[i])):
                    if j == 0:
                        continue
                    win.append(int(data[i][j]))
            
        return grid, player, win
    else:
       sys.exit()
       return False, False, False


"""this part was used for debugging
#only to print Grid
def printGrid(grid):
    for row in grid:
        print(row)
"""

#this function draws level map
def drawBoard(window, boardGrid):
    for i in range(gameBoardSize[0]):
        for j in range(gameBoardSize[1]):
            drawTile(window, i*tileSize[0], j*tileSize[1], tileSize, boardGrid[i][j])


#this function shows any message given on screen
def messageShow(window, text, time = 2000):
    message = basicFont.render(text, True, colors['WHITE'])
    messageRect = message.get_rect()
    messageRect.centerx = window.get_rect().centerx
    messageRect.centery = window.get_rect().centery
    pygame.draw.rect(window, colors['RED'], (messageRect.left - 20, messageRect.top - 20,
                                   messageRect.width + 40, messageRect.height + 40))
    window.blit(message, messageRect)
    pygame.display.update()
    pygame.time.wait(time)
    pass

#this function draws a single tile
def drawTile(window, yPos, xPos, size, itemType):
    tile = pygame.Rect(xPos, yPos, size[0], size[1])
    if itemType == -1:
        window.blit(wallStretchedImage, tile)
    elif itemType == 0:
        window.blit(tileStretchedImage, tile)
    elif itemType == 1:
        window.blit(boxStretchedImage, tile)
    elif itemType == 2:
        window.blit(platformStretchedImage, tile)
    elif itemType == 3:
        if winState == True:
            window.blit(platformStretchedImage, tile)
        else:
            window.blit(tileStretchedImage, tile)
        window.blit(playerStretchedImage, tile)


#this function checks possible moves of player and updates player position by calling the forward() function
def movePlayer(mapGrid, player, direction):
    global winState, gridMoves, playerMoves
    k = 1
    playerX = player[0]
    playerY = player[1]
    if direction == directions[0]:
        for i in range(playerX, 0, -1):
            if mapGrid[i-1][playerY] == -1:
                return mapGrid, player
            elif mapGrid[i-1][playerY] == 0:
                saveState(mapGrid, player)
                mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                break
            elif mapGrid[i-1][playerY] == 1:
                k += 1
            elif mapGrid[i-1][playerY] == 2:
                if k == 1:
                    winState = True
                    mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                    break
                else:
                    return mapGrid, player
            else:
                return mapGrid, player
        player[0] -= 1
    
    if direction == directions[1]:
        for i in range(playerX, len(mapGrid), 1):
            if mapGrid[i+1][playerY] == -1:
                return mapGrid, player
            elif mapGrid[i+1][playerY] == 0:
                saveState(mapGrid, player)
                mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                break
            elif mapGrid[i+1][playerY] == 1:
                k += 1
            elif mapGrid[i+1][playerY] == 2:
                if k == 1:
                    winState = True
                    mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                    break
                else:
                    return mapGrid, player
            else:
                return mapGrid, player
        player[0] += 1
    
    if direction == directions[2]:
        for i in range(playerY, 0, -1):
            if mapGrid[playerX][i-1] == -1:
                return mapGrid, player
            elif mapGrid[playerX][i-1] == 0:
                saveState(mapGrid, player)
                mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                break
            elif mapGrid[playerX][i-1] == 1:
                k += 1
            elif mapGrid[playerX][i-1] == 2:
                if k == 1:
                    winState = True
                    mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                    break
                else:
                    return mapGrid, player
            else:
                return mapGrid, player
        player[1] -= 1
    
    if direction == directions[3]:
        for i in range(playerY, len(mapGrid), 1):
            if mapGrid[playerX][i+1] == -1:
                return mapGrid, player
            elif mapGrid[playerX][i+1] == 0:
                saveState(mapGrid, player)
                mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                break
            elif mapGrid[playerX][i+1] == 1:
                k += 1
            elif mapGrid[playerX][i+1] == 2:
                if k == 1:
                    winState = True
                    mapGrid = forward(mapGrid, playerX, playerY, direction, k)
                    break
                else:
                    return mapGrid, player
            else:
                return mapGrid, player
        player[1] += 1
    if direction == directions[4]:
        tempGrid, tempPlayer = undoMove()
        if tempGrid != False or tempPlayer != False:
            mapGrid = tempGrid
            player = tempPlayer
    
    return mapGrid, player


#this function moves the player and boxes forward to the given direction
def forward(mapGrid, xPos, yPos, direction, steps):
    if direction == directions[0]:
        for i in range(steps, 0, -1):
            mapGrid[xPos-i][yPos] = mapGrid[xPos-i+1][yPos]
            mapGrid[xPos-i+1][yPos] = 0
    if direction == directions[1]:
        for i in range(steps, 0, -1):
            mapGrid[xPos+i][yPos] = mapGrid[xPos+i-1][yPos]
            mapGrid[xPos+i-1][yPos] = 0
    if direction == directions[2]:
        for i in range(steps, 0, -1):
            mapGrid[xPos][yPos-i] = mapGrid[xPos][yPos-i+1]
            mapGrid[xPos][yPos-i+1] = 0
    if direction == directions[3]:
        for i in range(steps, 0, -1):
            mapGrid[xPos][yPos+i] = mapGrid[xPos][yPos+i-1]
            mapGrid[xPos][yPos+i-1] = 0
    
    return mapGrid


#this function saves previous states before any move
def saveState(mapGrid, player):
    global gridMoves, playerMoves
    gridMoves.append(copy.deepcopy(mapGrid))
    playerMoves.append(copy.deepcopy(player))


#this function undos the last move
def undoMove():
    global gridMoves, playerMoves
    if len(gridMoves) == 0 or len(playerMoves) == 0:
        return False, False
    else:
        mapGrid = gridMoves[-1]
        player = playerMoves[-1]
        gridMoves.pop(-1)
        playerMoves.pop(-1)
        return mapGrid, player


def main():
    #set initial settings and variables
    global level, winState, gridMoves, playerMoves, isRunning
    window = pygame.display.set_mode((gameBoardSize[0]*tileSize[0], gameBoardSize[1]*tileSize[1]))
    pygame.display.set_caption('the GAME')
    pygame.display.set_icon(logoIcon)
    
    pygame.display.update()
    direction = 0
    
    grid, playerPos, winPos = load()
    
    #this while loop stands until player presses 'x' key or 'escape' key
    #all events will be handled from here
    messageShow(window, 'welcome to "the GAME"')
    while isRunning:
        drawBoard(window, grid)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_x or event.key == pygame.K_ESCAPE:
                    isRunning = False
                    break
                elif event.key == pygame.K_z:
                    direction = directions[4]
                
                elif event.key == pygame.K_UP:
                    direction = directions[0]
                elif event.key == pygame.K_DOWN:
                    direction = directions[1]
                elif event.key == pygame.K_LEFT:
                    direction = directions[2]
                elif event.key == pygame.K_RIGHT:
                    direction = directions[3]

                else:
                    continue
                
                grid, playerPos = movePlayer(grid, playerPos, direction)
                
                drawBoard(window, grid)
                pygame.display.update()
                
                #here checks win state with every move, if player was on the platform, game will proceed to the next level
                if playerPos == winPos:
                    message = 'level ' + str(level) + ' completed'
                    level += 1
                    gridMoves.clear()
                    playerMoves.clear()
                    messageShow(window, message, 2000)
                    winState = False
                    grid, playerPos, winPos = load()
                    
                    if grid == False:
                        isRunning = False
                        break
                    continue
        
        pygame.time.wait(200)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()