import numpy as np

BOARD_SIZE = 4

def getChild(node, type):
    rotations = getRotations(type)
    for i in range(0, rotations):
        node = rotateMatrixClockwise(node)

    if canMove(node):
        node = moveTiles(node)
        node = mergeTiles(node)
        node = addRandomTile(node)

    for j in range(0, (4 - rotations) % 4):
        node = rotateMatrixClockwise(node)

    return node


def moveTiles(node):
    # We want to work column by column shifting up each element in turn.
    for i in range(0, BOARD_SIZE):  # Work through our 4 columns.
        for j in range(0, BOARD_SIZE - 1):  # Now consider shifting up each element by checking top 3 elements if 0.
            while node[i][j] == 0 and sum(node[i][j:]) > 0:  # If any element is 0 and there is a number to shift we want to shift up elements below.
                for k in range(j, BOARD_SIZE - 1):  # Move up elements below.
                    node[i][k] = node[i][k + 1]  # Move up each element one.
                node[i][BOARD_SIZE - 1] = 0
    return node


def mergeTiles(node):
    for i in range(0, BOARD_SIZE):
        for k in range(0, BOARD_SIZE - 1):
            if node[i][k] == node[i][k + 1] and node[i][k] != 0:
                node[i][k] = node[i][k] * 2
                node[i][k + 1] = 0
                node = moveTiles(node)
    return node


def canMove(node):
    for i in range(0, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if node[i][j - 1] == 0 and node[i][j] > 0:
                return True
            elif (node[i][j - 1] == node[i][j]) and node[i][j - 1] != 0:
                return True

    return False


def addRandomTile(node):
    node = np.asarray(node)
    blankCoors = np.argwhere(node == 0)
    if len(blankCoors) == 0:
        return None
    randomCoor = blankCoors[np.random.randint(0, len(blankCoors))]
    randomTile = [2, 4][np.random.randint(10) == 9]
    node[randomCoor[0], randomCoor[1]] = randomTile
    return node.tolist()


def isGameOver(node):
    node = np.asarray(node)
    blankCoors = np.argwhere(node == 0)
    if len(blankCoors) == 0:
        return True
    return False


def rotateMatrixClockwise(node):
    for i in range(0, int(BOARD_SIZE / 2)):
        for k in range(i, BOARD_SIZE - i - 1):
            temp1 = node[i][k]
            temp2 = node[BOARD_SIZE - 1 - k][i]
            temp3 = node[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
            temp4 = node[k][BOARD_SIZE - 1 - i]

            node[BOARD_SIZE - 1 - k][i] = temp1
            node[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
            node[k][BOARD_SIZE - 1 - i] = temp3
            node[i][k] = temp4
    return node


def getRotations(k):
    if k == 'Up':
        return 0
    elif k == 'Down':
        return 2
    elif k == 'Left':
        return 1
    elif k == 'Right':
        return 3

def getInverseRotations(k):
    if k == 0:
        return 'Up'
    elif k == 2:
        return 'Down'
    elif k == 1:
        return 'Left'
    elif k == 3:
        return 'Right'

def convertToLinearMatrix(node):
    mat = []

    for i in range(0, BOARD_SIZE ** 2):
        mat.append(node[floor(i / BOARD_SIZE)][i % BOARD_SIZE])

    return mat

def checkIfCanGo(node):
    for i in range(0, BOARD_SIZE ** 2):
        if node[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
            return True

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE - 1):
            if node[i][j] == node[i][j + 1]:
                return True
            elif node[j][i] == node[j + 1][i]:
                return True
    return False

def floor(n):
    return int(n - (n % 1))
