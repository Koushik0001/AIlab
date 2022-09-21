#solving 15 puzzle using A* search

import numpy as np
import math
from queue import LifoQueue
from queue import PriorityQueue

CSVData = open("BFSstart.csv")
start = np.loadtxt(CSVData, delimiter=" ")

CSVData2 = open("BFSgoal.csv")
goal = np.loadtxt(CSVData2, delimiter=" ")

class State:
    def __init__(self, puzzle, pathCostFromStart, previousState):
        self.puzzle = puzzle
        self.pathCostFromStart = 0  #pathCostFromStart#path cost to reach this state from the start
        self.previousState = previousState
    
    def __lt__(self, other):
        return False
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
                    hashValue += (13+j)*self.puzzle[i][j]
                elif i == 2:
                    hashValue += (16+j)*self.puzzle[i][j]
        return int(hashValue)

    def makeCopy(self):
        matrix = [[0 for i in range(0,4)]for j in range(0,4)]
        for i in range(0,4):
            for j in range(0,4):
                matrix[i][j] = self.puzzle[i][j]
        return State(matrix,self.pathCostFromStart, self)

    def printState(self):
        for i in range(0, 4):    
            for k in range(0, 4):
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
    def __init__(self, startState, goalState) -> None:
        self.goal = goalState
        self.currentState = startState

        self.visitedNode = [None]*20000
        self.priorityQueue = PriorityQueue()
        
        #self.currentPathCost = 0
        
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

    def h(self, state):
        hValue = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if self.goal.puzzle[i][j] != state.puzzle[i][j]:
                    hValue+=1
        return hValue

    """This function will return unvisited successors of the self.currentState"""
    def explore(self):
        successors = self.currentState.getSuccessors()
        if(len(successors) != 0):
            for successor in successors:
                if(self.isVisited(successor)):
                    list(successors).remove(successor)
        return successors

    def aStar(self):
        self.priorityQueue.put((self.currentState.pathCostFromStart+self.h(self.currentState), self.currentState))
        while(True):
            print("=============================================================================")
            #print("Current frontier : ")
            #self.printFrontier(self.priorityQueue)
            print()
            self.currentState = self.priorityQueue.get()[1]
            self.putInVisited(self.currentState)
            print("Chosen node from Current Frontier : ")
            self.currentState.printState()
        
            if(self.isGoal(self.currentState)):
                self.isGoalReached = True
                self.goal = self.currentState
                break

            successors = self.explore()
            if(len(successors) == 0):
                if(self.priorityQueue.empty()):
                    break
            else:
                print("Successors of the chosen node : ")
                self.printSuccessors(successors)
                for successor in successors:
                    self.priorityQueue.put((successor.pathCostFromStart+self.h(successor), successor))

    def printSuccessors(self, successors):
        for i in range(0, 4):    
            for j in range(0, len(successors)):
                for k in range(0, 4):
                    if(successors[j].puzzle[i][k] == 0):
                        print("_", end=" ")
                    else:
                        print(math.trunc(successors[j].puzzle[i][k]), end = " ",)
                print("", end = "\t\t\t")
            print("\n")

    # def printFrontier(self, frontier):
    #     if frontier.qsize() <= 4:
    #         printInALine = frontier.qsize()
    #     else:
    #         printInALine = 4
        
    #     matricesPrinted = 0
    #     while matricesPrinted < frontier.qsize():
    #         for i in range(0, 3):    
    #             for j in range(matricesPrinted, printInALine):
    #                 for k in range(0, 3):
    #                     if(frontier.queue[j][1].puzzle[i][k] == 0):
    #                         print("_", end=" ")
    #                     else:
    #                         print(math.trunc(frontier.queue[j][1].puzzle[i][k]), end = " ")
    #                 print("", end = "\t\t\t")
    #             print("\n")
    #         print("\n")
    #         matricesPrinted += 4
    #         if matricesPrinted+printInALine < frontier.qsize():
    #             printInALine += matricesPrinted
    #         else:
    #             printInALine = frontier.qsize()
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
        
    newProcess.aStar()
    if(newProcess.isGoalReached == True):
        print("Goal reached")
        goalState = newProcess.goal
    else:
        print("Goal not reached")
    
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

startState = State(start, 0, 0)
goalState = State(goal, -1, 0)# path cost from start = -1, means it is undefined
main(startState, goalState)