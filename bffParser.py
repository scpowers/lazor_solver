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

    

# os.getcwd()
file_path = os.getcwd() + '\dark_1.bff'
#print(file_path)
openBFF(file_path)
