import math
import random
import numpy as np
from copy import deepcopy

class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_move = False
        val = None
        while not valid_move:
            try:
                move = input(f"{self.letter}'s turn. Input move: ")
                val = int(move)
                if val not in game.available_moves():
                    raise ValueError
                valid_move = True
            except ValueError:
                print("Invalid move. Try again.")
        return val

class ab_minimax(Player):
    def __init__(self, letter, max_depth=3):
        """
        Alpha-Beta Pruned Minimax Player.
        
        Args:
            letter (str): The player's letter ('X' or 'O').
            max_depth (int): The maximum search depth for minimax.
        """
        super().__init__(letter)
        self.max_depth = max_depth

    def get_move(self, game):
        """
        Determines the best move using the Alpha-Beta Pruned Minimax algorithm.

        Args:
            game: The game state.

        Returns:
            int: The best column to drop a piece in.
        """
        move_values, _ = self.get_move_values(game)  # Get minimax evaluations
        best_move = max(move_values, key=move_values.get)  # Choose best move

        # Print Minimax move evaluations similar to MCTS
        print("\nMinimax Move Evaluations:")
        for move, value in sorted(move_values.items(), key=lambda x: x[1], reverse=True):
            print(f"Move {move}: Evaluation Score = {value:.3f}")

        return best_move

    def minimax(self, state, player, alpha=-math.inf, beta=math.inf, depth=0, max_depth=4):
        """
        Performs the Minimax algorithm with Alpha-Beta pruning.

        Args:
            state: The current game state.
            player (str): The player making the move ('X' or 'O').
            alpha (float): The best already guaranteed score for maximizer.
            beta (float): The best already guaranteed score for minimizer.
            depth (int): The current depth of the recursive call.
            max_depth (int): The maximum search depth.

        Returns:
            dict: A dictionary with 'position' (best move) and 'score' (evaluation value).
        """
        max_player = self.letter
        other_player = "O" if player == "X" else "X"

        if state.current_winner == other_player:
            return {"position": None, "score": 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}

        if not state.empty_squares():
            return {"position": None, "score": 0}

        if depth == max_depth:
            return {"position": None, "score": self.evaluate_state(state)}

        best = {"position": None, "score": -math.inf if player == max_player else math.inf}

        for col in state.available_moves():
            temp_state = self.simulate_move(state, col, player)
            sim_score = self.minimax(temp_state, other_player, alpha, beta, depth + 1, max_depth)
            sim_score["position"] = col

            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
                alpha = max(alpha, best["score"])
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score
                beta = min(beta, best["score"])

            if beta <= alpha:
                break

        return best

    def simulate_move(self, state, col, player):
        """
        Simulates a move by copying the game state and applying the move.

        Args:
            state: The current game state.
            col (int): The column to drop a piece in.
            player (str): The player making the move.

        Returns:
            The new game state after the move.
        """
        temp_state = state.copy()
        temp_state.make_move(col, player)
        return temp_state

    def evaluate_state(self, state):
        """
        Evaluates the board state.

        Args:
            state: The game state.

        Returns:
            int: The evaluation score.
        """
        if state.current_winner == self.letter:
            return 1
        elif state.current_winner == ("O" if self.letter == "X" else "X"):
            return -1
        return 0

    def get_move_values(self, game):
        """
        Computes evaluation scores for all possible moves.

        Args:
            game: The current game state.

        Returns:
            dict: A dictionary of move evaluations.
        """
        move_values = {}
        for move in game.available_moves():
            temp_game = game.copy()
            temp_game.make_move(move, self.letter)
            move_values[move] = self.minimax(temp_game, self.letter)["score"]

        return move_values, None  # Minimax does not return percentages


