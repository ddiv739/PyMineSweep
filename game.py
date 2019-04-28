from gameboard import GameBoard


if __name__ == "__main__":
    print("Starting game")  
    gb = GameBoard(16,16)

    gb.printGameBoard()
    while(gb.gamestate != gb.GAME_OVER):
        print("Please input a command")
        user_input = input("Please input your command in the following format: [row,col]. Parenthesis are not required")
        user_input = str(user_input)
        user_input = user_input.strip()
        user_input = user_input.lstrip('[')
        user_input = user_input.rstrip(']')
        row,col = user_input.split(',')
        print(user_input)

        gb.userInput(int(row),int(col))

        gb.printGameBoard()