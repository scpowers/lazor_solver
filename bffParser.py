"""
@Author: Nick Bruns
@Created: 3/14/2023
Parses a BFF board file for the lazors mobile game
"""

# define values for parser usage later
FREE = 0  # o block
REFLECTIVE = 1  # A block
REFRACTIVE = 2  # C block
OPAQUE = 3  # B block
HOLE = 4  # x block
FIXED_REFLECTIVE = 5
FIXED_REFRACTIVE = 6
FIXED_OPAQUE = 7
UNAVAILABLE_GRID_KEY = 'x'
FREE_GRID_KEY = 'o'
FIXED_REFLECTIVE_KEY = 'A'
FIXED_OPAQUE_KEY = 'B'
FIXED_REFRACTIVE_KEY = 'C'
HOLE_CHAR = '4'
FREE_CHAR = '0'


def openBFF(filePointer: str):
    """
    This method opens and parses a .BFF file at a given directory, then returns a dictionary
    of the parsed grid of the file, the lazor origins and trajectory, the coordinates of the
    laser goal points, and a list of all movable blocks available to reach a solution

    **Parameters**

        filePointer: *str*
            String representing the location of the desired bff file to open and parse

    **Returns**

        grid: *list, list, int*
            List of integer lists presenting a 2D representation of the parsed board file including
            the locations of fixed blocks, holes in the board where no blocks may be placed, and
            open spaces in the board where blocks can be placed

            0 = free space to place a block
            4 = hole in the board where a laser can pass through unimpeded but no block can be placed
            5 = Fixed reflective block
            6 = Fixed refractive block
            7 = Fixed opaque block

        laserList: *list, list, int*
            List of integer lists specifying the origin coordinates and trajectory of each laser beam. Each
            interior list represents one laser 'emitter'. The length of the outside/containing list holding
            the inside lists may be arbitrarily long but length of every inside list is exactly 4 elements.
            The first element of the inside list is the x origin, the followed by the y origin, followed by
            +/-1 for the x direction, then +/-1 for the y direction. Coordinate 0,0 is the top left.

            [[x_origin,y_origin,+-1,+-1]...]

        pointGoalList: *list, list, int*
            List of integer lists containing the coordinates of goal points that must have a laser pass
            through them. Each individual 2 element list contained within the outer list represents the
            x and y coordinate of a single point. There may be multiple points and so the number of lists
            contained in the outer list can be arbitrarily large, however each of these inner lists is
            exactly 2 elements. Coordinate 0,0 is the top left.

            [[x_coordinate,y_coordinate]...]

        blockList: *list, int*
            An integer list storing the type and number of every block available in the given bff file that
            can be moved to solve the board. The number of occurances of each element in the list represents
            the number of those blocks that are present. The value at each element indicates the type of block.

            1 = REFLECTIVE
            2 = REFRACTIVE
            3 = OPAQUE
    """

    # open the file
    file = open(filePointer, 'r').read()

    # strip leading spaces and newlines, then split on new lines and assign each line as an element of a string list
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

    # CONVERSION OF STRING GRID TO NUMERICAL GRID
    # lambda function below converts the x and o characters to numerical strings
    def convertGridSymbol(newLine): return newLine.replace(UNAVAILABLE_GRID_KEY, HOLE_CHAR).replace(
        FREE_GRID_KEY, FREE_CHAR).replace(FIXED_REFLECTIVE_KEY, str(FIXED_REFLECTIVE)).replace(
        FIXED_REFRACTIVE_KEY, str(FIXED_REFRACTIVE)).replace(FIXED_OPAQUE_KEY, str(FIXED_OPAQUE))

    # cast result of map function applied to gridString and assign as grid
    grid = list(map(lineList, list(map(convertGridSymbol, gridString))))
    grid = [list(map(int, l)) for l in grid]

    # list of list storing the laser origin and trajectory, for now is initialized as an empty string to inform
    # python that it has a job to do
    laserList = []
    # block type list
    blockList = []
    # list of list storing the points the lasers must pass through
    pointGoalList = []

    # -- BLOCK, POINT, AND LASER PARSING -- #
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
            # pointGoalList.append(line.strip('P').strip().split())
            pointGoalList.append(
                list(map(int, line.strip('P').strip().split())))
        # check for A blocks
        elif line.startswith("A"):
            # number of a blocks is assigned as the present line with the leading A striped, then with the leading
            # spaces stripped, then cast to an integer value
            blockNumA = int(line.strip('A').strip())
            # iterate for extracted number of blocks
            for i in range(blockNumA):
                # append the global value for A blocks to the block list for as many times as the extracted
                # blockNum indicates
                blockList.append(REFLECTIVE)
        # check for B blocks
        elif line.startswith("B"):
            # number of a blocks is assigned as the present line with the leading B striped,
            # then with the leading spaces stripped,
            # then cast to an integer value
            blockNumB = int(line.strip('B').strip())
            # iterate for extracted number of blocks
            for i in range(blockNumB):
                # append the global value for B blocks to the block list for as many times as the extracted
                # blockNum indicates
                blockList.append(OPAQUE)
        # check for C blocks
        elif line.startswith("C"):
            # number of a blocks is assigned as the present line with the leading C striped,
            # then with the leading spaces stripped,
            # then cast to an integer value
            blockNumC = int(line.strip('C').strip())
            # iterate for extracted number of blocks
            for i in range(blockNumC):
                # append the global value for C blocks to the block list for as many times as the extracted
                # blockNum indicates
                blockList.append(REFRACTIVE)

    return grid, laserList, pointGoalList, blockList
