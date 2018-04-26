import numpy as np
import math
BOARD_SIZE = 4

def getChild(node, move):
    temp = np.copy(node)
    node = moveTiles(node, move)
    node = mergeTiles(node, move)
    if not np.equal(temp, node).all():
        node = addRandomTile(node)
    return node

def moveTiles(node, move):
    if move == 'Right':
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - 2, -1, -1):
                if node[i, j] == 0:
                    continue
                temp_j = j
                while temp_j <= BOARD_SIZE - 2:
                    if not node[i, temp_j + 1] == 0:
                        break
                    temp = node[i, temp_j]
                    node[i, temp_j] = node[i, temp_j + 1]
                    node[i, temp_j + 1] = temp
                    temp_j += 1
    elif move == 'Down':
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE - 2, -1, -1):
                if node[i, j] == 0:
                    continue
                temp_i = i
                while temp_i <= BOARD_SIZE - 2:
                    if not node[temp_i + 1, j] == 0:
                        break
                    temp = node[temp_i, j]
                    node[temp_i, j] = node[temp_i + 1, j]
                    node[temp_i + 1, j] = temp
                    temp_i += 1
        pass
    elif move == 'Left':
        for i in range(BOARD_SIZE):
            for j in range(1, BOARD_SIZE):
                if node[i, j] == 0:
                    continue
                temp_j = j
                while temp_j > 0:
                    if not node[i, temp_j - 1] == 0:
                        break
                    temp = node[i, temp_j]
                    node[i, temp_j] = node[i, temp_j - 1]
                    node[i, temp_j - 1] = temp
                    temp_j -= 1
    elif move == 'Up':
        for j in range(BOARD_SIZE):
            for i in range(1, BOARD_SIZE):
                if node[i, j] == 0:
                    continue
                temp_i = i
                while temp_i > 0:
                    if not node[temp_i - 1, j] == 0:
                        break
                    temp = node[temp_i, j]
                    node[temp_i, j] = node[temp_i - 1, j]
                    node[temp_i - 1, j] = temp
                    temp_i -= 1
    return node

# this function merges tiles which have the same value
def mergeTiles(grid, direction):

    # direction validity check
    if direction not in ["Up", "Down", "Left", "Right"]:
        print("ERR: Unknown direction for merge.")
        return -1

    # merge in up direction
    elif direction == "Up":

        # for each column
        for colNum in range(4):
            column = grid[:, colNum]

            # for each row in a column starting from top
            for rowNum in range(3):
                if column[rowNum] == 0 or column[rowNum] != column[rowNum + 1]:
                    continue
                else:
                    grid[rowNum, colNum] *= 2
                    grid[rowNum + 1, colNum] = 0

    # merge in down direction
    elif direction == "Down":

        # for each column
        for colNum in range(4):
            column = grid[:, colNum]

            # for each row in a column starting from bottom
            for rowNum in range(3, 0, -1):
                if column[rowNum] == 0 or column[rowNum] != column[rowNum - 1]:
                    continue
                else:
                    grid[rowNum, colNum] *= 2
                    grid[rowNum - 1, colNum] = 0

    # merge in left direction
    elif direction == "Left":

        # for each row
        for rowNum in range(4):
            row = grid[rowNum, :]

            # for each column in a row starting from left
            for colNum in range(3):
                if row[colNum] == 0 or row[colNum] != row[colNum + 1]:
                    continue
                else:
                    grid[rowNum, colNum] *= 2
                    grid[rowNum, colNum + 1] = 0

    # merge in right direction
    elif direction == "Right":

        # for each row
        for rowNum in range(4):
            row = grid[rowNum, :]

            # for each column in a row starting from right
            for colNum in range(3, 0, -1):
                if row[colNum] == 0 or row[colNum] != row[colNum - 1]:
                    continue
                else:
                    grid[rowNum, colNum] *= 2
                    grid[rowNum, colNum - 1] = 0

    # paranoia
    else:
        print("Something went wrong, blame the neutrinos.")
        return -1
    grid = moveTiles(grid, direction)
    return grid

def canMove(node, move):
    temp = np.copy(node)
    node = moveTiles(node, move)
    node = mergeTiles(node, move)
    if np.equal(node, temp).all():
        return False
    return True

def addRandomTile(node):
    blankCoors = np.argwhere(node == 0)
    if len(blankCoors) == 0:
        return None
    randomCoor = blankCoors[np.random.randint(0, len(blankCoors))]
    randomTile = [2, 4][np.random.randint(10) == 9]
    node[randomCoor[0], randomCoor[1]] = randomTile
    return node


def checkIfCanGo(node):
    if np.count_nonzero(node) == BOARD_SIZE*BOARD_SIZE:
        for move in ['Right', 'Down', 'Left', 'Up']:
            if canMove(node, move):
                return True
        return False
    return True

def checkInc(listToCheck):
    return all(x <= y for x, y in zip(listToCheck, listToCheck[1:]))

def checkDec(listToCheck):
    return all(x >= y for x, y in zip(listToCheck, listToCheck[1:]))

def checkMonotonicity(vector):
    return all(x <= y for x, y in zip(vector, vector[1:])) or all(x >= y for x, y in zip(vector, vector[1:]))

def gradeMonotonicityOfVector(vector):
    if checkInc(vector) or checkDec(vector):
        return 100 - (getSumOfPairwiseLogDistances(vector))
    else:
        return 0

def getFarthestPosition(value, vector):
    current = value
    vectorWalker = 0
    while vectorWalker < len(vector) and current == vector[vectorWalker]:
        vectorWalker += 1
        current *= 2
    return vectorWalker

def getSumOfPairwiseLogDistances(vector):
    sumOfPairwiseDistances = 0
    for elementNum in range(len(vector) - 1):
        if vector[elementNum] > 0 and vector[elementNum + 1] > 0:
            sumOfPairwiseDistances += abs(math.log(vector[elementNum], 2) - math.log(vector[elementNum + 1], 2))
    return sumOfPairwiseDistances

def getSumOfPairwiseDistances(vector):
    sumOfPairwiseDistances = 0
    for elementNum in range(len(vector) - 1):
        sumOfPairwiseDistances += abs(vector[elementNum] - vector[elementNum + 1])
    return sumOfPairwiseDistances

def n_max(arr, n):
    indices = arr.ravel().argsort()[-n:]
    indices = (np.unravel_index(i, arr.shape) for i in indices)
    return [i for i in indices][::-1]

def checkIfSnake(matrix):
    for rowNum in range(4):
        if (rowNum in [0, 2] and not checkDec(matrix[rowNum, :])) or (rowNum in [1, 3] and not checkInc(matrix[rowNum, :])):
            return False
    for colNum in range(4):
        if not checkInc(matrix[:, colNum]):
            return False
    return True

def findNumOfMerges(matrix):
    numOfMerges = 0
    for rowNum in range(3):
        numOfMerges += np.sum(matrix[rowNum, :] == matrix[rowNum + 1, :])
    for colNum in range(3):
        numOfMerges += np.sum(matrix[:, colNum] == matrix[:, colNum + 1])
    return numOfMerges

def calculateSnakeBonus(matrix):
    snakeBonus = 0
    factors = np.linspace(10000, 1, num=16)
    n = 0
    for rowNum in range(3, -1, -1):
        if rowNum in [3, 1]:
            for colNum in range(3, -1, -1):
                snakeBonus += matrix[rowNum, colNum] * factors[n]
                n += 1
        else:
            for colNum in range(3):
                snakeBonus += matrix[rowNum, colNum] * factors[n]
                n += 1
    return snakeBonus