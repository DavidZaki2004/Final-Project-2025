import pandas as pd
from player import HumanPlayer, ab_minimax, MCTSPlayer
from connect4 import Connect4, play_connect4
from tictactoe import TicTacToe, play_tictactoe

def update_results(game_type, x_player, o_player, result, move_times, game_moves, blocked_wins, missed_wins):
    """
    Updates the game results and appends them to a CSV file.

    Args:
        game_type (str): The type of game played (Tic-Tac-Toe or Connect 4).
        x_player (Player): The player using 'X'.
        o_player (Player): The player using 'O'.
        result (str): The game result ('X', 'O', or 'Tie').
        move_times (list): List of time taken per move.
        game_moves (list): List of moves made during the game.
        blocked_wins (dict): Dictionary tracking blocked wins for each player.
        missed_wins (dict): Dictionary tracking missed winning moves.

    Saves:
        Appends the results to "game_results.csv".
    """
    matchup = f"{type(x_player).__name__} vs {type(o_player).__name__}"
    total_moves = len(game_moves)

    # Split move times between X and O
    x_move_times = [move_times[i] for i in range(0, len(move_times), 2)]
    o_move_times = [move_times[i] for i in range(1, len(move_times), 2)]

    # Compute average move times
    avg_x_time = sum(x_move_times) / len(x_move_times) if x_move_times else 0
    avg_o_time = sum(o_move_times) / len(o_move_times) if o_move_times else 0

    # Extract additional attributes for AI players
    x_depth = getattr(x_player, 'minimax', lambda *args, **kwargs: {}).__defaults__[3] if hasattr(x_player, 'minimax') else None
    o_depth = getattr(o_player, 'minimax', lambda *args, **kwargs: {}).__defaults__[3] if hasattr(o_player, 'minimax') else None
    x_iterations = getattr(x_player, 'n_iterations', None)
    o_iterations = getattr(o_player, 'n_iterations', None)
    x_exploration = getattr(x_player, 'exploration_constant', None)
    o_exploration = getattr(o_player, 'exploration_constant', None)

    # Store the data in a dictionary
    data = {
        "Game Type": game_type,
        "Matchup": matchup,
        "X Wins": 1 if result == "X" else 0,
        "O Wins": 1 if result == "O" else 0,
        "Ties": 1 if result == "Tie" else 0,
        "Average X Move Time (s)": avg_x_time,
        "Average O Move Time (s)": avg_o_time,
        "Total Moves": total_moves,
        "Blocked Wins (X)": blocked_wins.get("X", 0),
        "Blocked Wins (O)": blocked_wins.get("O", 0),
        "Missed Wins (X)": missed_wins.get("X", 0),
        "Missed Wins (O)": missed_wins.get("O", 0),
        "X Depth": x_depth,
        "O Depth": o_depth,
        "X Iterations": x_iterations,
        "O Iterations": o_iterations,
        "X Exploration Constant": x_exploration,
        "O Exploration Constant": o_exploration,
    }

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame([data])

    # Attempt to append results to an existing CSV file, or create one if it doesn't exist
    try:
        existing_df = pd.read_csv("game_results.csv")
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv("game_results.csv", index=False)
    print("Game results updated in CSV file.")


def run_tictactoe(game, x_player, o_player, print_game=True):
    """
    Runs a single game of Tic-Tac-Toe and logs results.

    Args:
        game (TicTacToe): An instance of the TicTacToe game.
        x_player (Player): The player using 'X'.
        o_player (Player): The player using 'O'.
        print_game (bool): Whether to display game progress.

    Returns:
        str: The game result ('X', 'O', or 'Tie').
    """
    blocked_wins = {"X": 0, "O": 0}
    missed_wins = {"X": 0, "O": 0}
    move_times = []
    game_moves = []
    
    result = play_tictactoe(game, x_player, o_player, print_game, move_times, game_moves, blocked_wins, missed_wins)
    update_results("TicTacToe", x_player, o_player, result, move_times, game_moves, blocked_wins, missed_wins)
    return result


