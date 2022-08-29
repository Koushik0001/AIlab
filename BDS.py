#solving 8 puzzle using bidirectional search

import numpy as np
import math
from queue import Queue
from queue import LifoQueue

CSVData = open("IDSstart.csv")
start = np.loadtxt(CSVData, delimiter=" ")

CSVData2 = open("IDSgoal.csv")
goal = np.loadtxt(CSVData2, delimiter=" ")

class State:
    def __init__(self, puzzle, level, previousState) -> None:
        self.puzzle = puzzle
        self.level = level
        self.previousState = previousState
    

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
        return State(matrix, self.level, self)

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

class ProcessBDS:
    def __init__(self, startState, goalState) -> None:
        #varables for forBard searh
        self.goalForward = goalState
        self.currentStateForward = startState

        self.visitedForward = []
        self.fifoQueueForward = Queue()
        self.currentLevelForward = 0
        
        #variables for backward search
        self.goalBackward = startState.makeCopy()
        self.currentStateBackward = goalState.makeCopy()

        self.visitedBackward = []
        self.fifoQueueBackward = Queue()
        self.currentLevelBackward = 0
        #common variable
        self.isGoalReached = False


    def putInVisited(self, state, ForB):
        if ForB == "f":
            if self.isVisited(state, ForB)== False:
                self.visitedForward.append(state.countHashValue())
        else:
            if self.isVisited(state, ForB)== False:
                self.visitedBackward.append(state.countHashValue())


    def isVisited(self, state,ForB):
        if ForB == "f":
            if state.countHashValue() in self.visitedForward:
                return True
        else:
            if state.countHashValue() in self.visitedBackward:
                return True

        return False


    def isGoal(self):
        result = []
        for nodef in self.fifoQueueForward.queue:
            for nodeb in self.fifoQueueBackward.queue:
                if nodef.compare(nodeb):
                    result.append(nodef)
                    result.append(nodeb)
                    return result
        return []


    def explore(self, ForB):
        if ForB == "f":
            successors = self.currentStateForward.getSuccessors()
        else:
            successors = self.currentStateBackward.getSuccessors()
        # if len(successors) > 0:
        #     print("Successors of above node in level " + str(self.currentState.level + 1))
        #     self.printSuccessors(successors)
        # else:
        #     print("Successors : there is no successor")
        # print("=============================================================================")
        if(len(successors) != 0):
            for successor in list(successors):
                if(self.isVisited(successor,ForB)):
                    successors.remove(successor)
            return successors
        return -1

    def bds(self):
        self.fifoQueueForward.put(self.currentStateForward)
        self.fifoQueueBackward.put(self.currentStateBackward)

        self.putInVisited(self.currentStateForward, "f")#put current stae in visted
        self.putInVisited(self.currentStateBackward, "b")
        while(True):
            print("==========================================================================================")
            print("Frontier of forward search :  ")
            self.printFrontier(self.fifoQueueForward)
            print("\n")
            print("Frontier of backward search :  ")
            self.printFrontier(self.fifoQueueBackward)
            print("\n")
            print("==========================================================================================")
            intersection = self.isGoal()
            if len(intersection) != 0:
                return intersection

            self.currentStateForward = self.fifoQueueForward.get()
            successors = self.explore("f")
            if successors == -1:
                if not self.fifoQueueForward.empty:
                    self.fifoQueueForward.get()
                else:
                    break
            else:
                for successor in list(successors):
                    self.fifoQueueForward.put(successor)
                    self.putInVisited(successor, "f")
            
            print("==========================================================================================")
            print("Frontier of forward search :  ")
            self.printFrontier(self.fifoQueueForward)
            print("\n")
            print("Frontier of backward search :  ")
            self.printFrontier(self.fifoQueueBackward)
            print("\n")
            print("==========================================================================================")
            
            intersection = self.isGoal()
            if len(intersection) != 0:
                return intersection
            
            self.currentStateBackward = self.fifoQueueBackward.get()
            successorsBack = self.explore("b")
            if successorsBack == -1:
                if not self.fifoQueueBackward.empty:
                    self.fifoQueueBackward.get()
                else:
                    break
            else:
                for successor in list(successorsBack):
                    self.fifoQueueBackward.put(successor)
                    self.putInVisited(successor, "b")

    def printFrontier(self, frontier):
        if len(frontier.queue) <= 4:
            printInALine = len(frontier.queue)
        else:
            printInALine = 4
        
        matricesPrinted = 0
        while matricesPrinted < len(frontier.queue):
            for i in range(0, 3):    
                for j in range(matricesPrinted, printInALine):
                    for k in range(0, 3):
                        if(frontier.queue[j].puzzle[i][k] == 0):
                            print("_", end=" ")
                        else:
                            print(math.trunc(frontier.queue[j].puzzle[i][k]), end = " ")
                    print("", end = "\t\t\t")
                print("\n")
            print("\n")
            matricesPrinted += 4
            if matricesPrinted+printInALine < len(frontier.queue):
                printInALine += matricesPrinted
            else:
                printInALine = len(frontier.queue)




def main(startState, goalState):
    print("Start state : ")
    startState.printState()
    print("\n")
    print("Goal state : ")
    goalState.printState()
    print("\n")
    space = " "
    
    newProcess = ProcessBDS(startState, goalState)
    intersection = newProcess.bds()
    
    if(newProcess.isGoalReached == True):
        print("Goal reached")
    print()
    print("###################################################################")
    print("\nComplete path to goal is :\n")
    printPathToGoal(intersection[0], startState)
    state = intersection[1]
    state = state.previousState
    while(state.previousState != 0):
        state.printState()
        print("\n")
        state = state.previousState


def printPathToGoal(goalState, startState):
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
goalState = State(goal, 0, 0)
main(startState, goalState)