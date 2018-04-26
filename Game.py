
import sys
import pygame
from AI import *
from pygame.locals import *
from colours import *
from GridTools import *

PLY = 3
HEUR = 7

class Grid:
    def __init__(self):
        self.tileMatrix = np.zeros((4, 4), dtype=np.int)
        self.tileMatrix = addRandomTile(self.tileMatrix)
        self.tileMatrix = addRandomTile(self.tileMatrix)

    def setTileMatrix(self, matrix):
        self.tileMatrix = matrix

    def getTileMatrix(self):
        return self.tileMatrix

    def printMatrix(self, node):
        SURFACE.fill(frame)
        global BOARD_SIZE

        for j in range(0, BOARD_SIZE):
            for i in range(0, BOARD_SIZE):
                pygame.draw.rect(SURFACE, getColour(node[i][j]),
                                 (110*j + 10, 110*i + 110, 100, 100))
                if node[i][j] == 0:
                    label = tile_font.render("", 1, (255, 255, 255))
                elif node[i][j] == 2 or node[i][j] == 4:
                    label = tile_font.render(str(node[i][j]), 1, (120, 109, 102))
                else:
                    label = tile_font.render(str(node[i][j]), 1, (255, 255, 255))
                label2 = scorefont.render("AI", 1, (255, 255, 255))

                SURFACE.blit(label, (110*j+90 - [5, 23, 40, 60, 78, 90][len(str(node[i][j])) - 1],
                                     110*i + 175))
                SURFACE.blit(label2, (10, 20))

    def printGameOver(self, node):
        SURFACE.fill(frame)
        global BOARD_SIZE

        for j in range(0, BOARD_SIZE):
            for i in range(0, BOARD_SIZE):
                pygame.draw.rect(SURFACE, getColour(node[i][j]),
                                 (110*j + 10, 110*i + 110, 100, 100))
                if node[i][j] == 0:
                    label = tile_font.render("", 1, (255, 255, 255))
                elif node[i][j] == 2 or node[i][j] == 4:
                    label = tile_font.render(str(node[i][j]), 1, (120, 109, 102))
                else:
                    label = tile_font.render(str(node[i][j]), 1, (255, 255, 255))
                label2 = scorefont.render("Game Over:", 1, (255, 255, 255))

                SURFACE.blit(label, (110*j+90 - [5, 23, 40, 60, 78, 90][len(str(node[i][j])) - 1],
                                     110*i + 175))
                SURFACE.blit(label2, (10, 20))



DEFAULT_SCORE = 2
BOARD_SIZE = 4

pygame.init()

SURFACE = pygame.display.set_mode((450, 550), 0, 32)
pygame.display.set_caption("2048")
tile_font = pygame.font.SysFont("dejavuserif", 30)
scorefont = pygame.font.SysFont("dejavuserif", 50)
action_keys = {}
action_keys[pygame.K_UP] = 'Up'
action_keys[pygame.K_RIGHT] = 'Right'
action_keys[pygame.K_DOWN] = 'Down'
action_keys[pygame.K_LEFT] = 'Left'
undoMat = []

g = Grid()
node = g.getTileMatrix()
g.printMatrix(node)
pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if checkIfCanGo(node):
            if event.type == KEYDOWN:
                if event.key in action_keys:
                    node = getChild(node, action_keys[event.key])

                elif event.key == pygame.K_h:
                    while checkIfCanGo(node):
                        move = AI(PLY).getMaxAction(node, PLY, HEUR)
                        node = getChild(node, move)
                        g.printMatrix(node)
                        pygame.display.update()
                    g.printGameOver(node)
                    break

                elif event.key == pygame.K_a:
                    move = AI(PLY).getMaxAction(node, PLY, HEUR)
                    node = getChild(node, move)

                g.printMatrix(node)


        else:
            g.printGameOver(node)

        if event.type == KEYDOWN:
            if event.key == pygame.K_r:
                g = Grid()
                node = g.getTileMatrix()
                g.printMatrix(node)

    pygame.display.update()

