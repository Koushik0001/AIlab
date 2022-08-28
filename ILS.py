#solving 8 puzzle using iterative deepening search

from array import array
#from asyncio.windows_events import INFINITE
from itertools import count
#from operator import index, indexOf, le
#from os import stat
from random import randint
from this import d
from tkinter.tix import Tree
from traceback import print_tb
from turtle import right
import numpy as np
import math
from queue import LifoQueue

CSVData = open("IDSstart.csv")
start = np.loadtxt(CSVData, delimiter=" ")

CSVData2 = open("IDSgoal.csv")
goal = np.loadtxt(CSVData2, delimiter=" ")

class State:
    def __init__(self, puzzle, pathCostFromStart) -> None:
        self.puzzle = puzzle
        self.pathCostFromStart = pathCostFromStart#path cost to reach this state from the start
    

    def getIndexOfZero(self):
        index =[]
        for i in range(0,3):
            for j in range(0,3):
                if self.puzzle[i][j] == 0:
                    index.append(i)
                    index.append(j)
                    return index

    def availableActions(self):
        actions = [1,1,1,1]
        indexOfZero = self.getIndexOfZero()
        row = indexOfZero[0]
        column = indexOfZero[1]
        if row == 0:
            actions[0] = 0
        if row == 2:
            actions[2] = 0
        if column == 0:
            actions[3] = 0
        if column == 2:
            actions[1] = 0
        return actions

    #action == 0 => move up
    #action == 1 => move right
    #action == 2 => move down
    #action == 3 => move left
    def actionCost(self, action):
        return 1

    def getSuccessors(self):
        successors = []
        indexOfZero = self.getIndexOfZero()
        actionsList = self.availableActions()
        successorCount = 0
        for i in actionsList:
            if i==1:
                newState = self.makeCopy()
                successors.append(newState)
        for j in range(0,4):
            if actionsList[j] == 1:
                if j == 0:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]-1][indexOfZero[1]]
                    successors[successorCount].puzzle[indexOfZero[0]-1][indexOfZero[1]] = 0
                    successors[successorCount].pathCostFromStart = self.pathCostFromStart+self.actionCost(0)
                elif j == 1:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]][indexOfZero[1]+1]
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]+1] = 0
                    successors[successorCount].pathCostFromStart = self.pathCostFromStart+self.actionCost(1)
                elif j== 2:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]+1][indexOfZero[1]]
                    successors[successorCount].puzzle[indexOfZero[0]+1][indexOfZero[1]] = 0
                    successors[successorCount].pathCostFromStart = self.pathCostFromStart+self.actionCost(2)
                elif j == 3:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]][indexOfZero[1]-1]
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]-1] = 0
                    successors[successorCount].pathCostFromStart = self.pathCostFromStart+self.actionCost(3)
                successorCount += 1
                    
        return successors

    def countHashValue(self):
        hashValue = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if i == 0:
                    hashValue += (10+j)*self.puzzle[i][j]
                elif i == 1:
                    hashValue += (13+j)*self.puzzle[i][j]
                elif i == 2:
                    hashValue += (16+j)*self.puzzle[i][j]
        return hashValue

    def makeCopy(self):
        matrix = [[0 for i in range(0,3)]for j in range(0,3)]
        for i in range(0,3):
            for j in range(0,3):
                matrix[i][j] = self.puzzle[i][j]
        return State(matrix,self.pathCostFromStart)

    def printState(self):
        for i in range(0, 3):    
            for k in range(0, 3):
                if(self.puzzle[i][k] == 0):
                    print("_", end=" ")
                else:
                    print(math.trunc(self.puzzle[i][k]), end = " ")
            print("\n")
    
    def compare(self, state):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.puzzle[i][j] != state.puzzle[i][j]:
                    return False
        return True

class Process:
    def __init__(self, startState, goalState, pathCostLimit) -> None:
        self.goal = goalState
        self.currentState = startState
        self.pathCostLimit = pathCostLimit

        self.visited = []
        self.stack = LifoQueue()
        
        #self.currentPathCost = 0
        
        self.isGoalReached = False
        self.isMaxDepthReached = False
        self.lowestPathCostOfDiscardedNodes = 0


    def putInVisited(self):
        if self.isVisited(self.currentState)== False:
            self.visited.append(self.currentState.countHashValue())

    def isVisited(self, state):
        if state.countHashValue() in self.visited:
            return True
        else:
            return False


    def isGoal(self, state):
        return self.goal.compare(state)


    """This function will return an unvisited successor of the self.currentState or if it does not have any unvisited node then it will return -1"""
    def explore(self):
        successors = self.currentState.getSuccessors()
        for successor in list(successors):
            if successor.pathCostFromStart > self.pathCostLimit:
                successors.remove(successor)
                if self.lowestPathCostOfDiscardedNodes == 0:
                    self.lowestPathCostOfDiscardedNodes = successor.pathCostFromStart
                elif successor.pathCostFromStart < self.lowestPathCostOfDiscardedNodes:
                    self.lowestPathCostOfDiscardedNodes = successor.pathCostFromStart
                del successor
       
        if len(successors) > 0:
            print("Successors : ")
            self.printSuccessors(successors)
        else:
            print("Successors : there is no successor")
        print("=============================================================================")
        if(len(successors) != 0):
            for successor in successors:
                if(not self.isVisited(successor)):
                    return successor
        return -1

    def ids(self):
        while(True):
            print("=============================================================================")
            print("path Cost = " + str(self.currentState.pathCostFromStart))
            print("Chosen node from the above Successors : ")
            self.currentState.printState()
            self.putInVisited()#put current stae in visted
            self.stack.put(self.currentState)
            if(self.isGoal(self.currentState)):
                self.isGoalReached = True
                break
            nextNode = self.explore()
            if(nextNode == -1):
                poppedState = self.stack.get()
                del poppedState
                if(self.stack.empty()):
                    break
                else:
                    self.currentState = self.stack.get()
            else:
                self.currentState = nextNode

    def printSuccessors(self, successors):
        for i in range(0, 3):    
            for j in range(0, len(successors)):
                for k in range(0, 3):
                    if(successors[j].puzzle[i][k] == 0):
                        print("_", end=" ")
                    else:
                        print(math.trunc(successors[j].puzzle[i][k]), end = " ")
                print("", end = "\t\t\t")
            print("\n")

                
            


def main(startState, goalState):
    print("Start state : ")
    startState.printState()
    print("\n")
    print("Goal state : ")
    goalState.printState()
    print("\n")
    space = " "
    
    pathCostLimit = 0
    newProcess = Process(startState, goalState, pathCostLimit)
    while(True):
        print("\n\n *** New Iteration ***")
        print("pathCostLimit = " + str(pathCostLimit))
        print()
        newProcess.ids()
        if(newProcess.isGoalReached == True):
            print("Goal reached")
            break
        pathCostLimit = newProcess.lowestPathCostOfDiscardedNodes
        del newProcess
        newProcess = Process(startState, goalState, pathCostLimit)
        


startState = State(start, 0)
goalState = State(goal, -1)# path cost from start = -1, means it is undefined
main(startState, goalState)