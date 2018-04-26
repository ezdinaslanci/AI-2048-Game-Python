from expectiMaxThread import *


class AI:

    def __init__(self, ply):
        self.ply = ply
        self.workerThreads = [expectiMaxThread(), expectiMaxThread(), expectiMaxThread(), expectiMaxThread()]
        self.valueList = []

    def getMaxAction(self, node, ply, h):

        # get children
        actions = []
        children = []
        rotations = ['Up', 'Left', 'Down', 'Right']
        temp = np.copy(node)
        for r in rotations:
            node = np.copy(temp)
            node = moveTiles(node, r)
            node = mergeTiles(node, r)
            if not np.equal(temp, node).all():
                children.append(node)
                actions.append(r)

        for childNum in range(len(children)):
            self.workerThreads[childNum].setParameters(children[childNum], ply-1, h, "exp")
            self.workerThreads[childNum].start()

        for childNum in range(len(children)):
            self.workerThreads[childNum].join()
        maxAction = ''
        maxValue = -np.inf
        for childNum in range(len(children)):
            currentValue = self.workerThreads[childNum].getMaxValue()
            if currentValue >= maxValue:
                maxValue = currentValue
                maxAction = actions[childNum]
        return maxAction