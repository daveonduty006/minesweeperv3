class Tile:

    def __init__(self, hide_bomb):
        self.hide_bomb = hide_bomb
        self.num_ind = 0
        self.flagged = False
        self.clicked = False

    # 'Magic' method allowing the tile object to be printed on the screen in one of the following
    # characters...
    def __str__(self):
        if not self.clicked:
            if self.flagged:
                string = f" {'†'} "
            else:
                string = f" {'◙'} "
        else:            
            if not self.hide_bomb:
                if self.num_ind != 0:
                    string = f" {self.num_ind} "
                else:
                    string = "   "
            else: 
                string = f" {'☼'} " 
        return string