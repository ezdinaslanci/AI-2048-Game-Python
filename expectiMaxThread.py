import threading
from GridTools import *


class expectiMaxThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.node = None
        self.ply = None
        self.h = None
        self.expOrMax = None
        self.maxValue = None
        self.workerThreads = []

    def setParameters(self, node, ply, h, expOrMax):
        self.node = node
        self.ply = ply
        self.h = h
        self.expOrMax = expOrMax

    def run(self):
        self.maxValue = self.expectiMax(self.node, self.ply - 1, self.h, self.expOrMax)
        #print(self.maxValue)

    def getMaxValue(self):
        return self.maxValue

    def expectiMax(self, node, ply, h, expOrMax):

        if not checkIfCanGo(node):
            return -np.inf

        if ply == 0:
            return self.heuristic(node, h)

        elif expOrMax == 'max':

            # get children
            children = []
            rotations = ['Up', 'Left', 'Down', 'Right']
            temp = np.copy(node)
            for r in rotations:
                node = np.copy(temp)
                node = moveTiles(node, r)
                node = mergeTiles(node, r)
                if not np.equal(temp, node).all():
                    children.append(node)

            # calculate max
            childNum = 0
            for child in children:
                if not checkIfCanGo(node):
                    continue
                self.workerThreads.append(expectiMaxThread())
                self.workerThreads[childNum].setParameters(child, ply-1, h, "exp")
                self.workerThreads[childNum].start()
                childNum += 1

            childNum = 0
            for child in children:
                if not checkIfCanGo(node):
                    continue
                self.workerThreads[childNum].join()
                childNum += 1

            childNum = 0
            maxVal = -np.inf
            for child in children:
                if not checkIfCanGo(node):
                    continue
                maxVal = max(maxVal, self.workerThreads[childNum].getMaxValue())
                childNum += 1

            return maxVal

        elif expOrMax == 'exp':

            # get children
            blankCoors = np.argwhere(node == 0)
            randChildren = []
            for i in [2, 4]:
                temp = []
                for b in blankCoors:
                    child = np.copy(node)
                    child[b[0], b[1]] = i
                    temp.append(child)
                randChildren.append(temp)

            # calculate average
            childNum = 0
            for i in range(2):
                for rChild in randChildren[i]:

                    if not checkIfCanGo(node):
                        continue

                    self.workerThreads.append(expectiMaxThread())
                    self.workerThreads[childNum].setParameters(rChild, ply, h, "max")
                    self.workerThreads[childNum].start()

                    childNum += 1

            childNum = 0
            for i in range(2):
                for rChild in randChildren[i]:
                    if not checkIfCanGo(node):
                        continue
                    self.workerThreads[childNum].join()
                    childNum += 1

            avgList = []
            childNum = 0
            for i in range(2):
                avgList2 = []
                for rChild in randChildren[i]:
                    if not checkIfCanGo(node):
                        avgList2.append(0)
                        continue
                    avgList2.append(self.workerThreads[childNum].getMaxValue())
                    childNum += 1
                avgList.append(avgList2)

            return np.mean(avgList[0]) * 0.9 + np.mean(avgList[1]) * 0.1

    def heuristic(self, node, h):

        if h == 1: #number of blanks
            blankCoors = np.argwhere(np.asarray(node) == 0)
            return len(blankCoors)
        elif h == 2: #max tail
            blankCoors = np.argwhere(np.asarray(node) == 0)
            #return (np.max(node)/sum(sum(node)))*len(blankCoors)
            return node[3][3]*node[3][3]*node[2][3]*len(blankCoors)*len(blankCoors)
        elif h == 3: # sum Tail
            sum(sum(np.asarray(node)))
        elif h == 4: #sum of max 4
            blankCoors = np.argwhere(np.asarray(node) == 0)
            temp = np.reshape(node, 16)
            temp = sorted(temp)
            return len(blankCoors)*(temp[15]*5+temp[14]*2+temp[13])
        elif h == 5:
            maxCoors = np.argwhere(np.asarray(node) == max(node))[0]
            return 1/(1+abs(3-maxCoors[0]) + abs(3-maxCoors[1]))

        elif h == 6:
            utility = np.int64(0)
            orderScore = 0
            orderScore2 = 0
            sumOfPairwiseDistances = 0

            edgeBonus = 0

            for row in range(4):
                orderScore2 += gradeMonotonicityOfVector(node[row, :])**2 * sum(node[row, :]) * (16 if row in [0, 3] else 1)
                sumOfPairwiseDistances += getSumOfPairwiseDistances(node[row, :])
                edgeBonus += sum(node[row, :]) if row in [0, 3] else 0

            for col in range(4):
                orderScore2 += gradeMonotonicityOfVector(node[:, col])**2 * sum(node[:, col]) * (16 if col in [0, 3] else 1)
                sumOfPairwiseDistances += getSumOfPairwiseDistances(node[:, col])
                edgeBonus += sum(node[:, col]) if col in [0, 3] else 0

            numOfFreeTiles = 16 - np.count_nonzero(node)
            tilesSorted = sorted(np.reshape(node, 16), reverse=True)
            # freqs = np.bincount(np.reshape(node, 16))
            # freqs = freqs[np.nonzero(freqs)[0]]
            numOfAvailableMerges = findNumOfMerges(node)

            # penalize if highest N tiles are not in the same row or in the same column
            N = 4
            factor = 1
            highestNTilesPenalty = 0
            rows, cols = zip(*n_max(node, N))
            if tilesSorted[0]+tilesSorted[1]+tilesSorted[2]+tilesSorted[3]>=960 and not ((rows[1:] == rows[:-1] and rows[0] in [0,3] and checkMonotonicity(node[rows[0], :])) or (cols[1:] == cols[:-1] and cols[0] in [0,3] and checkMonotonicity(node[:, cols[0]]))):
                # print("This is BAD. ", end="")
                for tileNum in range(N - 1, -1, -1):
                    highestNTilesPenalty += factor * tilesSorted[tileNum]**2
                    factor *= 2

            maxTileCoor = n_max(node, 1)
            maxOfCorners = tilesSorted[0] if maxTileCoor in [(0,0),(0,3),(3,0),(3,3)] else 1
            sumOfGrid = sum(sum(node))
            maxTile = tilesSorted[0]

            # snakeBase = np.full((4, 4), 2, dtype=np.int)
            # snakes =    [   np.power(snakeBase, np.asarray([[4, 3, 2, 1], [5, 6, 7, 8], [12, 11, 10, 9], [13, 14, 15, 16]])),
            #                 np.power(snakeBase, np.asarray([[1, 2, 3, 4], [8, 7, 6, 5], [9, 10, 11, 12], [16, 15, 14, 13]])),
            #                 np.power(snakeBase, np.asarray([[16, 15, 14, 13], [9, 10, 11, 12], [8, 7, 6, 5], [1, 2, 3, 4]])),
            #                 np.power(snakeBase, np.asarray([[13, 14, 15, 16], [12, 11, 10, 9], [5, 6, 7, 8], [4, 3, 2, 1]])),
            #                 np.power(snakeBase, np.asarray([[4, 5, 12, 13], [3, 6, 11, 14], [2, 7, 10, 15], [1, 8, 9, 16]])),
            #                 np.power(snakeBase, np.asarray([[1, 8, 9, 16], [2, 7, 10, 15], [3, 6, 11, 14], [4, 5, 12, 13]])),
            #                 np.power(snakeBase, np.asarray([[16, 9, 8, 1], [15, 10, 7, 2], [14, 11, 6, 3], [13, 12, 5, 4]])),
            #                 np.power(snakeBase, np.asarray([[13, 12, 5, 4], [14, 1, 6, 3], [15, 10, 7, 2], [16, 9, 8, 1]]))
            #             ]
            #
            # bestSnake = snakes[0]
            # curSnakeVal = np.uint64(0)
            # bestSnakeVal = np.uint64(0)
            # for snake in snakes:
            #     curSnakeVal = sum(sum(np.multiply(snake, node)))
            #     bestSnakeVal = sum(sum(np.multiply(bestSnake, node)))
            #     if  curSnakeVal > bestSnakeVal:
            #         bestSnake = snake

            utility = + (0 * numOfAvailableMerges) \
                      + (10 * orderScore2) \
                      + (0 * edgeBonus) \
                      + (0 * maxOfCorners) \
                      - (0 * sumOfPairwiseDistances) \
                      - (0 * highestNTilesPenalty)

            # utility =   + sum(sum(np.multiply(bestSnake, node))) \
            #             + (1 * orderScore2) \
            #             + (1 * numOfAvailableMerges) \
            #             - (2 * highestNTilesPenalty)

            return utility

        elif h == 7:
            orderScore = 0
            orderScore1 = 0
            sumOfPairwiseDistances = 0
            for row in range(4):
                if checkInc(node[row, :]) and row == 3:
                    orderScore += np.mean(node[row, :]) * (5 if row in [0, 3] else 1)
                sumOfPairwiseDistances += getSumOfPairwiseDistances(node[row, :])

            for col in range(4):
                if checkInc(node[:, col]) and col == 3:
                    orderScore1 += np.mean(node[:, col]) * (5 if col in [0, 3] else 1)
                sumOfPairwiseDistances += getSumOfPairwiseDistances(node[:, col])

            orderScore = np.max([orderScore, orderScore1])

            numOfFreeTiles = 16 - np.count_nonzero(node)
            snake = []
            snake.append([node[3, 3], node[3, 2], node[3, 1], node[3, 0]])
            snake.append([node[2, 0], node[2, 1], node[2, 2], node[2, 3]])
            snake.append([node[1, 3], node[1, 2], node[1, 1], node[1, 0]])
            snake.append([node[0, 0], node[0, 1], node[0, 2], node[0, 3]])

            snake2 = []
            snake2.append([node[3, 3], node[2, 3], node[1, 3], node[0, 3]])
            snake2.append([node[0, 2], node[1, 2], node[2, 2], node[3, 2]])
            snake2.append([node[3, 1], node[2, 1], node[1, 1], node[0, 1]])
            snake2.append([node[0, 0], node[1, 0], node[2, 0], node[3, 0]])


            maxV = 1
            maxV2 = 1
            a = 2.2**16
            for s, s1 in zip(snake, snake2):
                a /= 3.14*9
                for i, j in zip(s, s1):
                    maxV += i*a
                    maxV2 += j*a
                    a /= 1.3

            temp = np.reshape(node, 16)
            temp = sorted(temp)
            penalty = 0
            if not node[3,3] == temp[15]:
                penalty = temp[15] + temp[14] + temp[13] + temp[12] - node[3, 3]
            elif not node[3,2] == temp[14]:
                penalty = temp[14] + temp[13] + temp[12] - node[3, 2]
            elif not node[3,1] == temp[13]:
                penalty = temp[13] + temp[12] - node[3, 1]
            elif not node[3,0] == temp[12]:
                penalty = temp[12] - node[3, 0]

            penalty2 = 0
            if not node[3, 3] == temp[15]:
                penalty2 = temp[15] + temp[14] + temp[13] + temp[12] - node[3, 3]
            elif not node[2, 3] == temp[14]:
                penalty2 = temp[14] + temp[13] + temp[12] - node[2, 3]
            elif not node[1, 3] == temp[13]:
                penalty2 = temp[13] + temp[12] - node[1, 3]
            elif not node[0, 3] == temp[12]:
                penalty2 = temp[12] - node[0, 3]

            penalty = np.min([penalty, penalty2])
            maxV = np.max([maxV, maxV2])
            utility = (orderScore *10 + maxV*2000 - sumOfPairwiseDistances*10 - penalty*200) * [0, 1][numOfFreeTiles > 0] + np.max(node)
            return maxV