from gameboard import GameBoard
from flask import Flask
import PySimpleGUI as sg



if __name__ == "__main__":
    """      
    Demonstrates using a "tight" layout with a Dark theme.      
    Shows how button states can be controlled by a user application.  The program manages the disabled/enabled      
    states for buttons and changes the text color to show greyed-out (disabled) buttons      
    """      



    print("Starting game")  
    gb = GameBoard(16,16)
    gb.printGameBoard()


    sg.ChangeLookAndFeel('Dark')      
    sg.SetOptions(element_padding=(0,0))      

    layout = [[sg.Text('Minesweeper')],     
              [sg.Button('f', button_color=('white', 'black'), key='Start'),      
               sg.Button('s', button_color=('white', 'black'), key='Stop'),      
               sg.Button('?', button_color=('white', 'firebrick3'), key='Reset'),      
               sg.Button('3', button_color=('white', 'springgreen4'), key='Submit')]      
              ]    

    layout = gb.getGameBoard()

    window = sg.Window("Time Tracker",  auto_size_text=False, auto_size_buttons=False,      
                       default_button_element_size=(2,1))      
    window.Layout(layout)      
    
    recording = have_data = False      
    while True:   

        event, values = window.Read() 

        if(event == None):
            break     
        print(event)      
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
        gb.printGameBoard()

        new_board = gb.getGameBoard()
        for row in range(0,gb.height):
            for col in range(0,gb.width):
                if(new_board[row][col].GetText() != "?"):
                    window.FindElement(str(row)+','+str(col)).Update(new_board[row][col].GetText(),disabled=True)
                
        
        window.Refresh()
    window.Close()



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

    if(gb.gamestate == gb.GAME_WIN):
        print("YOU WIN!!!")
    else:
        print("YOU LOSE :(")
    gb.printDebugBoard()

