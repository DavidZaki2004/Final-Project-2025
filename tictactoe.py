import time
from player import MCTSPlayer  # Importing the Monte Carlo Tree Search player class

class TicTacToe:
    """
    A class representing a Tic-Tac-Toe game.
    Handles board state, move validation, and win conditions.
    """

    def __init__(self):
        """Initialize an empty 3x3 Tic-Tac-Toe board."""
        self.board = [" " for _ in range(9)]  # Represents a 3x3 board in a 1D list
        self.current_winner = None  # Tracks the current winner (X or O)
        self.last_move = None  # Stores the last move made

    def print_board(self):
        """Prints the Tic-Tac-Toe board in a readable format."""
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        """Returns a list of available move positions (indices) on the board."""
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        """Checks if there are any empty squares left on the board."""
        return " " in self.board

    def num_empty_squares(self):
        """Returns the number of empty squares left on the board."""
        return self.board.count(" ")

    def make_move(self, square, letter):
        """
        Places a move on the board if the square is empty.

        Args:
            square (int): The board position where the move is made.
            letter (str): The player making the move ('X' or 'O').

        Returns:
            bool: True if move was successful, False otherwise.
        """
        if self.board[square] == " ":
            self.board[square] = letter
            self.last_move = square  # Store the last move made
            if self.winner(square, letter):
                self.current_winner = letter  # Update the winner if the move results in a win
            return True
        return False

    def winner(self, square, letter):
        """
        Checks if the current move results in a win.

        Args:
            square (int): The last move made.
            letter (str): The player making the move ('X' or 'O').

        Returns:
            bool: True if the player has won, False otherwise.
        """
        row_ind = square // 3  # Determine row index
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):  # Check if all spots in the row match
            return True

        col_ind = square % 3  # Determine column index
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):  # Check if all spots in the column match
            return True

        if square % 2 == 0:  # Check diagonals (only possible for certain squares)
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # Left to right diagonal
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # Right to left diagonal
            if all([spot == letter for spot in diagonal1]) or all([spot == letter for spot in diagonal2]):
                return True

        return False  # No winning condition met

    def copy(self):
        """
        Creates a copy of the current game state.

        Returns:
            TicTacToe: A new instance of the TicTacToe game with the same board state.
        """
        new_game = TicTacToe()
        new_game.board = self.board[:]
        new_game.current_winner = self.current_winner
        new_game.last_move = self.last_move  # Copy the last move
        return new_game


def play_tictactoe(game, x_player, o_player, print_game=True, move_times=None, game_moves=None, blocked_wins=None, missed_wins=None):
    """
    Runs a game of Tic-Tac-Toe between two players.

    Args:
        game (TicTacToe): An instance of the TicTacToe game.
        x_player (Player): The player controlling 'X'.
        o_player (Player): The player controlling 'O'.
        print_game (bool): Whether to print the game progress.
        move_times (list): Stores the time taken per move.
        game_moves (list): Stores the sequence of moves.
        blocked_wins (dict): Tracks blocked opponent winning moves.
        missed_wins (dict): Tracks missed winning moves.

    Returns:
        str: The winner ('X' or 'O') or 'Tie' if the game ends in a draw.
    """
    letter = "X"  # X always starts the game

    while game.available_moves():
        start_time = time.time()  # Track move time

        # Store available moves before making a decision
        available_moves_before = set(game.available_moves())

        # Step 1: Identify if the opponent had an **immediate winning move**
        opponent = "O" if letter == "X" else "X"
        opponent_winning_moves = []
        for move in available_moves_before:
            temp_game = game.copy()
            if temp_game.make_move(move, opponent) and temp_game.current_winner == opponent:
                opponent_winning_moves.append(move)

        # Step 2: Check for an **immediate winning move** for the current player
        immediate_winning_moves = []
        if missed_wins is not None:
            for move in available_moves_before:
                temp_game = game.copy()
                if temp_game.make_move(move, letter) and temp_game.current_winner == letter:
                    immediate_winning_moves.append(move)
            missed_move_detected = bool(immediate_winning_moves)

        # Step 3: Retrieve move values if MCTS is used
        move_values = {}
        move_percentages = {}
        if isinstance(x_player, MCTSPlayer) or isinstance(o_player, MCTSPlayer):
            move_values, move_percentages = x_player.get_move_values(game) if letter == "X" else o_player.get_move_values(game)

        # Step 4: The player makes a move
        square = o_player.get_move(game) if letter == "O" else x_player.get_move(game)

        # Step 5: Execute the move and update tracking lists
        if game.make_move(square, letter):
            move_time = time.time() - start_time  # Compute move duration
            if move_times is not None:
                move_times.append(move_time)
            if game_moves is not None:
                game_moves.append(square)

            # Step 6: Track missed winning opportunities
            if missed_wins is not None and missed_move_detected:
                if square not in immediate_winning_moves:
                    missed_wins[letter] += 1  # Increment missed wins count

            # Step 7: Track blocked opponent wins
            if blocked_wins is not None:
                if opponent_winning_moves and any(move in opponent_winning_moves for move in available_moves_before):
                    if square in opponent_winning_moves:
                        blocked_wins[letter] += 1  # Increment blocked wins count

            # Step 8: Print move and evaluation details if enabled
            if print_game:
                print(f"{letter} makes a move to square {square}")
                game.print_board()
                print()

                if move_percentages:
                    print(f"Move choices by MCTS (percentages): {move_percentages}")
                if move_values:
                    print(f"Move values by Minimax: {move_values}")

            # Step 9: Check for a winner
            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter

            # Step 10: Switch turns
            letter = "O" if letter == "X" else "X"

    # If the loop exits, the game is a tie
    if print_game:
        print("It's a tie!")
    return "Tie"
