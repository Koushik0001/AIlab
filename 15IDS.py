#solving 8 puzzle using iterative deepening search

import numpy as np
import math
from queue import LifoQueue

CSVData = open("BFSstart.csv")
start = np.loadtxt(CSVData, delimiter=" ")

CSVData2 = open("BFSgoal.csv")
goal = np.loadtxt(CSVData2, delimiter=" ")

class State:
    def __init__(self, puzzle, previousState) -> None:
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

    def getSuccessors(self, currentDepth, depthLimit):
        successors = []
        if currentDepth < depthLimit:
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
                    hashValue += (10+j)*self.puzzle[i][j]
                elif i == 1:
                    hashValue += (14+j)*self.puzzle[i][j]
                elif i == 2:
                    hashValue += (18+j)*self.puzzle[i][j]
                elif i == 3:
                    hashValue += (22+j)*self.puzzle[i][j]
        return int(hashValue)

    def makeCopy(self):
        matrix = [[0 for i in range(0,4)]for j in range(0,4)]
        for i in range(0,4):
            for j in range(0,4):
                matrix[i][j] = self.puzzle[i][j]
        return State(matrix , self)

    def printState(self):
        for row in self.puzzle:
            for val in row:
                print ('{:4}'.format(int(val)), end=' ')
            print("\n")
    
    def compare(self, state):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.puzzle[i][j] != state.puzzle[i][j]:
                    return False
        return True

class Process:
    def __init__(self, startState, goalState, depthLimit) -> None:
        self.goal = goalState
        self.currentState = startState
        self.depthLimit = depthLimit

        self.visitedNode = [None]*20000
        self.stack = LifoQueue()
        
        self.currentDepth = 0
        
        self.isGoalReached = False
        self.isMaxDepthReached = False



    def putInVisited(self, state):
        hvalue = state.countHashValue()
        if self.isVisited(state)== False:
            if self.visitedNode[hvalue] == None: #Empty slot - turn into list of keys to avoid extra cases
                self.visitedNode[hvalue] = [state]
            else: #Collision - append
                self.visitedNode[hvalue].append(state)

    def isVisited(self, state):
        hvalue = state.countHashValue()
        if self.visitedNode[hvalue] == None:
            return False
        else:
            for node in self.visitedNode[hvalue]:
                if node.compare(state):
                    return True
            return False


    def isGoal(self, state):
        return self.goal.compare(state)


    """This function will return an unvisited successor of the self.currentState or if it does not have any unvisited node then it will return -1"""
    def explore(self):
        successors = self.currentState.getSuccessors(self.currentDepth,self.depthLimit)
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
            print("depth = " + str(self.currentDepth))
            print("Chosen node from the above Successors : ")
            self.currentState.printState()
            self.putInVisited(self.currentState)#put current stae in visted
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
                        print ('{:>4}'.format('_'), end=' ')
                    else:
                        print ('{:4}'.format(int(successors[j].puzzle[i][k])), end=' ')
                print("", end = "\t\t")
            print("\n")

                
            


def main(startState, goalState):
    print("Start state : ")
    startState.printState()
    print("\n")
    print("Goal state : ")
    goalState.printState()
    print("\n")
    space = " "
    
    
    depthLimit = 0
    newProcess = Process(startState, goalState, depthLimit)
    while(True):
        print("\n\n*** New Iteration ***")
        print("DepthLimit = " + str(depthLimit))
        print()
        newProcess.ids()
        if(newProcess.isGoalReached == True):
            print("Goal reached")
            goalState = newProcess.goal
            break
        depthLimit += 1
        del newProcess
        newProcess = Process(startState, goalState, depthLimit)
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
        print("\n\n")        


startState = State(start, 0)
goalState = State(goal, 0)
main(startState, goalState)