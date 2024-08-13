# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import random
import queue
import os

class MyAI( AI ):
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        
        self.boardRow = colDimension
        self.boardColumn = rowDimension
        self.boardBombs = totalMines
        self.xcoordinate = startX
        self.ycoordinate = startY

        self.sadTotalBoardSpots = (rowDimension * colDimension) - totalMines
        self.mySadBoard = [[-2 for j in range( self.boardColumn)] for i in range( self.boardRow)]
        self.mySadProbabilityBoard = [[-2 for j in range(self.boardColumn)] for i in range(self.boardRow)]
        self.mySadQueue = queue.Queue()
        self.visited = []
        self.totalExploredSpots = 0

        self.minValue = 1000
        self.minX = 1000
        self.minY = 1000
        self.myBoardNeighbors = [(-1,0),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(1,-1),(1,1)]

        self.gameMode = 1

        if (rowDimension == 5 and colDimension == 5):
            self.gameMode = 0
        else:
            self.gameMode = 1

    def getAction(self, number: int) -> "Action Object":
        # for 5 x 5 game mode
        if(self.gameMode == 0):
            if(self.mySadBoard[self.xcoordinate][self.ycoordinate] == -2):
                self.mySadBoard[self.xcoordinate][self.ycoordinate] = number
                self.totalExploredSpots = self.totalExploredSpots + 1

            if (self.sadTotalBoardSpots == self.totalExploredSpots):
                return Action(AI.Action.LEAVE)

            if (number == 0):
                return self.isZero()

            if (number == 1):
                return self.isOne()

        # for any other game mode
        else:
            #print("helloooo\n")
            #print(self.xcoordinate, "\n")
            #print(self.ycoordinate, "\n")
            if(self.totalExploredSpots == self.sadTotalBoardSpots):
                # print("puto\n")
                return Action(AI.Action.LEAVE, 1, 1)
            
            #print("I am here\n")
            x,y = self.xcoordinate, self.ycoordinate

            # set the board number, 1,2,3, etc.
            # print(len(self.mySadBoard))
            self.mySadBoard[x][y] = number 

            # this is absolute safe
            self.mySadProbabilityBoard[x][y] = 0 
            
            #print("I am there\n")
            self.xcoordinate, self.ycoordinate, actiontype = self.caseNumberIsZero(number)
            #stops working here
            #print("I am poo\n")
            if(actiontype != AI.Action.FLAG):
                self.totalExploredSpots += 1
            #print("I am here now\n")
            self.visited.append((self.xcoordinate,self.ycoordinate))
            return Action(actiontype, self.xcoordinate, self.ycoordinate)
        
    def caseNumberIsZero(self,number):
        #print("I am in my function\n")
        for x, y in self.myBoardNeighbors: 
            # print("I am in my function two\n")
            newX = self.xcoordinate + x 
            newY = self.ycoordinate + y
            if(self.inValidSpot(newX, newY) and not ((newX,newY) in self.visited) and not ((newX,newY) in list(self.mySadQueue.queue))):
                #propogate to my neighbors of my current number
                #print(newX,newY)
                if(number == 0):
                    self.mySadProbabilityBoard[newX][newY] = 0
                    self.mySadQueue.put((newX,newY)) #this is safe
                    continue
            
                if(self.mySadProbabilityBoard[newX][newY] == 0):
                    continue
                
                if(self.mySadProbabilityBoard[newX][newY] < 0):
                    self.mySadProbabilityBoard[newX][newY] = 1
                else:
                    self.mySadProbabilityBoard[newX][newY] += 1
        #print("I am in my function some \n")

        for xcoordinate in range(len(self.mySadProbabilityBoard)):
            for ycoordinate in range(len(self.mySadProbabilityBoard[xcoordinate])):
                if(self.mySadProbabilityBoard[xcoordinate][ycoordinate] == 0 and not ((xcoordinate,ycoordinate) in self.visited) and not ((xcoordinate,ycoordinate) in list(self.mySadQueue.queue))): 
                    self.mySadQueue.put((xcoordinate,ycoordinate))
                    continue
        
                if(self.mySadBoard[xcoordinate][ycoordinate] == -2):
                    continue
                
                vacant = []
                nonVacant = []
                flagged = []
                for x,y in self.myBoardNeighbors:
                    newX = xcoordinate + x 
                    newY = ycoordinate + y
                    if(self.inValidSpot(newX,newY) ):
                        #inside the boundary
                        if(self.mySadBoard[newX][newY] == -2):
                            vacant.append((newX,newY))
                        elif(self.mySadBoard[newX][newY] == -1):
                            flagged.append((newX,newY))
                        else:
                            nonVacant.append((newX,newY))

                if(len(vacant) > 0 and len(vacant) == self.mySadBoard[xcoordinate][ycoordinate]- len(flagged)):
                    # the vacant squares must be bomb
                    vacantx, vacanty = vacant.pop(0)

                    # print("I am in my first return\n")

                    #decrement surrounding squares
                    for x,y in self.myBoardNeighbors:
                        newX = xcoordinate + x
                        newY = ycoordinate + y
                        if(self.inValidSpot(newX,newY) and self.mySadProbabilityBoard[newX][newY] > 0):
                            self.mySadProbabilityBoard[newX][newY] -= 1
                    # print("I am in my first return\n")
                    
                    
                    
                    temp = list(self.mySadQueue.queue)
                    i = 0
                    while(i < len(temp)):
                        if(temp[i] == (vacantx, vacanty)):
                            temp.pop(i)
                            continue
                        i+=1
                    newQueue = queue.Queue()
                    [newQueue.put(i) for i in temp]    
                    self.mySadQueue = newQueue
                    
                    return vacantx, vacanty, AI.Action.FLAG
                
                if(self.mySadBoard[xcoordinate][ycoordinate] == len(flagged)):
                    #all vacant are then safe
                    for x,y in self.myBoardNeighbors:
                        newX = xcoordinate + x
                        newY = ycoordinate + y
                        if(self.inValidSpot(newX,newY) and self.mySadBoard[xcoordinate][ycoordinate] >= 0 and self.mySadProbabilityBoard[newX][newY] > 0):
                            self.mySadProbabilityBoard[newX][newY] = 0
                            if(not ((newX,newY) in self.visited) and not ((newX, newY) in list(self.mySadQueue.queue))):
                                self.mySadQueue.put((newX,newY))          
                                self.mySadProbabilityBoard[newX][newY] = max(0, self.mySadProbabilityBoard[newX][newY]-1)              

        if(self.mySadQueue.qsize() > 0):
           coordinate = self.mySadQueue.get()
           return coordinate[0], coordinate[1], AI.Action.UNCOVER
            
        else:
           
            rando = []
            for xcoordinate in range(len(self.mySadBoard)):
                for ycoordinate in range(len(self.mySadBoard[xcoordinate])):
                    if(self.mySadBoard[xcoordinate][ycoordinate] == -2):
                        # # rando = random.randint(0,2)
                        # # if(rando > 0):     
                        # rando.append((self.mySadProbabilityBoard[xcoordinate][ycoordinate], xcoordinate, ycoordinate))
                        return xcoordinate,ycoordinate, AI.Action.UNCOVER 
                        # rando.append((xcoordinate,ycoordinate))
            if(len(rando) == 0):
                return 1,1, AI.Action.LEAVE
            
            #separate to 0s and non-0s
            zeros = [i for i in rando if i[0] == 0]
            nonzero = [i for i in rando if i [0] > 0]
            
            if(len(nonzero) > 0):
                nonzero = sorted(nonzero, key=lambda x: x[0])
                return nonzero[0][1], nonzero[0][2], AI.Action.UNCOVER
            
            return zeros[0][1], zeros[0][2]
            
            # r = random.randint(0, len(rando)-1)
            # return rando[r][0], rando[r][1], AI.Action.UNCOVER
    
            
            
    def inValidSpot(self, x, y):
        if x < 0 or x >= self.boardRow:
            return False
        if y < 0 or y >= self.boardColumn:
            return False
        return True

    # the below functions are for 5 x 5 game mode
    def isOne(self) -> "Action Object":
        if (self.totalExploredSpots == 1):
            if (self.xcoordinate + 1 < self.boardColumn):
                self.xcoordinate = self.xcoordinate + 1
                return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
            elif (self.xcoordinate - 1 >= 0):
                self.xcoordinate = self.xcoordinate - 1
                return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
            elif (self.ycoordinate + 1 < self.boardRow):
                self.ycoordinate = self.ycoordinate + 1
                return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
            elif (self.xcoordinate - 1 >= 0):
                self.ycoordinate = self.ycoordinate - 1
                return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)

        for x in range(self.boardRow):
                for y in range(self.boardColumn):
                    # right
                    if (self.mySadBoard[x][y] == 0 and x + 1 < self.boardColumn and self.mySadBoard[x + 1][y] == -2):
                        self.xcoordinate = x + 1
                        self.ycoordinate = y
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                    # top
                    elif (self.mySadBoard[x][y] == 0 and y + 1 < self.boardColumn and self.mySadBoard[x][y + 1] == -2):
                        self.xcoordinate = x
                        self.ycoordinate = y + 1
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                    # left
                    elif (self.mySadBoard[x][y] == 0 and x - 1 >= 0 and self.mySadBoard[x - 1][y] == -2):
                        self.xcoordinate = x - 1
                        self.ycoordinate = y
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                    # bottom
                    elif (self.mySadBoard[x][y] == 0 and y - 1 >= 0 and self.mySadBoard[x][y - 1] == -2):
                        self.xcoordinate = x
                        self.ycoordinate = y - 1
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
    
        for x in range(self.boardRow):
                for y in range(self.boardColumn):
                    if (self.mySadBoard[x][y] == 1):
                        # up and to the right corner
                        if (y + 1 < self.boardRow and y + 2 < self.boardRow and x + 1 < self.boardColumn and self.mySadBoard[x][y + 1] == 1 and self.mySadBoard[x][y + 2] == 1 and self.mySadBoard[x + 1][y + 2] == - 2):
                            self.xcoordinate = x + 1
                            self.ycoordinate = y + 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # across and to the lower right corner
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and y - 1 >= 0 and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == 1 and self.mySadBoard[x + 2][y - 1] == -2):
                            self.xcoordinate = x + 2
                            self.ycoordinate = y - 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # up and to the left corner
                        elif (y + 1 < self.boardRow and y + 2 < self.boardRow and x - 1 >= 0 and self.mySadBoard[x][y + 1] == 1 and self.mySadBoard[x][y + 2] == 1 and self.mySadBoard[x - 1][y + 2] == - 2):
                            self.xcoordinate = x - 1
                            self.ycoordinate = y + 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # across and to the lower left corner
                        elif (x - 1 >= 0 and x - 2 >= 0 and y - 1 >= 0 and self.mySadBoard[x - 1][y] == 1 and self.mySadBoard[x - 2][y] == 1 and self.mySadBoard[x - 2][y - 1] == -2):
                            self.xcoordinate = x - 2
                            self.ycoordinate = y - 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # down and to the left corner
                        elif (y - 1 >= 0 and y - 2 >= 0 and x - 1 >= 0 and self.mySadBoard[x][y - 1] == 1 and self.mySadBoard[x][y - 2] == 1 and self.mySadBoard[x - 1][y - 2] == - 2):
                            self.xcoordinate = x - 1
                            self.ycoordinate = y - 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # down and to the right corner
                        elif (y - 1 >= 0 and y - 2 >= 0 and x + 1 < self.boardColumn and self.mySadBoard[x][y - 1] == 1 and self.mySadBoard[x][y - 2] == 1 and self.mySadBoard[x + 1][y - 2] == - 2):
                            self.xcoordinate = x + 1
                            self.ycoordinate = y - 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # across and to the upper right corner
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and y + 1 < self.boardColumn and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == 1 and self.mySadBoard[x + 2][y + 1] == -2):
                            self.xcoordinate = x + 2
                            self.ycoordinate = y + 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, vertical down
                        elif (y + 1 < self.boardRow and y + 2 < self.boardRow and self.mySadBoard[x][y + 1] == 1 and self.mySadBoard[x][y + 2] == -2):
                            self.xcoordinate = x
                            self.ycoordinate = y + 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # square ones in corner going across going down in a square
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and y + 1 < self.boardRow and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == 1 and self.mySadBoard[x][y + 1] == -2):
                            # print("I am in here")
                            self.xcoordinate = x
                            self.ycoordinate = y + 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, vertical going down in a square
                        elif (y - 1 < self.boardRow and y - 2 < self.boardRow and self.mySadBoard[x][y - 1] == 1 and self.mySadBoard[x][y - 2] == -2):
                            self.xcoordinate = x
                            self.ycoordinate = y - 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, horizontal going right in a square
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == -2):
                            self.xcoordinate = x + 2
                            self.ycoordinate = y
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, horizontal going left in a square
                        elif (x - 1 >= 0 and x - 2 >= 0 and self.mySadBoard[x - 1][y] == 1 and self.mySadBoard[x - 2][y] == -2):
                            self.xcoordinate = x - 2
                            self.ycoordinate = y
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
        
        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)	

    def isZero(self) -> "Action Object":
        # bottom middle 
        if (self.ycoordinate - 1 >= 0 and self.mySadBoard[self.xcoordinate][self.ycoordinate - 1] == -2):
            self.ycoordinate = self.ycoordinate - 1
        # top middle 
        elif (self.ycoordinate + 1 < self.boardColumn and self.mySadBoard[self.xcoordinate][self.ycoordinate + 1] == -2):
            self.ycoordinate = self.ycoordinate + 1
        # directly left
        elif (self.xcoordinate - 1 >= 0 and self.mySadBoard[self.xcoordinate - 1][self.ycoordinate] == -2):
            self.xcoordinate = self.xcoordinate - 1
        # directly right
        elif (self.xcoordinate + 1 < self.boardRow and self.mySadBoard[self.xcoordinate + 1][self.ycoordinate] == -2):
            self.xcoordinate = self.xcoordinate + 1
        # bottom left corner
        elif (self.xcoordinate - 1 >= 0 and self.ycoordinate - 1 >= 0 and self.mySadBoard[self.xcoordinate - 1][self.ycoordinate - 1] == -2):
            self.xcoordinate = self.xcoordinate - 1
            self.ycoordinate = self.ycoordinate - 1
        # bottom right corner
        elif (self.xcoordinate + 1 < self.boardColumn and self.ycoordinate - 1 >= 0 and self.mySadBoard[self.xcoordinate + 1][self.ycoordinate - 1] == -2):
            self.xcoordinate = self.xcoordinate + 1
            self.ycoordinate = self.ycoordinate - 1
        # top left corner
        elif (self.xcoordinate - 1 >= 0 and self.ycoordinate + 1 < self.boardRow and self.mySadBoard[self.xcoordinate - 1][self.ycoordinate + 1] == -2):
            self.xcoordinate = self.xcoordinate - 1
            self.ycoordinate = self.ycoordinate + 1
        # top right corner
        elif (self.xcoordinate + 1 < self.boardColumn and self.ycoordinate + 1 < self.boardRow and self.mySadBoard[self.xcoordinate + 1][self.ycoordinate + 1] == -2):
            self.xcoordinate = self.xcoordinate + 1
            self.ycoordinate = self.ycoordinate + 1
        else:
            for x in range(self.boardRow):
                for y in range(self.boardColumn):
                    if (self.mySadBoard[x][y] == 0 and x + 1 < self.boardColumn and self.mySadBoard[x+1][y] == -2):
                        self.xcoordinate = x + 1
                        self.ycoordinate = y
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                    elif (self.mySadBoard[x][y] == 0 and y + 1 < self.boardRow and self.mySadBoard[x][y + 1] == -2):
                        self.xcoordinate = x
                        self.ycoordinate = y + 1
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                    elif (self.mySadBoard[x][y] == 0 and x - 1 >= 0 and self.mySadBoard[x - 1][y] == -2):
                        self.xcoordinate = x - 1
                        self.ycoordinate = y 
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                    elif (self.mySadBoard[x][y] == 0 and y - 1 >= 0 and self.mySadBoard[x][y - 1] == -2):
                        self.xcoordinate = x
                        self.ycoordinate = y - 1
                        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                
            for x in range(self.boardRow):
                for y in range(self.boardColumn):
                    if (self.mySadBoard[x][y] == 1):
                        # up and to the right corner
                        if (y + 1 < self.boardRow and y + 2 < self.boardRow and x + 1 < self.boardColumn and self.mySadBoard[x][y + 1] == 1 and self.mySadBoard[x][y + 2] == 1 and self.mySadBoard[x + 1][y + 2] == - 2):
                            self.xcoordinate = x + 1
                            self.ycoordinate = y + 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # across and to the lower right corner
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and y - 1 >= 0 and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == 1 and self.mySadBoard[x + 2][y - 1] == -2):
                            self.xcoordinate = x + 2
                            self.ycoordinate = y - 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # up and to the left corner
                        elif (y + 1 < self.boardRow and y + 2 < self.boardRow and x - 1 >= 0 and self.mySadBoard[x][y + 1] == 1 and self.mySadBoard[x][y + 2] == 1 and self.mySadBoard[x - 1][y + 2] == - 2):
                            self.xcoordinate = x - 1
                            self.ycoordinate = y + 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # across and to the lower left corner
                        elif (x - 1 >= 0 and x - 2 >= 0 and y - 1 >= 0 and self.mySadBoard[x - 1][y] == 1 and self.mySadBoard[x - 2][y] == 1 and self.mySadBoard[x - 2][y - 1] == -2):
                            self.xcoordinate = x - 2
                            self.ycoordinate = y - 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # down and to the left corner
                        elif (y - 1 >= 0 and y - 2 >= 0 and x - 1 >= 0 and self.mySadBoard[x][y - 1] == 1 and self.mySadBoard[x][y - 2] == 1 and self.mySadBoard[x - 1][y - 2] == - 2):
                            self.xcoordinate = x - 1
                            self.ycoordinate = y - 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # down and to the right corner
                        elif (y - 1 >= 0 and y - 2 >= 0 and x + 1 < self.boardColumn and self.mySadBoard[x][y - 1] == 1 and self.mySadBoard[x][y - 2] == 1 and self.mySadBoard[x + 1][y - 2] == - 2):
                            self.xcoordinate = x + 1
                            self.ycoordinate = y - 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # across and to the upper right corner
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and y + 1 < self.boardColumn and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == 1 and self.mySadBoard[x + 2][y + 1] == -2):
                            self.xcoordinate = x + 2
                            self.ycoordinate = y + 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, vertical down
                        elif (y + 1 < self.boardRow and y + 2 < self.boardRow and self.mySadBoard[x][y + 1] == 1 and self.mySadBoard[x][y + 2] == -2):
                            self.xcoordinate = x
                            self.ycoordinate = y + 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # square ones in corner going across going down in a square
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and y + 1 < self.boardRow and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == 1 and self.mySadBoard[x][y + 1] == -2):
                            # print("I am in here")
                            self.xcoordinate = x
                            self.ycoordinate = y + 1
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, vertical going down in a square
                        elif (y - 1 < self.boardRow and y - 2 < self.boardRow and self.mySadBoard[x][y - 1] == 1 and self.mySadBoard[x][y - 2] == -2):
                            self.xcoordinate = x
                            self.ycoordinate = y - 2
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, horizontal going right in a square
                        elif (x + 1 < self.boardColumn and x + 2 < self.boardColumn and self.mySadBoard[x + 1][y] == 1 and self.mySadBoard[x + 2][y] == -2):
                            self.xcoordinate = x + 2
                            self.ycoordinate = y
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
                        # two one's in a row, horizontal going left in a square
                        elif (x - 1 >= 0 and x - 2 >= 0 and self.mySadBoard[x - 1][y] == 1 and self.mySadBoard[x - 2][y] == -2):
                            self.xcoordinate = x - 2
                            self.ycoordinate = y
                            return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)
        
        return Action(AI.Action.UNCOVER, self.xcoordinate, self.ycoordinate)