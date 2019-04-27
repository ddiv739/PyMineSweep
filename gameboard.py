from pprint import pprint
from random import randint
class GameBoard:
    width = None
    height = None
    __gameboard = None
    __visibilityboard = None
    mines = None
    TYPE_MINE = -1

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mines = (width*height)/4
        self.__gameboard = [[0 for x in range(width)] for y in range(height)] 
        self.__visibilityboard = [[ False for x in range(width)] for y in range(height)] 
        pprint(self.__gameboard)

        mine_count = self.mines

        while(mine_count > 0):
            #find random position. if not populate then populate and decrement else skip
            row , col = randint(0, height-1) , randint(0, width-1)

            if(self.__gameboard[row][col] == -1):
                continue
            self.__gameboard[row][col] = -1
            mine_count-=1

        pprint(self.__gameboard)