from turtle import end_fill
from handle import *

def readInputLevel1():
    pathParent = os.path.join(os.curdir,'input')
    pathParent = os.path.join(pathParent,'level_1')
    dir_list = os.listdir(pathParent)
    for i in range(len(dir_list)):
        numInput = dir_list[i][:dir_list[i].find('.txt')]
        pathChild = os.path.join(pathParent,dir_list[i])
        handleInputLevel1(pathChild, numInput)

def readInputLevel2():
    pathParent = os.path.join(os.curdir,'input')
    pathParent = os.path.join(pathParent,'level_2')
    dir_list = os.listdir(pathParent)
    for i in range(len(dir_list)):
        numInput = dir_list[i][:dir_list[i].find('.txt')]
        pathChild = os.path.join(pathParent,dir_list[i])
        handleInputLevel2(pathChild, numInput)

def readInputLevel3():
    pathParent = os.path.join(os.curdir,'input')
    pathParent = os.path.join(pathParent,'level_3')
    dir_list = os.listdir(pathParent)
    for i in range(len(dir_list)):
        numInput = dir_list[i][:dir_list[i].find('.txt')]
        pathChild = os.path.join(pathParent,dir_list[i])
        handleInputLevel3(pathChild, numInput)

def readInputAdvance():
    pathParent = os.path.join(os.curdir,'input')
    pathParent = os.path.join(pathParent,'advance')
    dir_list = os.listdir(pathParent)
    for i in range(len(dir_list)):
        numInput = dir_list[i][:dir_list[i].find('.txt')]
        pathChild = os.path.join(pathParent,dir_list[i])
        handleInputAdvance(pathChild, numInput)

def main():
    readInputLevel1()
    readInputLevel2()
    readInputLevel3()
    readInputAdvance()

main()