'''
Program that tries to emulate sand
'''

import pygame
import numpy as np
import time
from sys import exit


pygame.init()
pygame.display.set_caption('sandtest')

width, height = 1200, 840
screen = pygame.display.set_mode((width, height))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 100, 70
dimCW = width / nxC
dimCH = height / nyC
gameState = np.zeros((nxC, nyC))

pauseExect = False


while True:
    newGameState = np.copy(gameState)
    screen.fill(bg)

    ev = pygame.event.get()

    #time.sleep(0.3)
    # Constant grain generator
    '''
    genX = int(np.floor(nxC / 2))
    if gameState[genX, 0] == 0:
        newGameState[genX, 0] = 1
    '''
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        # Left-click to draw a sand particle
        if mouseClick[0]:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = (int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH)))
            if gameState[celX, celY] == 0:
                newGameState[celX, celY] = 1
        # Right-click to draw a water particle
        if mouseClick[2]:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = (int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH)))
            if gameState[celX, celY] == 0:
                newGameState[celX, celY] = 3
        # Wheel-click to draw a wood pixel
        if mouseClick[1]:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = (int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH)))
            if gameState[celX, celY] == 0:
                newGameState[celX, celY] = 5
            elif gameState[celX, celY] == 5:
                newGameState[celX, celY] = 0



        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for y in range(0, nyC):
        for x in range(0, nxC):

            if not pauseExect and y < nyC - 1:
                if gameState[x,y] == 1:
                    if gameState[x, y+1] == 0:
                        newGameState[x, y] = 0
                        newGameState[x, y+1] = 1
                    else:
                        if x < nxC - 1 and x > 0:
                            if gameState[x-1, y+1] == 0:
                                newGameState[x, y] = 0
                                newGameState[x-1, y+1] = 1
                            elif gameState[x+1, y+1] == 0:
                                newGameState[x, y] = 0
                                newGameState[x+1, y+1] = 1
                            else:
                                newGameState[x, y] = 2
                        else:
                            newGameState[x, y] = 2
                elif gameState[x, y] == 3:
                    if gameState[x, y+1] == 0:
                        newGameState[x, y] = 0
                        newGameState[x, y+1] = 3
                    else:
                        if x < nxC - 1 and x > 0:
                            if gameState[x-1, y+1] == 0 and x > 0:
                                newGameState[x, y] = 0
                                newGameState[x-1, y+1] = 3
                            elif gameState[x+1, y+1] == 0 and x < nxC - 1:
                                newGameState[x, y] = 0
                                newGameState[x+1, y+1] = 3
                            elif gameState[x-1, y] == 0 and x > 0:
                                #newGameState[x, y] = 0
                                newGameState[x-1, y] = 3
                            elif gameState[x+1, y] == 0 and x < nxC - 2:
                                #newGameState[x, y] = 0
                                newGameState[x+1, y] = 3
                            else:
                                newGameState[x, y] = 4
                        else:
                            newGameState[x, y] = 4

            # Creamos el polígono de cada celda a dibujar
            poly = [((x)*dimCW, y*dimCH),
                    ((x+1)*dimCW, y*dimCH),
                    ((x+1)*dimCW, (y+1)*dimCH),
                    ((x)*dimCW, (y+1)*dimCH)]

            # Y dibujamos la celda para cada par x e y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (192, 165, 101), poly, -1)
            elif newGameState[x,y] == 1 or newGameState[x,y] == 2:
                pygame.draw.polygon(screen, (192, 165, 101), poly, 0)
            elif newGameState[x,y] == 3 or newGameState[x,y] == 4:
                pygame.draw.polygon(screen, (77, 141, 238), poly, 0)
            elif newGameState[x,y] == 5:
                pygame.draw.polygon(screen, (126, 141, 102), poly, 0)



    gameState = np.copy(newGameState)
    pygame.display.flip()
