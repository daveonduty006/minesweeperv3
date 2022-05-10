from tile import Tile 
from random import random

class Board:

    def __init__(self):
        self.boardsize, self.prob = self.settings_menu()
        self.game_over = False
        self.game_won = False
        self.clicked_tiles = 0
        self.safe_tiles = 0
        self.board = self.create_board()
        self.set_board_indicators()

    # Method allowing the player to define the board dimensions and overall difficulty
    # (the difficulties are tied to the probability of if a tile is harboring a bomb/mine).
    def settings_menu(self):
        print()
        print("CHOOSE THE BOARD DIMENSIONS: ")
        rows = int(input("NUMBER OF ROWS: "))
        cols = int(input("NUMBER OF COLUMNS: "))
        dim = rows, cols
        sel = 0
        while not 1 <= sel <= 3: 
            print("CHOOSE THE DIFFICULTY: ")
            print("1. EASY")
            print("2. NORMAL")
            print("3. HARD")
            sel = int(input("CHOICE: "))
        if sel == 1:
            bomb_prob = 0.2  # 20% chance that each tile is hiding a mine
        elif sel == 2:
            bomb_prob = 0.35 # 35% chance that each tile is hiding a mine
        else:
            bomb_prob = 0.5  # 50% chance that each tile is hiding a mine
        return dim, bomb_prob  
        
    # Method containing the game loop
    def start_game(self):
        running = True
        while running:
            print()
            self.display()
            # The player is asked to enter a tile coordinates (ex: A5)
            ij = input("Where do you want to go? (row+col): ")\
                .replace(",","").replace(" ","").replace("+","").upper()
            i, j = ij[0], ij[1:]
            i = ord(i) - 64 
            j = int(j)
            # The coordinates are run through a validity check (are we out of bounds?)
            if not (0 < i <= self.boardsize[0] and 0 < j <= self.boardsize[1]):
                print()
                print("Tile out of bounds, try again")
                continue                   
            # The player is asked to select an action to perform on the selected tile  
            sel = 0
            while not 1 <= sel <= 2:
                print()
                print("What do you want to do here?")
                print("1. Place/Remove a Flag")
                print("2. Start Digging!")
                sel = int(input("Choice: "))
            # The flag action toggles flag on or off of the selected tile 
            if sel == 1:
                self.board[i][j].flagged = False if self.board[i][j].flagged else True
                continue
            # The digging action calls the make_move method 
            else:                
                self.make_move(i, j)
            # We check if the dug tile has triggered our game over condition 
            # (the tile was hiding a mine)
            if self.game_over:
                print()
                print("GAME OVER")
                print(f"{chr(i+64)}{j} was a mine :(")
                for i in range(1, self.boardsize[0]+1):
                    for j in range(1, self.boardsize[1]+1):
                        self.board[i][j].clicked = True
                self.display()
                running = False
                continue
            # Likewise, we check if the dug tile has triggered our win condition
            # (all safe tiles have been selected by the player)
            elif self.clicked_tiles == self.safe_tiles:
                print()
                print("!!! YOU'RE WINNER !!!")
                for i in range(1, self.boardsize[0]+1):
                    for j in range(1, self.boardsize[1]+1):
                        self.board[i][j].clicked = True
                self.display()
                running = False 

    # Method allowing the player's selected tile to be dug
    def make_move(self, i, j):
        if self.board[i][j].clicked:
            print()
            print("You've already dug here, try again")
        else:
                if self.board[i][j].hide_bomb:
                    self.game_over = True
                elif self.board[i][j].num_ind > 0:
                    self.board[i][j].clicked = True
                    self.clicked_tiles += 1

    # Method displaying the state of the board on the console
    def display(self):
        for row in self.board:
            for data in row:
                print(f"{data}", end="")
            print()

    # The bomb assignment by probability process is inspired by Daniel Chang's pygame minesweeper
    # URL: https://github.com/danielchang2002/Pygame/blob/main/Minesweeper/board.py
    # Method generating a new board (the board will be a 2D array)
    def create_board(self):
        self.board = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.board.append([])
        # Our first row is being created here
        # This row will contains the column index (col1=1, col13=13, etc)
        for j in range(self.boardsize[1]+1):
            if j < 10:
                self.board[0].append(f" {j} ")
            else:
                self.board[0].append(f" {j}")
        self.board[0][0] = "  "
        # Our additional rows are being created here
        # The first data on each row from now on will be our row index (row1=A,row13=M, etc)
        for i in range(1, self.boardsize[0]+1):
            self.board.append([])
            self.board[i].append(f"{alphabet[i-1]} ")
            # The game objects (our tiles) will be instanciated here
            # A boolean value will determine whether the instanciated tile 
            # will have a mine (True/False), dynamically placing the mines on our board
            for j in range(1, self.boardsize[1]+1):
                hide_bomb = random() < self.prob
                # We increment our safe_tiles board attribute if the tile doesn't have a mine
                # This final number will determine how many tiles the player must uncover before
                # triggering the win condition in the game loop
                if not hide_bomb:
                    self.safe_tiles += 1
                tile = Tile(hide_bomb)
                self.board[i].append(tile)
        return self.board

    # The number assignment process is inspired by Kylie Ying's command-line minesweeper
    # URL: https://github.com/kying18/minesweeper/blob/main/minesweeper.py
    # Method assigning the tile object num_ind attribute (how many mines are touching the tile)
    def set_board_indicators(self):
        for i in range(1, self.boardsize[0]+1):
            for j in range(1, self.boardsize[1]+1):
                if self.board[i][j].hide_bomb:
                    continue
                num_ind = self.get_num_bomb_around(i,j)
                self.board[i][j].num_ind = num_ind
                # This version of minesweeper have all zero-tiles (no mines around it) uncovered 
                # at the start of the game (they are revealed automatically)
                if self.board[i][j].num_ind == 0:
                    self.board[i][j].clicked = True
                    self.clicked_tiles += 1

    # Method counting and returning the number of mines touching the tile by 
    # looking up its neighbors
    def get_num_bomb_around(self, row, col):
        num_bomb_around = 0       
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                # We check if the neighbor we are looking at is within the game boundaries
                # If it isn't, then the neighbor doesn't actually exist...
                inbounds = (0 < i <= self.boardsize[0]) and (0 < j <= self.boardsize[1])
                # We also check if the place on the board we are looking at isn't the tile itself
                same = (i == row) and (j == col)
                # If we are inbounds and the tile isn't looking at itself then...
                if (not same) and inbounds:
                    # We check if the neighboring tile hides a mine
                    if self.board[i][j].hide_bomb:
                        # In which case we increase our tile number indicator :)
                        num_bomb_around += 1
        return num_bomb_around 