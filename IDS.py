from array import array
from itertools import count
from operator import index, indexOf, le
from os import stat
from random import randint
from this import d
from tkinter.tix import Tree
from traceback import print_tb
import numpy as np
import math
from queue import LifoQueue

CSVData = open("start.csv")
start = np.loadtxt(CSVData, delimiter=" ")

CSVData2 = open("goal.csv")
goal = np.loadtxt(CSVData2, delimiter=" ")

def indexOfElement(twoDArray, element):
    index =[]
    for i in range(0,3):
        for j in range(0,3):
            if twoDArray[i][j] == element:
                print(i)
                print(j)
                index.append(i)
                index.append(j)
                return index
def printState(state):
    for i in range(0, 3):    
        for k in range(0, 3):
            if(state[i][k] == 0):
                print("_", end=" ")
            else:
                print(math.trunc(state[i][k]), end = " ")
        print("\n")


class process:
    def __init__(self, start, goal, depthLimit) -> None:
        self.goal = goal
        self.currentState = start
        self.depthLimit = depthLimit

        self.visited = []
        self.stack = LifoQueue()
        
        self.indexOfZero = []
        self.currentDepth = 0
        self.actionsList = []
        
        self.isGoalReached = False
        self.isMaxDepthReached = False

    def availableActions(self):
        actions = [1,1,1,1]
        self.indexOfZero = indexOfElement(self.currentState, 0)
        row = self.indexOfZero[0]
        column = self.indexOfZero[1]
        if row == 0:
            actions[0] = 0
        if row == 2:
            actions[2] = 0
        if column == 0:
            actions[3] = 0
        if column == 2:
            actions[1] = 0

        return actions

    def getSuccessors(self):
        successors = []
        if self.currentDepth < self.depthLimit:
            for i in self.actionsList:
                if i==1:
                    newMatrix = self.makeCopy(self.currentState)
                    successors.append(newMatrix)
            successorCount = 0
            for j in range(0,4):
                if self.actionsList[j] == 1:
                    if j == 0:
                        successors[successorCount][self.indexOfZero[0]][self.indexOfZero[1]] = self.currentState[self.indexOfZero[0]-1][self.indexOfZero[1]]
                        successors[successorCount][self.indexOfZero[0]-1][self.indexOfZero[1]] = 0
                    elif j == 1:
                        successors[successorCount][self.indexOfZero[0]][self.indexOfZero[1]] = self.currentState[self.indexOfZero[0]][self.indexOfZero[1]+1]
                        successors[successorCount][self.indexOfZero[0]][self.indexOfZero[1]+1] = 0
                    elif j== 2:
                        successors[successorCount][self.indexOfZero[0]][self.indexOfZero[1]] = self.currentState[self.indexOfZero[0]+1][self.indexOfZero[1]]
                        successors[successorCount][self.indexOfZero[0]+1][self.indexOfZero[1]] = 0
                    elif j == 3:
                        successors[successorCount][self.indexOfZero[0]][self.indexOfZero[1]] = self.currentState[self.indexOfZero[0]][self.indexOfZero[1]-1]
                        successors[successorCount][self.indexOfZero[0]][self.indexOfZero[1]-1] = 0
                    successorCount += 1
        
        return successors

    def putInVisited(self, state):
        if self.isVisited(state)== False:
            self.visited.append(self.countHashValue(state))

    def isVisited(self, state):
        if self.countHashValue(state) in self.visited:
            return True
        else:
            return False

    def countHashValue(self, state):
        hashValue = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if i == 0:
                    hashValue += (10+j)*state[i][j]
                elif i == 1:
                    hashValue += (13+j)*state[i][j]
                elif i == 2:
                    hashValue += (16+j)*state[i][j]
        return hashValue

    def makeCopy(self, state):
        matrix = [[0 for i in range(0,3)]for j in range(0,3)]
        for i in range(0,3):
            for j in range(0,3):
                matrix[i][j] = self.currentState[i][j]
        return matrix

    def isGoal(self, state):
        for i in range(0, 3):
            for j in range(0, 3):
                if state[i][j] != self.goal[i][j]:
                    return False
        return True


    """This function will return an unvisited successor of the self.currentState or if it does not have any unvisited node then it will return -1"""
    def explore(self):
        self.actionsList = self.availableActions()
        successors = self.getSuccessors()
        if(len(successors) != 0):
            for successor in successors:
                if(not self.isVisited(successor)):
                    return successor
        # else:
        #     self.isMaxDepthReached = True

        return []

    def ids(self):
        while(True):
            print("depth = " + str(self.currentDepth))
            printState(self.currentState)
            self.putInVisited(self.currentState)
            self.stack.put(self.currentState)
            if(self.isGoal(self.currentState)):
                self.isGoalReached = True
                break
            nextNode = self.explore()
            if(len(nextNode) == 0):
                self.stack.get()
                self.currentDepth -= 1
                if(self.stack.empty()):
                    break
                else:
                    self.currentState = self.stack.get()
            else:
                self.currentState = nextNode
                self.currentDepth += 1



                
            


def main(start, goal):
    print("Start state : ")
    printState(start)
    print("\n")
    print("Goal state : ")
    printState(goal)
    print("\n")
    space = " "
    
    depthLimit = 0
    newProcess = process(start, goal, depthLimit)
    while(True):
        newProcess.ids()
        if(newProcess.isGoalReached == True):
            break
        depthLimit += 1
        newProcess = process(start, goal, depthLimit)
        


main(start, goal)