def run_connect4(game, x_player, o_player, print_game=True):
    """
    Runs a single game of Connect 4 and logs results.

    Args:
        game (Connect4): An instance of the Connect4 game.
        x_player (Player): The player using 'X'.
        o_player (Player): The player using 'O'.
        print_game (bool): Whether to display game progress.

    Returns:
        str: The game result ('X', 'O', or 'Tie').
    """
    blocked_wins = {"X": 0, "O": 0}
    missed_wins = {"X": 0, "O": 0}
    move_times = []
    game_moves = []

    result = play_connect4(game, x_player, o_player, print_game, move_times, game_moves, blocked_wins, missed_wins)
    update_results("Connect4", x_player, o_player, result, move_times, game_moves, blocked_wins, missed_wins)
    return result


def choose_game():
    """Prompts the user to select between Tic-Tac-Toe and Connect 4."""
    print("\nChoose a game to play:")
    print("1. Tic Tac Toe")
    print("2. Connect 4")
    choice = input("\nEnter your choice (1 or 2): ")
    while choice not in ["1", "2"]:
        print("Invalid choice. Please select 1 or 2.")
        choice = input("Enter your choice (1 or 2): ")
    return int(choice)


def choose_player(player_number, game_type):
    """
    Prompts the user to select a player type.

    Args:
        player_number (int): Player number (1 or 2).
        game_type (str): The selected game type.

    Returns:
        Player: An instance of the selected player class.
    """
    print(f"\nChoose Player {player_number} for {game_type}:")
    print("1. Human Player")
    print("2. A-B Minimax ")
    print("3. Monte-Carlo Tree Search")
    choice = input("\nEnter your choice (1, 2, 3): ")
    while choice not in ["1", "2", "3"]:
        print("Invalid choice. Please select 1, 2, or 3.")
        choice = input("Enter your choice (1, 2, 3): ")
    if choice == "1":
        return HumanPlayer('X' if player_number == 1 else 'O')
    elif choice == "2":
        return ab_minimax('X' if player_number == 1 else 'O')
    elif choice == "3":
        return MCTSPlayer('X' if player_number == 1 else 'O')


def run_experiment():
    """Runs multiple automated games for statistical analysis."""
    print(f"\nWelcome to the Experiment Mode!")
    game_choice = choose_game()
    game_type = "Tic Tac Toe" if game_choice == 1 else "Connect 4"
    x_player = choose_player(1, game_type)
    o_player = choose_player(2, game_type)
    num_games = int(input("Enter the number of games to run: "))

    print(f"Running {num_games} games of {game_type} with {type(x_player).__name__} vs {type(o_player).__name__}...")
    for i in range(num_games):
        print(f"\nGame {i + 1} / {num_games}...")
        game = TicTacToe() if game_choice == 1 else Connect4()
        run_tictactoe(game, x_player, o_player, False) if game_choice == 1 else run_connect4(game, x_player, o_player, False)
    
    print(f"\nExperiment Complete! Results logged in game_results.csv")


if __name__ == "__main__":
    """Main program loop for playing games."""
    print("Welcome to the Game Hub!")
    while True:
        print("\n1. Play a single game")
        print("2. Run an experiment (multiple games)")
        mode = input("\nChoose an option (1 or 2): ")
        if mode == "1":
            game_choice = choose_game()
            game = TicTacToe() if game_choice == 1 else Connect4()
            x_player = choose_player(1, "Tic Tac Toe" if game_choice == 1 else "Connect 4")
            o_player = choose_player(2, "Tic Tac Toe" if game_choice == 1 else "Connect 4")
            result = run_tictactoe(game, x_player, o_player, True) if game_choice == 1 else run_connect4(game, x_player, o_player, True)
            print(f"\nGame Over! Result: {result}")
        elif mode == "2":
            run_experiment()
        if input("Play again? (yes/no): ").strip().lower() != "yes":
            print("Thanks for playing!")
            break
