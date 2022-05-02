from random import random

class Minesweeper:

    def __init__(self, boardsize=None, bomb_probability=None):
        self.boardsize, self.prob = self.menu()
        self.game_over = False
        self.game_won = False
        self.clicked_tiles = 0
        self.safe_tiles = 0
        self.board = self.create_board()
        #print(self.board)

    def menu(self):
        print("CHOOSE THE BOARD DIMENSION: ")
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
            bomb_prob = 0.1
        elif sel == 2:
            bomb_prob = 0.2
        else:
            bomb_prob = 0.3
        return dim, bomb_prob  

    def start_game(self):
        running = True
        while running:
            pass   

    def create_board(self):
        self.board = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.board.append([])
        for i in range(self.boardsize[1]+1):
                self.board[0].append(f" {i}")
        self.board[0][0] = " "
        for i in range(1, self.boardsize[0]+1):
            self.board.append([])
            self.board[i].append(alphabet[i-1])
            for j in range(self.boardsize[1]):
                hide_bomb = random() < self.prob
                if not hide_bomb:
                    self.safe_tiles += 1
                tile = Tile(hide_bomb) 
                self.board[i].append(tile)
        return self.board  

    def display(self):
        for line in self.board:
            for data in line:
                print(f"{data}", end ="")
            print()

class Tile:

    def __init__(self, hide_bomb):
        self.hide_boom = hide_bomb
        self.neighbors = []
        self.clicked = False
        self.flagged = False

    def __repr__(self):
        return f"Tile({self.hide_boom})"

    def __str__(self):
        bomb_str = "☼" if self.hide_boom else "◙"
        return f" {bomb_str}"


    
M = Minesweeper()
M.display()
