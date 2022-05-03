from random import random

class Minesweeper:

    def __init__(self, boardsize=None, bomb_probability=None):
        self.boardsize, self.prob = self.menu()
        self.game_over = False
        self.game_won = False
        self.clicked_tiles = 0
        self.safe_tiles = 0
        self.board = self.create_board()

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
            bomb_prob = 0.25
        elif sel == 2:
            bomb_prob = 0.4
        else:
            bomb_prob = 0.5
        return dim, bomb_prob  

    def start_game(self):
        running = True
        while running:
            self.display()
            #i = input(which row...)
            #j = input(which column...)
            #check = self.make_move(i,j)
            #if not check:
                #self.game_over = True
            #if check:
                #reveal tile 
            pass 

    def make_move(self, i, j):
        if self.board[i][j] == "☼":
            return False
        elif self.board[i][j].mine_around > 0:
            return True
        pass

    def display(self):
        for row in self.board:
            for data in row:
                print(f"{data}", end ="")
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
        self.find_tile_neighbors()
        return self.board

    def find_tile_neighbors(self):
        for i in range(1, self.boardsize[0]+1):
            for j in range(1, self.boardsize[1]+1):
                tile = self.board[i][j]
                neighbors = self.get_tile_neighbors( (i,j) )
                tile.set_neighbors(neighbors)

    def get_tile_neighbors(self, tile_pos):
        neighbors = []
        for i in range(tile_pos[0]-1, tile_pos[0]+2):
            for j in range(tile_pos[1]-1, tile_pos[1]+2):
                # This boolean will be False if one neighbor of the tile doesn't exist
                out_of_bounds = i < 1 or i >= self.boardsize[0]+1 or\
                                j < 1 or j >= self.boardsize[1]+1
                # This boolean will be True if the neighbor is actually the tile itself 
                same = (i == tile_pos[0]) and (j == tile_pos[1])
                if same or out_of_bounds:
                    continue
                neighbors.append(self.board[i][j])
        return neighbors

class Tile:

    def __init__(self, hide_bomb):
        self.hide_bomb = hide_bomb
        self.neighbors = []
        self.mine_around = 0
        self.clicked = False
        self.flagged = False

    def set_neighbors(self, neighbors_list):
        # This method receives a list of neighbors from self.board (Minesweeper-object attribute)
        self.neighbors = neighbors_list
        print(self.neighbors)
        for neighbor in self.neighbors:
            if neighbor.hide_bomb:
                self.mine_around += 1
        print(self.mine_around)

    def __str__(self):
        bomb_str = "☼" if self.hide_bomb else "◙"
        return f" {bomb_str}"

    def __repr__(self):
        return f"Tile({self.hide_bomb})"



    
M = Minesweeper()
#M.start_game()
M.display()
