from random import random

class Minesweeper:

    def __init__(self):
        self.boardsize, self.prob = self.settings_menu()
        self.game_over = False
        self.game_won = False
        self.clicked_tiles = 0
        self.safe_tiles = 0
        self.board = self.create_board()
        self.set_board_indicators()

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
            bomb_prob = 0.2
        elif sel == 2:
            bomb_prob = 0.35
        else:
            bomb_prob = 0.5
        return dim, bomb_prob  
        
    def start_game(self):
        running = True
        while running:
            print()
            self.display()
            ij = input("Enter the tile you want to dig into (row,col): ")
            flag = input("Flag: ")
            i,j = ij.split(",")
            i = ord(i) - 64 
            j = int(j)
            
            
            if not (0 < i <= self.boardsize[0] and 0 < j <= self.boardsize[1]):
                print()
                print("Tile out of bounds, try again")
                print()
            self.make_move(i,j, flag)
            if self.game_over:
                print()
                print("GAME OVER")
                print(f"{chr(i+64)}{j} was a mine :(")
                print()
                self.board[i][j].clicked = True
                self.display()
                running = False
                continue
            if self.clicked_tiles == self.safe_tiles:
                print()
                print("!!! YOU'RE WINNER !!!")
                print()
                self.display()
                running = False 

    def make_move(self, i, j, flag):
        if self.board[i][j].clicked:
            print()
            print("You've already dug here, try again")
            print()
        else:
            if flag:
                self.board[i][j].flag = True 
            else:
                if self.board[i][j].hide_bomb:
                    self.game_over = True
                elif self.board[i][j].num_ind > 0:
                    self.board[i][j].clicked = True
                    self.clicked_tiles += 1
        return

    def display(self):
        for row in self.board:
            for data in row:
                print(f"{data}", end="")
            print()

    def create_board(self):
        self.board = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.board.append([])
        for j in range(self.boardsize[1]+1):
                self.board[0].append(f" {j}")
        self.board[0][0] = " "
        for i in range(1, self.boardsize[0]+1):
            self.board.append([])
            self.board[i].append(alphabet[i-1])
            for j in range(1, self.boardsize[1]+1):
                hide_bomb = random() < self.prob
                if not hide_bomb:
                    self.safe_tiles += 1
                tile = Tile(hide_bomb)
                self.board[i].append(tile)
        return self.board

    def set_board_indicators(self):
        for i in range(1, self.boardsize[0]+1):
            for j in range(1, self.boardsize[1]+1):
                if self.board[i][j].hide_bomb:
                    continue
                num_ind = self.get_num_bomb_around(i,j)
                self.board[i][j].num_ind = num_ind
                if self.board[i][j].num_ind == 0:
                    self.board[i][j].clicked = True
                    self.clicked_tiles += 1

    def get_num_bomb_around(self, row, col):
        num_bomb_around = 0       
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                inbounds = (0 < i <= self.boardsize[0]) and (0 < j <= self.boardsize[1])
                same = (i == row) and (j == col)
                if (not same) and inbounds:
                    if self.board[i][j].hide_bomb:
                        num_bomb_around += 1
        return num_bomb_around 

class Tile:

    def __init__(self, hide_bomb):
        self.hide_bomb = hide_bomb
        self.num_ind = 0
        self.flag = False
        self.clicked = False

    def __str__(self):
        if not self.clicked and not self.flag:
            string = " ◙"
        elif self.flag:
            string = " †"
        else: #HERE
            if not self.hide_bomb:
                if self.num_ind != 0:
                    string = f" {self.num_ind}"
                else:
                    string = "  "
            else: 
                string = " ☼" 
        return string

    def __repr__(self):
        return f"Tile({self.hide_bomb},{self.num_ind},{self.clicked})"

def main_menu():
    exit = False
    while not exit:
        sel = 0
        while not 1 <= sel <= 3: 
            print()
            print("MINESWEEPER 0.1 HOME MENU")
            print("1. Start Game")
            print("2. How-To-Play")
            print("3. Quit")
            sel = int(input("Choice: "))
        if sel == 1:
            minesweeper = Minesweeper()
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
Once the tile selected two options is offered to the player:
    -Dig
    -Flag/Unflag

The 'Dig' action reveals what is under the tile.
The 'Flag' action marks the tile as suspect, easing grid navigation.
A flagged tile can always be unflagged by the player simply by flagging it again.

CHANGELOG 2022-05-04: Flag action not yet implemented""")
        else:
            exit = True

    
main_menu()