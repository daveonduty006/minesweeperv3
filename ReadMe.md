# Minesweeper :triangular_flag_on_post:

## Description 
### Context
    This terminal version of the popular video game Minesweeper is a school term project, developed by a 3-person team. 
    The game is thoroughly playable in 5 minutes and has a player menu. An object-oriented programming (OOP) approach was used during the game development.
 
### Realisation
    Minesweeper is a game where mines are hidden in a grid of tiles.
    Safe tiles have numbers telling you how many mines touch it. You use the number clues to solve the game by digging all of the safe tiles.
    If you dig a mine you lose the game!

    WIN CONDITION:
    The number of undigged tiles is equal to the number of mines on the board.

    GAME FLOW:
    At each turn in the game the player is requested to input a set of tile coordinate. 
    Once the tile is selected two options are offered to the player:
        -Place/Remove a Flag here
        -Start Digging here
    The 'Dig' action reveals what is under the tile, stepping game progression.
    The 'Flag' action marks the tile as suspect, easing grid analysis.
    A flagged tile can always be unflagged by the player by simply flagging it again.


## Installation 
    Requires Python 3

## Authors and Thank-You's 
[Martin Normandin](https://github.com/MartinNormandin) 

[David Normandin](https://github.com/daveonduty006) 

[Maxime Bellavance](https://github.com/Maxb416) 

A very big thank you to our teacher [Keven Presseau St-Laurent](https://github.com/kpresseau) for his wise guidance and epic patience shown in face of asinine newbie questions and shady excuses.

## Licence 
None

## State of the Project 
Ready for evaluation