import time

class Connect4:
    """
    A class representing a Connect 4 game.
    Manages board state, move validation, and win conditions.
    """

    def __init__(self):
        """Initializes a 6x7 Connect 4 board."""
        self.rows = 6  # Number of rows
        self.cols = 7  # Number of columns
        self.board = self.make_board()  # Create an empty board
        self.current_winner = None  # Tracks the current winner
        self.last_move = None  # Stores the last move made

    def make_board(self):
        """Creates an empty 6x7 Connect 4 board."""
        return [[" " for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self):
        """Prints the Connect 4 board in a readable format."""
        for row in self.board:
            print("| " + " | ".join(row) + " |")
        print("  " + "   ".join(map(str, range(self.cols))))  # Print column numbers

    def available_moves(self):
        """Returns a list of available columns where a move can be made."""
        return [col for col in range(self.cols) if self.board[0][col] == " "]

    def make_move(self, col, letter):
        """
        Places a move in the specified column if it's available.

        Args:
            col (int): The column where the move is made.
            letter (str): The player making the move ('X' or 'O').

        Returns:
            bool: True if move was successful, False otherwise.
        """
        if col not in self.available_moves():
            return False

        for row in range(self.rows - 1, -1, -1):  # Start from the bottom row
            if self.board[row][col] == " ":
                self.board[row][col] = letter
                self.last_move = col  # Store the last move made
                if self.winner(row, col, letter):
                    self.current_winner = letter  # Update the winner if a win condition is met
                return True

        return False  # Move not valid

    def winner(self, row, col, letter):
        """
        Checks if the current move results in a win.

        Args:
            row (int): The row where the last move was made.
            col (int): The column where the last move was made.
            letter (str): The player making the move ('X' or 'O').

        Returns:
            bool: True if the player has won, False otherwise.
        """
        def check_direction(delta_row, delta_col):
            """
            Counts the number of matching pieces in a given direction.

            Args:
                delta_row (int): Row increment (positive or negative).
                delta_col (int): Column increment (positive or negative).

            Returns:
                int: The number of connected pieces in the given direction.
            """
            count = 0
            r, c = row, col
            while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == letter:
                count += 1
                r += delta_row
                c += delta_col

            return count

        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal down-right
            (1, -1)  # Diagonal down-left
        ]

        for dr, dc in directions:
            count = check_direction(dr, dc) + check_direction(-dr, -dc) - 1  # Count in both directions
            if count >= 4:  # A win occurs when four pieces are connected
                return True

        return False  # No winning condition met

    def empty_squares(self):
        """Checks if there are any empty squares left on the board."""
        return any(" " in row for row in self.board)

    def num_empty_squares(self):
        """Returns the total number of empty squares left on the board."""
        return sum(row.count(" ") for row in self.board)

    def reset(self):
        """Resets the board to an empty state."""
        self.board = self.make_board()
        self.current_winner = None
        self.last_move = None

    def copy(self):
        """
        Creates a copy of the current game state.

        Returns:
            Connect4: A new instance of the Connect4 game with the same board state.
        """
        new_game = Connect4()
        new_game.board = [row[:] for row in self.board]  # Deep copy of the board
        new_game.current_winner = self.current_winner
        new_game.last_move = self.last_move  # Copy the last move
        return new_game


def play_connect4(game, x_player, o_player, print_game=True, move_times=None, game_moves=None, blocked_wins=None, missed_wins=None):
    """
    Runs a game of Connect 4 between two players.

    Args:
        game (Connect4): An instance of the Connect4 game.
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

    while game.empty_squares():
        start_time = time.time()  # Track move time

        available_moves_before = set(game.available_moves())  # Store available moves

        # Step 1: Identify if there's an immediate winning move available for the current player
        immediate_winning_moves = []
        for move in available_moves_before:
            temp_game = game.copy()
            if temp_game.make_move(move, letter) and temp_game.current_winner == letter:
                immediate_winning_moves.append(move)

        # Step 2: Player makes a move
        col = o_player.get_move(game) if letter == "O" else x_player.get_move(game)

        if game.make_move(col, letter):
            move_time = time.time() - start_time  # Compute move duration
            if move_times is not None:
                move_times.append(move_time)
            if game_moves is not None:
                game_moves.append(col)

            # Step 3: Check if player had an immediate winning move but didn't take it
            if missed_wins is not None:
                if immediate_winning_moves and col not in immediate_winning_moves:
                    missed_wins[letter] += 1  # Player missed an immediate win

            # Step 4: Track blocked winning moves
            if blocked_wins is not None:
                opponent = "O" if letter == "X" else "X"
                for move in available_moves_before:
                    temp_game = game.copy()
                    if temp_game.make_move(move, opponent) and temp_game.current_winner == opponent:
                        temp_game = game.copy()
                        temp_game.make_move(col, letter)
                        if not any(temp_game.make_move(m, opponent) and temp_game.current_winner == opponent
                                   for m in temp_game.available_moves()):
                            blocked_wins[letter] += 1  # Track successful blocks

            if print_game:
                print(f"{letter} makes a move to column {col}")
                game.print_board()
                print()

            # Step 5: Check for a winner
            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter

            # Step 6: Switch turns
            letter = "O" if letter == "X" else "X"

        else:
            print("Invalid move. Try again.")  # Handle invalid moves

    # If the loop exits, the game is a tie
    if print_game:
        print("It's a tie!")
    return "Tie"
