'''
@Author: Nick Bruns
@Created: 3/14/2023
Parses a BFF board file for the lazors mobile game
'''

import os

# define values for parser usage later
FREE = 0  # o block
REFLECTIVE = 1  # A block
REFRACTIVE = 2  # B block
OPAQUE = 3  # C block
HOLE = 4  # x block
FIXED_REFLECTIVE = 5
FIXED_REFRACTIVE = 6
FIXED_OPAQUE = 7
UNAVAILABLE_GRID_KEY='x'
FREE_GRID_KEY='o'
FIXED_REFLECTIVE_KEY = 'A'
FIXED_OPAQUE_KEY = 'B'
FIXED_REFRACTIVE_KEY = 'C'
HOLE_CHAR='4'
FREE_CHAR='0'


def openBFF(filePointer: str):

    # open the file
    file = open(filePointer, 'r').read()

    # the length of GRID START is 11 characters, hence I add 11 charactes to the index it was first found
    gridStart = 11+file.find("GRID START")
    gridEnd = file.find("GRID STOP")

    # gridString = file[gridStart:gridEnd].strip()
    # grid=gridString.split('\n')

    # print(gridString)
    # print(grid)

    # alternative approach

    lineSplitFile = file.strip().splitlines()

    # the line preceding the one where grid start was identified
    startGridLine = 1+lineSplitFile.index("GRID START")

    # the stop grid line is the line before the GRID STOP string
    stopGridLine = lineSplitFile.index("GRID STOP")-1

    # iterate the index from grid start line to grid end line plus 1 to include in range
    gridString = lineSplitFile[startGridLine:stopGridLine+1]

    # define grid as an empty list of lists
    grid = [[]]

    # lambda function below splits a given line into a list of values
    def lineList(gridLine): return gridLine.split()

    ###CONVERSION OF STRING GRID TO NUMERICAL GRID
    #lambda function below converts the x and o characters to numerical strings 
    convertGridSymbol = lambda newLine : newLine.replace(UNAVAILABLE_GRID_KEY, HOLE_CHAR).replace(FREE_GRID_KEY,FREE_CHAR).replace(FIXED_REFLECTIVE_KEY,str(FIXED_REFLECTIVE)).replace(FIXED_REFRACTIVE_KEY,str(FIXED_REFRACTIVE)).replace(FIXED_OPAQUE_KEY,str(FIXED_OPAQUE))

    # cast result of map function appied to gridString and assign as grid
    grid = list(map(lineList, list(map(convertGridSymbol,gridString))))
    grid = [list(map(int, l)) for l in grid]

    # list of list storing the laser origin and tragectory, for now is initialized as an empty string to inform python that it has a job to do
    laserList = []
    # block type list
    blockList = []
    # list of list storing the points the lasers must pass through
    pointGoalList = []

    ###BLOCK, POINT, AND LASER PARSING###
    # iterate from the end of the grid to the end of the file to avoid capturing values within the grid string
    for line in lineSplitFile[stopGridLine+1:]:
        # check for lazor trajectory
        if line.startswith("L"):
            # take the current line,
            # strip the leading L,
            # then strip the leading whitespace,
            # then split each integer value on the space,
            # then apply map function to cast to int
            # then cast map output to list
            # then append list to laserList
            laserList.append(list(map(int, line.strip('L').strip().split())))
        # check for point goals
        elif line.startswith("P"):
            # take the current line,
            # strip the leading P,
            # then strip the leading whitespace,
            # then split each integer value on the space,
            # then apply map function to cast the string to an integer,
            # then cast the map output to a list,
            # then append this list to pointGoalList
            thisLine = list(map(int, line.strip('P').strip().split()))
            # pointGoalList.append(line.strip('P').strip().split())
            pointGoalList.append(
                list(map(int, line.strip('P').strip().split())))
        # check for A blocks
        elif line.startswith("A"):
            # number of a blocks is assigned as the present line with the leading A striped, then with the leading spaces stripped, then cast to an integer value
            blockNumA = int(line.strip('A').strip())
            # iterate for extracted number of blocks
            for i in range(blockNumA):
                # append the global value for A blocks to the block list for as many times as the extracted blockNum indicates
                blockList.append(REFLECTIVE)
        # check for B blocks
        elif line.startswith("B"):
            # number of a blocks is assigned as the present line with the leading B striped,
            # then with the leading spaces stripped,
            # then cast to an integer value
            blockNumB = int(line.strip('B').strip())
            # iterate for extracted number of blocks
            for i in range(blockNumB):
                # append the global value for B blocks to the block list for as many times as the extracted blockNum indicates
                blockList.append(OPAQUE)
        # check for C blocks
        elif line.startswith("C"):
            # number of a blocks is assigned as the present line with the leading C striped,
            # then with the leading spaces stripped,
            # then cast to an integer value
            blockNumC = int(line.strip('C').strip())
            # iterate for extracted number of blocks
            for i in range(blockNumC):
                # append the global value for C blocks to the block list for as many times as the extracted blockNum indicates
                blockList.append(REFRACTIVE)

    """
    print(grid)
    print(laserList)
    print(pointGoalList)
    print(blockList)
    """
    return grid, laserList, pointGoalList, blockList

if __name__ == '__main__':
    # os.getcwd()
    file_path = os.getcwd() + '/dark_1.bff'
    # print(file_path)
    openBFF(file_path)
