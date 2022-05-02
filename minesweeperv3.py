import pygame
import os 
from random import random
from time import sleep


class Board:

    def __init__(self):
        self.screensize, self.arraysize, self.prob = self.menu()
        self.tilesize = (self.screensize[0]//self.arraysize[0],\
                         self.screensize[1]//self.arraysize[1])
        self.game_over = False
        self.win = False
        self.clicked_tiles = 0
        self.safe_tiles = 0            
        self.load_images()
        self.array = self.create_array()

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screensize)
        self.game_loop()

    def game_loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    array_xy = pygame.mouse.get_pos()
                    toggle_flag = pygame.mouse.get_pressed()[2]
                    self.define_action(array_xy, toggle_flag)
            self.print_board()
            pygame.display.flip()
            if self.win:
                sleep(5)
                run = False
        pygame.quit()         

    def menu(self):
        sel = 0
        while not 1 <= sel <= 3: 
            print("CHOOSE YOUR DIFFICULTY LEVEL: ")
            print("1. Easy (9x9 Board, 10% Bomb Probability)")
            print("2. Normal (18x18 Board, 20% Bomb Probability)")
            print("3. Hard (36x36 Board, 30% Bomb Probability)")
            sel = int(input("Selection: "))
        if sel == 1:
            self.screensize = (800,800)
            self.arraysize = (9,9)
            self.prob = (0.1)
        elif sel == 2:
            self.screensize = (800,800)
            self.arraysize = (18,18)
            self.prob = (0.2)
        else:
            self.screensize = (800,800)
            self.arraysize = (36,36)
            self.prob = (0.3)
        return self.screensize, self.arraysize, self.prob        

    def load_images(self):
        self.images = {}
        # This for loop will create a dictionary of images from the images folder
        for filename in os.listdir("images"):
            image = pygame.image.load(f"images/{filename}")
            # Rescale the image into the tile_size dimensions 
            image = pygame.transform.scale(image, self.tilesize)
            # Allow access to an image via a dictionary key without the file extension
            self.images[filename.replace(".png", "")] = image

    def create_array(self):
        # This will create a 2D array with bombs on certain tiles
        self.array = []
        for row in range(self.arraysize[0]):
            row = []
            for col in range(self.arraysize[1]):
                # This will return a boolean value regarding if a random float is 
                # greater or not than the bomb probability set during the Board initialisation
                # The float is randomly chosen via the imported random method
                # If False, the number of safe tiles is increased by 1
                boom = random() < self.prob 
                if not boom:
                    self.safe_tiles += 1
                # Reminder: boom is a boolean value 
                tile = Tile(boom)
                row.append(tile)
            self.array.append(row)
        # This will attribute a list of neighbors (nearby tiles) to each tiles
        for row in range(self.arraysize[0]):
            for col in range(self.arraysize[1]):
                tile_xy = (row,col)
                neighbors = self.get_neighbors(tile_xy)
                tile.set_neighbors(neighbors)
        return self.array

    def get_neighbors(self, tile_xy):
        # This will generate a list of neighbors relative to the incoming tile position
        neighbors = []
        # We will set which neighbors are surrounding the tile 
        for row in range(tile_xy[0]-1, tile_xy[0]+2):
            for col in range(tile_xy[1]-1, tile_xy[1]+2):
                # This boolean will be False if one neighbor of the tile doesn't exist
                out_of_bounds = row < 0 or row >= self.arraysize[0] or\
                              col < 0 or col >= self.arraysize[1]
                # This boolean will be True if the neighbor is actually the tile itself 
                same = (row == tile_xy[0]) and (col == tile_xy[1])
                # This check will skip the append if either condition is True 
                if same or out_of_bounds:
                    continue
                neighbors.append(self.array[row][col])
        return neighbors 

    def print_board(self):
        # Starting from the position (0, 0) in the array 
        start = (0, 0)
        for row in range(self.arraysize[0]):
            for col in range(self.arraysize[1]):
                tile_xy = (row,col)
                tile = self.get_tile(tile_xy)
                # We access the image via the get_image method 
                image = self.get_image(tile)
                # We draw the image of the first tile on the screen surface
                self.screen.blit(image, start)
                # We will define the next tile to be draw in the row by 
                # incrementing our next start by the WIDTH of a tile
                start = ( (start[0]+self.tilesize[0]), start[1])
            # We will define the first tile to be draw in the next row by
            # incrementing our next start by the HEIGHT of a tile
            start = ( 0, (start[1]+self.tilesize[1]) )

    def get_tile(self, tile_xy):
        return self.array[tile_xy[0]][tile_xy[1]] 

    def get_image(self, tile):
        # This method will return the appropriate tile image by passing through these following checks:
        image = ""
        # If the tile get left-clicked on 
        if tile.get_revealed():
            # If the tile hides a mine
            if tile.get_boom():
                image = "bomb_at_clicked_block"
            else:
                image = str(tile.get_mine_around())
        else:
            # If the tile has been flagged by the player
            if tile.get_flagged():
                image = "flag"
            # If the tile has been recursively revealed 
            else:
                image = "empty_block"
        return self.images[image]

    def define_action(self, array_xy, toggle_flag):
        if self.game_over:
            return
        tile_xy = (array_xy[1] // self.tilesize[1],\
                   array_xy[0] // self.tilesize[0])
        tile = self.get_tile(tile_xy)
        ###########################################
        if tile.get_revealed() or (not toggle_flag and tile.get_flagged()):
            return
        elif toggle_flag:
            tile.set_flag()
            return
        ###########################################
        tile.set_reveal()
        if tile.get_boom():
            self.game_over = True
            return
        self.safe_tiles += 1
        if tile.get_mine_around() != 0:
            return 
        for neighbor in tile.get_neighbors():
            if (not neighbor.get_boom()) and (not neighbor.get_revealed()):
                self.define_action(neighbor, False)


class Tile:

    def __init__(self, boom):
        self.boom = boom
        self.revealed = False
        self.flagged = False
        self.mine_around = 0
        self.neighbors = [] 

    def get_boom(self):
        return self.boom

    # This add the number of mines in the area (3x3) of each tile (centerpiece of the 3x3 area)
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        for neighbor in self.neighbors:
            # Check if the tile in question returns True (it is hiding a mine)
            if neighbor.get_boom():
                self.mine_around += 1

    def get_revealed(self):
        return self.revealed

    def get_mine_around(self):
        return self.mine_around 

    def get_flagged(self):
        return self.flagged

    def set_flag(self):
        self.flagged = not self.flagged

    def set_reveal(self):
        self.revealed = True

    def get_neighbors(self):
        return self.neighbors

    def __repr__(self):
        return f"Tile({self.boom})"

        

    
            






board = Board()
board.start_game()
