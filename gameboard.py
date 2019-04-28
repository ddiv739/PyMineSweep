from pprint import pprint
from random import randint
import PySimpleGUI as sg

class GameBoard:
    width = None
    height = None
    __gameboard = None
    __visibilityboard = None
    mines = None
    remaining_tiles = None
    #3 types of pieces. Mines which are game over. Empties which flood fill and have no discernable display. And numerical 
    #tiles which provides information to player
    TYPE_MINE = -1
    TYPE_EMPTY = 0

    #Visibility
    VIS_UNKNOWN = 1
    VIS_FLAGGED = 2
    VIS_EXPOSED = 0

    #State
    GAME_STARTING = 0
    GAME_RUNNING = 1
    GAME_OVER = 2
    GAME_WIN = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gamestate = 0

        self.mines = (width*height)/6.25
        self.remaining_tiles = self.width * self.height - self.mines

        self.__gameboard = [[0 for x in range(width)] for y in range(height)] 
        self.__visibilityboard = [[ 1 for x in range(width)] for y in range(height)] 
        
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

        # self.printDebugBoard()
        self.gamestate = self.GAME_RUNNING

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

    def printDebugBoard(self):
        for row in self.__gameboard:
            x = "["
            for col in row:
                if col == self.TYPE_MINE:
                    x += "*"
                elif col == self.TYPE_EMPTY:
                    #Change to whitespace later
                    x += "0"
                else :
                    x += str(col)
                x+= " , "
            x = x.rstrip(", ")
            x += "]"
            print(x)

    def printGameBoard(self):
        for row in range(0,self.height):
            x = "["
            for col in range(0,self.width):
                if(self.__visibilityboard[row][col] == self.VIS_UNKNOWN):
                    x += '?'
                elif(self.__visibilityboard[row][col] == self.VIS_FLAGGED):
                    x += 'F'
                else:
                    x += str(self.__gameboard[row][col])
                x+=' , '
            x = x.rstrip(", ")
            x += "]"
            print(x)

    def getGameBoard(self):
        y= []
        for row in range(0,self.height):
            x = []
            for col in range(0,self.width):
                if(self.__visibilityboard[row][col] == self.VIS_UNKNOWN):
                    x.append(sg.Button('?',button_color=('white', 'black'), key=str(row)+','+str(col)))
                elif(self.__visibilityboard[row][col] == self.VIS_FLAGGED):
                    x.append(sg.Button('F',button_color=('white', 'black'), key=str(row)+','+str(col)))
                else:
                    x.append(sg.Button(str(self.__gameboard[row][col]),button_color=('white', 'black'),disabled=True))
            y.append(x)
        
        return y


    def userInput(self, row, col):
        self.checkWinCondition()
        try:
            if(self.__gameboard[row][col] == self.TYPE_MINE):
                self.gameOver()
            elif(self.__visibilityboard[row][col] == self.VIS_EXPOSED):
                pass
            elif(self.__visibilityboard[row][col] == self.VIS_FLAGGED):
                print("You may not expose a flagged space. Use the f command on this space again to unflag it")
            else:
                self.exposeTile(row,col)

        except IndexError as e:
            pass

    def exposeTile(self,row,col):
        if( not (0<=row<self.width) or not (0<=col<self.height)):
            return
        if( self.__visibilityboard[row][col] == self.VIS_EXPOSED):
            return

        self.__visibilityboard[row][col] = self.VIS_EXPOSED
        self.remaining_tiles -= 1

        if(self.__gameboard[row][col] == self.TYPE_EMPTY):
            self.exposeTile(row+1,col)
            self.exposeTile(row-1,col)
            self.exposeTile(row,col+1)
            self.exposeTile(row,col-1)
            self.exposeTile(row+1,col+1)
            self.exposeTile(row+1,col-1)
            self.exposeTile(row-1,col+1)
            self.exposeTile(row-1,col-1)
        return

       

    def setFlag(self,row,col):
        try:
            self.__visibilityboard[row][col] = self.VIS_FLAGGED
        except IndexError as e:
            pass

    def checkWinCondition(self):
        if(self.remaining_tiles <=0):
            self.gamestate = self.GAME_WIN

    def gameOver(self) :
        #Set visibility of all
        self.__visibilityboard = [[ 0 for x in range(self.width)] for y in range(self.height)] 

        #Set game state as finished
        self.gamestate = self.GAME_OVER