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
            ########################
            ij = input("Where do you want to go? (row+col): ")\
                .replace(",","").replace(" ","").replace("+","").upper()
            i, j = ij[0], ij[1:]
            i = ord(i) - 64 
            j = int(j)
            ########################
            if not (0 < i <= self.boardsize[0] and 0 < j <= self.boardsize[1]):
                print()
                print("Tile out of bounds, try again")
                continue                   
            ########################   
            sel = 0
            while not 1 <= sel <= 2:
                print()
                print("What do you want to do here?")
                print("1. Place/Remove a Flag")
                print("2. Start Digging!")
                sel = int(input("Choice: "))
            ########################
            if sel == 1:
                self.board[i][j].flagged = False if self.board[i][j].flagged else True
                continue
            ########################
            else:                
                self.make_move(i, j)
            ########################
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
            ########################
            elif self.clicked_tiles == self.safe_tiles:
                print()
                print("!!! YOU'RE WINNER !!!")
                for i in range(1, self.boardsize[0]+1):
                    for j in range(1, self.boardsize[1]+1):
                        self.board[i][j].clicked = True
                self.display()
                running = False 

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
            if j < 10:
                self.board[0].append(f" {j} ")
            else:
                self.board[0].append(f" {j}")
        self.board[0][0] = "  "
        for i in range(1, self.boardsize[0]+1):
            self.board.append([])
            self.board[i].append(f"{alphabet[i-1]} ")
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