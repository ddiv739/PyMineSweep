import random
from gameboard import GameBoard
REWARD_WIN = 750
REWARD_FLAG_MINE = 50
REWARD_CLEARED_TILE = 5

PENALTY_MOVE = -1
PENALTY_LOSS = -250
PENALTY_FALSE_FLAG = -20

class ReinforcementAgent:
    gameboard = None

    def __init__(self,gameboard : GameBoard):
        self.gameboard = gameboard    

    def analyseMoveReward(self):
        pass

    def make_move(self, parameter_list):
        pass
    
    def random_step(self):
        #(row,col)
        return (random.randint(self.gameboard.width),random.randint(self.gameboard.height))



