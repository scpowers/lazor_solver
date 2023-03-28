import os


def openBFF(filePointer: str = "dark_1.bff"):

    # open the file
    file = open(filePointer, 'r').read()

    #print(file)

    #print(len(file))
    
    # the length of GRID START is 11 characters, hence I add 11 charactes to the index it was first found
    gridStart = 11+file.find("GRID START")
    gridEnd = file.find("GRID STOP")

    #gridString = file[gridStart:gridEnd].strip()
    #grid=gridString.split('\n')

    #print(gridString)
    #print(grid)

    ##alternative approach

    lineSplitFile=file.strip().splitlines()
    
    #print(lineSplitFile)
    #the line preceding the one where grid start was identified 
    startGridLine=1+lineSplitFile.index("GRID START")
    
    #print(startGridLine)

    #the stop grid line is the line before the GRID STOP string
    stopGridLine=lineSplitFile.index("GRID STOP")-1
    #print(stopGridLine)
    #print(lineSplitFile[stopGridLine])

    #iterate the index from grid start line to grid end line plus 1 to include in range
    gridString=lineSplitFile[startGridLine:stopGridLine+1]
    
    #print(gridString)
    
    #define grid as an empty list of lists
    grid=[[]]
    
    #lambda function below splits a given line into a list of values
    lineList= lambda gridLine: gridLine.split() 
    
    #print(lineList(gridString[0]))

    #cast result of map function appied to gridString and assign as grid  
    grid=list(map(lineList, gridString))
    print(grid)

    #lasers=lineSplitFile.index("L")
    #laserLines=list(map(str.find("L"),file))

    #list of list storing the laser origin and tragectory
    laserList=[]
    #block list number list 
    blockList=[]
    #list of list storing the points the lasers must pass through
    pointGoalList=[]

    #iterate from the end of the grid to the end of the file to avoid capturing values within the grid string
    for line in lineSplitFile[stopGridLine:]:
        if line.startswith("L"):
            #take the current line, strip the leading L, then strip the leading whitespace, then split each integer value on the space, then append list to laserList
            laserList.append(line.strip('L').strip().split())
            print(laserList)

            
        elif line.startswith("P"):
            pointGoalList.append(line.strip('P').strip().split())
            print(pointGoalList)


    #print(laserLines)

# os.getcwd()
file_path = os.getcwd() + '\dark_1.bff'
#print(file_path)
openBFF(file_path)
