#solving 8 puzzle using breadth First search search

from os import stat
import numpy as np
import math
from queue import Queue
from queue import LifoQueue

CSVData = open("BFSstart.csv")
start = np.loadtxt(CSVData, delimiter=" ")

CSVData2 = open("BFSgoal.csv")
goal = np.loadtxt(CSVData2, delimiter=" ")

class State:
    def __init__(self, puzzle, level, previousState) -> None:
        self.puzzle = puzzle
        self.level = level
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
                successors[successorCount].level = self.level + 1
                successors[successorCount].previousNode = self
                successorCount += 1

        return successors

    def countHashValue(self):
        hashValue = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if i == 0:
                    hashValue += (16+j)*self.puzzle[i][j]
                elif i == 1:
                    hashValue += (20+j)*self.puzzle[i][j]
                elif i == 2:
                    hashValue += (24+j)*self.puzzle[i][j]
                elif i == 3:
                    hashValue += (28+j)*self.puzzle[i][j]
        return int(hashValue)

    def makeCopy(self):
        matrix = [[0 for i in range(0,4)]for j in range(0,4)]
        for i in range(0,4):
            for j in range(0,4):
                matrix[i][j] = self.puzzle[i][j]
        return State(matrix, self.level, self)

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
    def __init__(self, startState, goalState):
        self.goal = goalState
        self.currentState = startState

        self.visitedNode = [None]*20000
        self.fifoQueue = Queue()

        self.isGoalReached = False


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
        successors = self.currentState.getSuccessors()
        if len(successors) > 0:
            print("Successors of above node in level " + str(self.currentState.level + 1))
            self.printSuccessors(successors)
        else:
            print("Successors : there is no successor")
        print("=============================================================================")
        if(len(successors) != 0):
            for successor in list(successors):
                if(self.isVisited(successor)):
                    successors.remove(successor)
            return successors
        return -1

    def bfs(self):
        self.fifoQueue.put(self.currentState)
        self.putInVisited(self.currentState)#put current stae in visted
        while(True):
            self.currentState = self.fifoQueue.get()
            print("=============================================================================")
            print("level = " + str(self.currentState.level))
            print("Chosen node from level " + str(self.currentState.level))
            self.currentState.printState()
            if(self.isGoal(self.currentState)):
                self.isGoalReached = True
                self.goal = self.currentState
                break
            else:
                successors = self.explore()
                if successors == -1:
                    if self.fifoQueue.empty:
                        self.fifoQueue.get()
                    else:
                        break
                else:
                    for successor in list(successors):
                        self.fifoQueue.put(successor)
                        self.putInVisited(successor)
        

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
    
    newProcess = Process(startState, goalState)
    newProcess.bfs()
    if(newProcess.isGoalReached == True):
        print("Goal reached")
    print()
    print("###################################################################")
    print("\nComplete path to goal is :\n")
    printPathToGoal(newProcess.goal, startState)

def printPathToGoal(goalState, startState):
    state = goalState
    stack = LifoQueue()
    while(state.previousState != 0):
        stack.put(state)
        state = state.previousState
    stack.put(state)
    while(not stack.empty()):
        stack.get().printState()
        print("\n\n")


        


startState = State(start, 0, 0)
goalState = State(goal, -1, 0)
main(startState, goalState)