# courtesy of the code provided by Hayoung-Kim for making this possible || https://github.com/hayoung-kim/mcts-tic-tac-toe
class MCTSPlayer:
    def __init__(self, letter, n_iterations=1500, depth=15, exploration_constant=20):
        self.letter = letter
        self.n_iterations = n_iterations
        self.depth = depth
        self.exploration_constant = exploration_constant
        self.tree = {}
        self.total_n = 0

    def _initialize_tree(self, game):
        """Initializes the MCTS tree with the root node."""
        root_id = (0,)
        self.tree = {root_id: {'state': game.copy(),
                                'player': self.letter,
                                'child': [],
                                'parent': None,
                                'n': 0,
                                'w': 0,
                                'q': None}}

    def selection(self):
        """Selects the best leaf node based on UCT values."""
        node_id = (0,)
        while self.tree[node_id]['child']:
            max_uct = -np.inf
            best_child = None
            for action in self.tree[node_id]['child']:
                child_id = node_id + (action,)
                w, n = self.tree[child_id]['w'], self.tree[child_id]['n']
                total_n = self.total_n if self.total_n > 0 else 1
                
                uct = (w / (n + 1e-4)) + self.exploration_constant * np.sqrt(np.log(total_n + 1) / (n + 1e-4))

                if uct > max_uct:
                    max_uct = uct
                    best_child = child_id
            
            node_id = best_child
        return node_id

    def expansion(self, leaf_id):
        """Expands the tree by adding all possible child nodes if not already visited."""
        if self.tree[leaf_id]['n'] > 0:  # If already visited, no need to expand
            return leaf_id  

        game = deepcopy(self.tree[leaf_id]['state'])
        possible_moves = game.available_moves()
        
        if not possible_moves:
            return leaf_id  # No valid moves, return the same node

        children = []
        for move in possible_moves:
            child_state = deepcopy(game)
            child_state.make_move(move, self.tree[leaf_id]['player'])
            next_player = 'O' if self.tree[leaf_id]['player'] == 'X' else 'X'

            child_id = leaf_id + (move,)
            self.tree[child_id] = {'state': child_state,
                                'player': next_player,
                                'child': [],
                                'parent': leaf_id,
                                'n': 0, 'w': 0, 'q': 0}
            self.tree[leaf_id]['child'].append(move)
            children.append(child_id)

        return random.choice(children) if children else leaf_id

        
    def simulation(self, node_id):
        """Runs a simulation using weighted rollouts instead of pure randomness."""
        game = deepcopy(self.tree[node_id]['state'])
        player = self.tree[node_id]['player']

        while game.empty_squares():
            possible_moves = game.available_moves()
            move_scores = []

            # Score each move: +100 for win, -100 for loss, 0 otherwise
            for move in possible_moves:
                temp_game = deepcopy(game)
                temp_game.make_move(move, player)
                if temp_game.current_winner == player:
                    return 1 if player == self.letter else -1  # Instant win
                elif temp_game.current_winner:
                    move_scores.append((move, -100))  # Instant loss, bad move
                else:
                    move_scores.append((move, 0))  # Neutral move

            if move_scores:
                best_moves = [m for m, s in move_scores if s == max([s for _, s in move_scores])]
                move = random.choice(best_moves)  # Favor best moves
            else:
                move = random.choice(possible_moves)

            game.make_move(move, player)
            if game.current_winner:
                return 1 if game.current_winner == self.letter else -1

            player = "O" if player == "X" else "X"

        return 0  # Draw



    def backpropagation(self, node_id, result):
        """Backpropagates the result up the tree to properly update values."""
        while node_id is not None:
            self.tree[node_id]['n'] += 1  # Increment visit count
            self.tree[node_id]['w'] += result  # Update win score
            self.tree[node_id]['q'] = self.tree[node_id]['w'] / (self.tree[node_id]['n'] + 1e-4)  # Avoid division by zero
            
            node_id = self.tree[node_id]['parent']
            result *= -1  # Flip result for the opponent


    def get_move_values(self, game):
        """Runs MCTS iterations and returns move evaluations."""
        self._initialize_tree(game)

        for _ in range(self.n_iterations):
            leaf_id = self.selection()
            child_id = self.expansion(leaf_id)
            result = self.simulation(child_id)
            self.backpropagation(child_id, result)

        root_id = (0,)
        move_values = {move: self.tree[root_id + (move,)]['q'] for move in self.tree[root_id]['child']}
        total_visits = sum(self.tree[root_id + (move,)]['n'] for move in self.tree[root_id]['child'])
        move_percentages = {move: (self.tree[root_id + (move,)]['n'] / total_visits) * 100 for move in move_values}

        return move_values, move_percentages

    def get_move(self, game):
        """Selects the best move based on MCTS evaluations."""
        move_values, move_percentages = self.get_move_values(game)
        best_move = max(move_values, key=move_values.get)
        
        print("\nMCTS Move Evaluations:")
        for move, value in sorted(move_values.items(), key=lambda x: x[1], reverse=True):
            print(f"Move {move}: Q-value = {value:.3f}, Selection % = {move_percentages[move]:.2f}%")

        return best_move


