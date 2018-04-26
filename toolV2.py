import numpy as np

# this function merges tiles which have the same value
def mergeTiles(grid, direction):

    # direction validity check
    if direction not in ["up", "down", "left", "right"]:
        print("ERR: Unknown direction for merge.")
        return -1

    # merge in up direction
    elif direction == "up":

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
    elif direction == "down":

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
    elif direction == "left":

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
    elif direction == "right":

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

    return grid

mat = np.zeros((4, 4), dtype = np.int)
mat[0, 0] = 2
mat[1, 0] = 0
mat[2, 0] = 2
mat[3, 0] = 0

mat[0, 1] = 2
mat[1, 1] = 4
mat[2, 1] = 2
mat[3, 1] = 2

mat[0, 2] = 2
mat[1, 2] = 4
mat[2, 2] = 2
mat[3, 2] = 2

mat[0, 3] = 2
mat[1, 3] = 4
mat[2, 3] = 2
mat[3, 3] = 2

print(mat)
print(mergeTiles(mat, "right"))