from pprint import pprint
from random import randint
import PySimpleGUI as sg

class GameBoard:
    isVisual = False
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

    #Reinforcement agent scores TODO move to unified file for agent and board
    REWARD_WIN = 750
    REWARD_FLAG_MINE = 50
    REWARD_CLEARED_TILE = 5

    PENALTY_MOVE = -1
    PENALTY_LOSS = -250
    PENALTY_FALSE_FLAG = -20

    def __init__(self, width, height, isVisual=False):
        self.width = width
        self.height = height
        self.gamestate = 0
        self.isVisual = isVisual
        self.FlagMode = False
        if(self.isVisual):
            self.flagbutton = sg.Checkbox('Flag Mode', default=False, background_color="#404040",text_color="white")
        #Floor // in order to cast down to prevent float errors in checking win conditions
        self.mines = (width*height)//6.25
        self.remaining_tiles = int(self.width * self.height - self.mines)

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
        if(not self.isVisual):
            return "This is not a visual game instance "
        y= [[sg.Text('Minesweeper')],
        [sg.Button('Reset',size=(4,1), button_color=('white', 'black'), key="Reset")],
        [self.flagbutton]]
        for row in range(0,self.height):
            x = []
            for col in range(0,self.width):
                if(self.__visibilityboard[row][col] == self.VIS_UNKNOWN):
                    x.append(sg.Button('?',button_color=('white', 'black'), key=str(row)+','+str(col)))
                elif(self.__visibilityboard[row][col] == self.VIS_FLAGGED):
                    x.append(sg.Button('F',button_color=('white', 'red'), key=str(row)+','+str(col)))
                else:
                    x.append(sg.Button(str(self.__gameboard[row][col]),button_color=('white', 'black'),disabled=True))
            y.append(x)
        
        return y


    def userInput(self, row, col,flagMode=False):
        #Score relates to reinforcement agent and its training
        if(self.isVisual):
            self.FlagMode = self.flagbutton.Get()
        else :
            self.FlagMode = flagMode
        try:
            if(self.FlagMode ):
                return self.setFlag(row,col)


            if(self.__visibilityboard[row][col] == self.VIS_EXPOSED):
                return self.PENALTY_MOVE
            elif(self.__visibilityboard[row][col] == self.VIS_FLAGGED):
                print("You may not expose a flagged space. Use the f command on this space again to unflag it")
                return self.PENALTY_MOVE
            elif(self.__gameboard[row][col] == self.TYPE_MINE):
                self.gameOver()
                return self.PENALTY_LOSS
            else:
                exposing_score = self.exposeTile(row,col)
                if(self.checkWinCondition()):
                    return self.REWARD_WIN + exposing_score
                
                return exposing_score

        except IndexError as e:
            return self.PENALTY_MOVE

    def exposeTile(self,row,col, score=0):
        if( not (0<=row<self.width) or not (0<=col<self.height)):
            return 0
        if( self.__visibilityboard[row][col] == self.VIS_EXPOSED):
            return 0

        self.__visibilityboard[row][col] = self.VIS_EXPOSED
        score += self.REWARD_CLEARED_TILE
        self.remaining_tiles -= 1
        if(self.__gameboard[row][col] == self.TYPE_EMPTY):
            score += self.exposeTile(row+1,col)
            score += self.exposeTile(row-1,col)
            score += self.exposeTile(row,col+1)
            score += self.exposeTile(row,col-1)
            score += self.exposeTile(row+1,col+1)
            score += self.exposeTile(row+1,col-1)
            score +=  self.exposeTile(row-1,col+1)
            score += self.exposeTile(row-1,col-1)

        return score

       

    def setFlag(self,row,col):
        try:
            if(self.__visibilityboard[row][col] == self.VIS_EXPOSED):
                return self.PENALTY_MOVE
            if(self.__visibilityboard[row][col] == self.VIS_FLAGGED):
                self.__visibilityboard[row][col] = self.VIS_UNKNOWN
                return self.PENALTY_MOVE
            else:
                self.__visibilityboard[row][col] = self.VIS_FLAGGED
                if(self.__gameboard[row][col] == self.TYPE_MINE):
                    return self.REWARD_FLAG_MINE
                else:
                    return self.PENALTY_FALSE_FLAG
        except IndexError as e:
            return self.PENALTY_MOVE

    def checkWinCondition(self):
        if(self.remaining_tiles <=0):
            self.gamestate = self.GAME_WIN

    def gameOver(self) :
        #Set visibility of all
        self.__visibilityboard = [[ 0 for x in range(self.width)] for y in range(self.height)] 

        #Set game state as finished
        self.gamestate = self.GAME_OVER