''' this code below is the first iteration of MCTS, turned out to be wrong as it had 4 major mistakes:
1. My implementation uses class-based tree representation with nodes. The correct or the second implementation uses an explicit tree structure with selection, expansion, simulation and backpropagation steps. 
2. My implementation had a slightly off selection strategy not purely based off of UCT. Second implementation used UCT purely to select nodes based on exploitation and exploration as it is supposed to 
3. My implementation expanded one child at a time as opposed to expanding nodes by generating all possible children
4. My implementation would perform random rollouts with immediate terminatoin if a winner was found, as opposed to a more correct implementation of a terminal state being found  
5. a slight change with how backpropagation is handled'''
# class MCTSPlayer(Player):
#     def __init__(self, letter, num_rollouts=25000):
#         super().__init__(letter)
#         self.num_rollouts = num_rollouts  
#         self.num_workers = cpu_count()
#         self.transposition_table = {}

#     class Node:
#         def __init__(self, state, parent=None):
#             self.state = state
#             self.parent = parent
#             self.children = []
#             self.visits = 0
#             self.value = 0
#             self.state_hash = hash(str(state.board))

#         def is_fully_expanded(self):
#             return len(self.children) == len(self.state.available_moves())

#         def best_child(self, exploration_weight):
#             if not self.children:
#                 return None  # Return None if no children exist to avoid max() error

#             return max(
#                 self.children,
#                 key=lambda child: child.value / (child.visits + 1e-6) +
#                 exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
#             )

#     def get_move(self, game):
#         # Reset the transposition table at the start of each game
#         self.transposition_table.clear()

#         # Initialize the root node for the new game
#         root = self.Node(game.copy())
#         iterations = 0
        
#         with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
#             for _ in range(self.num_rollouts // self.num_workers):
#                 nodes = [self._select(root) for _ in range(self.num_workers)]
#                 rewards = list(executor.map(self._simulate, [node.state for node in nodes]))
#                 for node, reward in zip(nodes, rewards):
#                     self._backpropagate(node, reward)
#                 iterations += self.num_workers

#         best_child = root.best_child(exploration_weight=0)

#         if best_child is None:
#             print("MCTS could not find a best move. Choosing a random move.")
#             return random.choice(game.available_moves())

#         print(f"MCTS completed {iterations} iterations.")
#         return best_child.state.last_move

#     def _select(self, node):
#         while node.is_fully_expanded() and node.children:
#             node = node.best_child(exploration_weight=1.41 if hasattr(node.state, "cols") else 0.2)
        
#         state_hash = node.state_hash
#         if state_hash in self.transposition_table:
#             return self.transposition_table[state_hash]

#         if not node.is_fully_expanded():
#             new_node = self._expand(node)
#             self.transposition_table[state_hash] = new_node
#             return new_node

#         return node

#     def _expand(self, node):
#         untried_moves = [move for move in node.state.available_moves() 
#                          if move not in [child.state.last_move for child in node.children]]
#         if not untried_moves:
#             return node
        
#         move = random.choice(untried_moves)
#         new_state = node.state.copy()
#         new_state.make_move(move, self.letter)
#         child_node = self.Node(new_state, parent=node)
#         node.children.append(child_node)
#         return child_node

#     def _simulate(self, state):
#         current_state = state.copy()
#         current_player = self.letter

#         while current_state.empty_squares():
#             move = random.choice(current_state.available_moves())
#             current_state.make_move(move, current_player)

#             if current_state.current_winner:
#                 return 1 if current_player == self.letter else -1

#             current_player = "O" if current_player == "X" else "X"

#         return 0  # Draw

#     def _backpropagate(self, node, reward):
#         discount_factor = 0.95  # Encourage more recent moves
#         while node:
#             node.visits += 1
#             node.value += reward
#             reward = -reward * discount_factor
#             node = node.parent
