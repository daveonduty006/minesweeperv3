from board import Board 

exit = False
while not exit:
    sel = 0
    while not 1 <= sel <= 3: 
        print()
        print("MINESWEEPER v3 HOME MENU")
        print("1. Start Game")
        print("2. How-To-Play")
        print("3. Quit")
        sel = int(input("Choice: "))
    if sel == 1:
        minesweeper = Board()
        minesweeper.start_game()
    elif sel == 2:
        print()
        print("""Minesweeper is a game where mines are hidden in a grid of tiles.
Safe tiles have numbers telling you how many mines touch it. 
You use the number clues to solve the game by digging all of the safe tiles.
If you dig a mine you lose the game!
WIN CONDITION:
The number of undigged tiles is equal to the number of mines on the board.
GAME FLOW:
At each turn in the game the player is requested to input a set of tile coordinate. 
Once the tile is selected two options are offered to the player:
    -Place/Remove a Flag here
    -Start Digging here
The 'Dig' action reveals what is under the tile.
The 'Flag' action marks the tile as suspect, easing grid analysis.
A flagged tile can always be unflagged by the player simply by flagging it again.""")
    else:
        exit = True