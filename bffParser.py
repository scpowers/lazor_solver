import os


def openBFF(filePointer: str = "dark_1.bff"):

    # open the file
    file = open(filePointer, 'r').read()

    print(file)

    print(len(file))
    # the length of GRID START is 11 characters, hence I add 11 charactes to the index it was first found
    gridStart = 11+file.find("GRID START")
    gridEnd = file.find("GRID STOP")

    gridString = file[gridStart:gridEnd].strip()
    grid=gridString.split('\n')

    print(gridString)
    print(grid)

    ##alternative approach

    lineSplitFile=file.strip().splitlines()
    print(lineSplitFile)
    startline=lineSplitFile.index("GRID START")
    print(startline)


# os.getcwd()
file_path = os.getcwd() + '\dark_1.bff'
print(file_path)
openBFF(file_path)