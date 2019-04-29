from gameboard import GameBoard
from flask import Flask
import PySimpleGUI as sg


def playVisualGame():
    sg.ChangeLookAndFeel('Dark')      
    sg.SetOptions(element_padding=(0,0))      
    window = sg.Window("Time Tracker",  auto_size_text=False, auto_size_buttons=False,      
                       default_button_element_size=(2,1))      
    
    recording = have_data = False 
    while True:
        
        print("Starting game")  
        gb = GameBoard(16,16)
        gb.printGameBoard()

        sg.ChangeLookAndFeel('Dark')      
        sg.SetOptions(element_padding=(0,0))      

        layout = gb.getGameBoard()

        window = sg.Window("Time Tracker",  auto_size_text=False, auto_size_buttons=False,      
                        default_button_element_size=(2,1))      
        window.Layout(layout)      
        
        recording = have_data = False 
        while True:   

            event, values = window.Read() 

            if(event == None):
                quit()     
            # print(event)      
            if(event == "Reset"):
                window.Close()
                #Break the inner loop to reset the game
                break
            x = event.split(',')
            
            if(len(x) < 2 or len(x)>3):
                print("Invalid input length")
                continue
            
            row = None
            col = None
            F = False
            if(len(x) == 2):
                row,col = x
            else:
                row,col,F = x
            
            
            gb.userInput(int(row),int(col))
            if(gb.gamestate == gb.GAME_WIN):
                print("YOU WIN!!!")
            elif(gb.gamestate == gb.GAME_OVER):
                print("YOU LOSE :(")
            new_board = gb.getGameBoard()
            for row in range(0,gb.height):
                for col in range(0,gb.width):
                    try:
                        if(window.FindElement(str(row)+','+str(col)).GetText() == "F"):
                            window.FindElement(str(row)+','+str(col)).Update("?")
                        if(new_board[row+3][col].GetText() != "?"):
                            if(new_board[row+3][col].GetText() != "F"):
                                window.FindElement(str(row)+','+str(col)).Update(disabled=True)
                            
                            window.FindElement(str(row)+','+str(col)).Update(new_board[row+3][col].GetText())

                    except AttributeError as e:
                        #We need to catch and pass over non button elements
                        pass
                    

            window.Refresh()

    window.Close()

if __name__ == "__main__":

    print("Starting game")  
    gb = GameBoard(16,16)
    gb.printGameBoard()

    # playVisualGame()




    while(gb.gamestate == gb.GAME_RUNNING):
        print("Please input your command in the following format: [row,col,flag(optional)]. Parenthesis are not required")
        user_input = input()
        user_input = str(user_input)
        user_input = user_input.strip()

        user_input = user_input.lstrip('[')
        user_input = user_input.rstrip(']')
        x = user_input.split(',')
        
        if(len(x) < 2 or len(x)>3):
            print("Invalid input length")
            continue
        
        row = None
        col = None
        F = False
        if(len(x) == 2):
            row,col = x
        else:
            row,col,F = x
        gb.userInput(int(row),int(col))
        gb.printGameBoard()
