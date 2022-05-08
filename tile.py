class Tile:

    def __init__(self, hide_bomb):
        self.hide_bomb = hide_bomb
        self.num_ind = 0
        self.flagged = False
        self.clicked = False

    def __str__(self):
        if not self.clicked:
            if self.flagged:
                string = f" {'†'} "
            else:
                string = f" {'◙'} "
        else: #HERE            
            if not self.hide_bomb:
                if self.num_ind != 0:
                    string = f" {self.num_ind} "
                else:
                    string = "   "
            else: 
                string = f" {'☼'} " 
        return string

    def __repr__(self):
        return f"Tile({self.hide_bomb})"