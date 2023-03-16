import os

def openBFF(filePointer: str="dark_1.bff"):
    
    #open the file
    file=open(filePointer,'r').read()

    print(file)

#os.getcwd()
file_path = os.getcwd() + '\dark_1.bff'
print(file_path)
openBFF(file_path)

