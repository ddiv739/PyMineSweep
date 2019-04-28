from pprint import pprint
from random import randint
class GameBoard:
    width = None
    height = None
    __gameboard = None
    __visibilityboard = None
    mines = None

    #3 types of pieces. Mines which are game over. Empties which flood fill and have no discernable display. And numerical 
    #tiles which provides information to player
    TYPE_MINE = -1
    TYPE_EMPTY = 0
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mines = (width*height)/6.25
        self.__gameboard = [[0 for x in range(width)] for y in range(height)] 
        self.__visibilityboard = [[ False for x in range(width)] for y in range(height)] 

        mine_count = int(self.mines)

        print("Creating a 16 x 16 board with " + str(mine_count)+ " mines")
        while(mine_count > 0):
            #find random position. if not populate then populate and decrement else skip
            row , col = randint(0, height-1) , randint(0, width-1)

            if(self.__gameboard[row][col] == -1):
                continue
            self.__gameboard[row][col] = -1
            mine_count-=1
            #form adjacencies
            self.incrementAdjacentTiles(row,col)

        

        self.printBoardStatus()

    def incrementAdjacentTiles(self, row, col):
         
        if(col + 1 < self.width):
            self.ifNotMineIncrement(row,col+1)
            if(row + 1 < self.height):
                self.ifNotMineIncrement(row+1,col+1)
            if(row - 1 >= 0):
                self.ifNotMineIncrement(row-1,col+1)

        if(col - 1 >= 0):
            self.ifNotMineIncrement(row,col-1)
            if(row + 1 < self.height):
                self.ifNotMineIncrement(row+1,col-1)
            if(row - 1 >= 0):
                self.ifNotMineIncrement(row-1,col-1)

        if(row + 1 < self.height):
            self.ifNotMineIncrement(row+1,col)
        if(row - 1 >= 0):
            self.ifNotMineIncrement(row-1,col)

    def ifNotMineIncrement(self, row, col):
        if(self.__gameboard[row][col] != -1):
            self.__gameboard[row][col] += 1

    def printBoardStatus(self):
        for row in self.__gameboard:
            x = "["
            for col in row:
                if col == self.TYPE_MINE:
                    x += "*"
                elif col == self.TYPE_EMPTY:
                    x += "0"
                else :
                    x += str(col)
                x+= " , "
            x = x.rstrip(", ")
            x += "]"
            print(x)
