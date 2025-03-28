# Final Project 2025 

## A comparison study between Monte-Carlo Tree Search and Alpha Beta Minimax on Low and Medium Complexity Games
 
## Overview
This project focuses on gauging the performance between MCTS and a-b minimax in low to medium level complexity environments.
This is accomplished by using a determinstic environment to provide a stable and equal environment for both agents to express their capabilities without hindrance, as to allow their skills to speak for itself. The environment in question are 2 games. With Tic-Tac-Toe representing the low complexity side of things and Connect 4 representing medium complexity. Data is logged and presented in a csv where the user can then interact with it to view the results of their many iterations and draw conclusions. 

## To Enter the Environment
1. **Clone the repository**:
   ```sh
   git clone https://github.com/DavidZaki2004/Final-Project-2025.git
   cd Final-Project-2025

or download the zipfile and unzip it for easy immediate access

## Install Required Dependencies 
*pip install -r requirements.txt*

## To play a Game
Input the following command: *python game.py*

You will be met with this menu: 

![Game Menu Screenshot](assets/game_menu.jpg) 

Follow the steps as instructed to enter the type of match you'd like to see.

Then you will be asked to pick your game type 

![ pick your game menu Screenshot](assets/pick_your_game.jpg)

After choosing the game type, you will see these 2 menus: 

![Choose player 1 menu Screenshot](assets/choose_player_1.jpg) ![Choose player 2 menu Screenshot](assets/choose_player_2.jpg)

These are asking you to pick your respective player in order, so that you get to decide who gets the first move. 

## In-game view
Tic-Tac-Toe board: 

![Tictactoe board Screenshot](assets/ttt_gameboard.jpg)

The board is a 3x3 block with 9 total spaces split up into 9 values starting from the top left (0) and ending in the bottom right (8). The user is expected to input a value between 0 - 8 where an error message will appear if the spot is taken already or does not exist on the board.

Connect4 board: 

![Connect 4 board Screenshot](assets/C4_board.jpg)

The board is split up into 7 columns, starting from 0 - 6. The user picks a value from 0 - 6 and that is where their token/coin will drop. 

**It is important to keep these values in mind for smooth playing experience!**

If you have chosen to play against MCTS or against Minimax, a move evaluation output exists to help illustrate the mathematics going on in the background. It will be show up as so:

![MCTS move evaluation Screenshot](assets/mcts_evaluation.jpg)
![ab minimax move evaluation Screenshot](assets/minimax_evaluation.jpg)

## Data and Tables
To access the tables and/or the raw data you could visit the *game_result.csv* file where any completed game is logged there with relevant data. Otherwise you could use the command *python table.py* in the terminal to generate a table that contains all the relevant data for the chosen categories (csv headers), the tables display various pieces of information as to try and provide a coherent breakdown of information to allow for easier digestion of all the information.
![table Screenshot](assets/table.jpg)

## Adjusting Difficulty 
This comes in a few steps, the difficulty is controlled mostly by the max_depth in the case of ab_minimax and iterations in the case of MCTS, by tweaking those values in the classes you will be able to adjust the difficulty. Traditionally, the academic paper follows 2 metrics of difficulty which are Easy and Hard. These changes can be done in the *player.py* file. 

### Under Tic-Tac-Toe
- **Minimax**: Easy Mode = 2 max_depth | Hard Mode = 3 max_depth
- **MCTS**: Easy Mode = 1500 iterations | Hard Mode = 3000 iterations

### Under Connect-4
- **Minimax**: Easy Mode = 3 max_depth | Hard Mode = 4 max_depth
- **MCTS**: Easy Mode = 2000 iterations | Hard Mode = 4000 iterations