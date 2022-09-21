#solving 8 puzzle using depth first search

import numpy as np
import math
from queue import LifoQueue

CSVData = open("BFSstart.csv")
start = np.loadtxt(CSVData, delimiter=" ")

CSVData2 = open("BFSgoal.csv")
goal = np.loadtxt(CSVData2, delimiter=" ")

class State:
    def __init__(self, puzzle, previousState):
        self.puzzle = puzzle
        self.previousState = previousState
    

    def getIndexOfZero(self):
        index =[]
        for i in range(0,4):
            for j in range(0,4):
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
        if row == 3:
            actions[2] = 0
        if column == 0:
            actions[3] = 0
        if column == 3:
            actions[1] = 0
        return actions

    def getSuccessors(self):
        successors = []
        indexOfZero = self.getIndexOfZero()
        actionsList = self.availableActions()
        for i in actionsList:
            if i==1:
                newState = self.makeCopy()
                successors.append(newState)
        successorCount = 0
        for j in range(0,4):
            if actionsList[j] == 1:
                if j == 0:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]-1][indexOfZero[1]]
                    successors[successorCount].puzzle[indexOfZero[0]-1][indexOfZero[1]] = 0
                elif j == 1:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]][indexOfZero[1]+1]
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]+1] = 0
                elif j== 2:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]+1][indexOfZero[1]]
                    successors[successorCount].puzzle[indexOfZero[0]+1][indexOfZero[1]] = 0
                elif j == 3:
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]] = self.puzzle[indexOfZero[0]][indexOfZero[1]-1]
                    successors[successorCount].puzzle[indexOfZero[0]][indexOfZero[1]-1] = 0
                successors[successorCount].previousNode = self    
                successorCount += 1

        return successors

    def countHashValue(self):
        hashValue = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if i == 0:
                    hashValue += (1+j)*self.puzzle[i][j]
                elif i == 1:
                    hashValue += (5+j)*self.puzzle[i][j]
                elif i == 2:
                    hashValue += (9+j)*self.puzzle[i][j]
                elif i == 3:
                    hashValue += (13+j)*self.puzzle[i][j]
        return int(hashValue)

    def makeCopy(self):
        matrix = [[0 for i in range(0,4)]for j in range(0,4)]
        for i in range(0,4):
            for j in range(0,4):
                matrix[i][j] = self.puzzle[i][j]
        return State(matrix, self)

    def printState(self):
        for i in range(0, 4):    
            for k in range(0, 4):
                if(self.puzzle[i][k] == 0):
                    print("_", end=" ")
                else:
                    print(math.trunc(self.puzzle[i][k]), end = " ")
            print("\n")
    
    def compare(self, state):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.puzzle[i][j] != state.puzzle[i][j]:
                    return False
        return True

class Process:
    def __init__(self, startState, goalState):
        self.goal = goalState
        self.currentState = startState

        self.visitedhValue = []
        self.visitedNode = [list() for i in range(0,20000)]
        self.stack = LifoQueue()
        
        self.currentDepth = 0
        
        self.isGoalReached = False



    def putInVisited(self):
        print(self.currentState.countHashValue())
        if self.isVisited(self.currentState)== False:
            self.visitedhValue.append(self.currentState.countHashValue())
            self.visitedNode[self.currentState.countHashValue()].append(self.currentState)

    def isVisited(self, state):
        if state.countHashValue() in self.visitedhValue:
            for node in self.visitedNode[state.countHashValue()]:
                if(node.compare(state)):
                    return True
        return False


    def isGoal(self, state):
        return self.goal.compare(state)


    """This function will return an unvisited successor of the self.currentState or if it does not have any unvisited node then it will return -1"""
    def explore(self):
        successors = self.currentState.getSuccessors()
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

    def dfs(self):
        while(True):
            print("=============================================================================")
            print("depth = " + str(self.currentDepth))
            print("Chosen node from the above Successors : ")
            self.currentState.printState()
            self.putInVisited()#put current stae in visted
            self.stack.put(self.currentState)
            if(self.isGoal(self.currentState)):
                self.isGoalReached = True
                self.goal = self.currentState
                break
            nextNode = self.explore()
            if(nextNode == -1):
                poppedState = self.stack.get()
                del poppedState
                self.currentDepth -= 1
                if(self.stack.empty()):
                    print("stack empty")
                    break
                else:
                    self.currentState = self.stack.get()
            else:
                self.currentState = nextNode
                self.currentDepth += 1

    def printSuccessors(self, successors):
        for i in range(0, 4):    
            for j in range(0, len(successors)):
                for k in range(0, 4):
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
    
    
    newProcess = Process(startState, goalState)
    newProcess.dfs()
    if(newProcess.isGoalReached == True):
        print("Goal reached")
        goalState = newProcess.goal
    del newProcess
    print("\nComplete Path to goal is : ")
    printPathToGoal(goalState)
    
def printPathToGoal(goalState):
    state = goalState
    stack = LifoQueue()
    while(state.previousState != 0):
        stack.put(state)
        state = state.previousState
    stack.put(state)
    while(not stack.empty()):
        stack.get().printState()
        print()        


startState = State(start, 0)
goalState = State(goal, 0)
main(startState, goalState)