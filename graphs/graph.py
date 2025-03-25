from graphviz import Digraph

def create_compact_ab_minimax_flowchart():
    """
    Creates a compact flowchart for the Alpha-Beta Pruned Minimax algorithm.

    The flowchart represents the decision-making process in the minimax algorithm,
    showing the recursive evaluation of nodes, alpha-beta pruning, and return values.

    Returns:
        Digraph: A Graphviz Digraph object representing the flowchart.
    """
    dot = Digraph("Alpha-Beta Minimax", format="png")
    dot.attr(rankdir="TB", nodesep="0.15", ranksep="0.25")  # Set graph direction and spacing

    # Start node
    dot.node("start", "Start Minimax (node, depth, α, β, maximizingPlayer)", shape="ellipse")

    # Base case: Check if we reached a leaf node or max depth
    dot.node("base_check", "Depth = 0 or terminal state? (Leaf node condition)", shape="diamond")
    dot.node("return_heuristic", "Return heuristic value", shape="parallelogram")

    # Maximizing Player Process
    dot.node("max_turn", "Maximizing Player\nmaxEval = -∞", shape="box")
    dot.node("max_loop", "For each child:\nMinimax(child, depth-1, α, β, False)", shape="box")
    dot.node("max_update", "maxEval = max(maxEval, eval)\nα = max(α, eval)", shape="box")
    dot.node("max_prune", "β ≤ α if yes pruning occurs", shape="diamond")

    # Minimizing Player Process
    dot.node("min_turn", "Minimizing Player\nminEval = +∞", shape="box")
    dot.node("min_loop", "For each child:\nMinimax(child, depth-1, α, β, True)", shape="box")
    dot.node("min_update", "minEval = min(minEval, eval)\nβ = min(β, eval)", shape="box")
    dot.node("min_prune", "β ≤ α if yes pruning occurs", shape="diamond")

    # End recursion
    dot.node("return_eval", "Return best evaluation (maxEval or minEval) based on strategy", shape="parallelogram")

    # Define edges for the flowchart
    dot.edge("start", "base_check")
    dot.edge("base_check", "return_heuristic", label="Yes")  # If at leaf node, return heuristic
    dot.edge("base_check", "max_turn", label="No, Maximizing")  # Continue to maximizing branch
    dot.edge("base_check", "min_turn", label="No, Minimizing")  # Continue to minimizing branch

    # Maximizing Player Flow
    dot.edge("max_turn", "max_loop")
    dot.edge("max_loop", "max_update")
    dot.edge("max_update", "max_prune")
    dot.edge("max_prune", "return_eval", label="Yes (Prune)")  # Pruning occurs
    dot.edge("max_prune", "max_loop", label="No (Continue)")  # Continue looping through children

    # Minimizing Player Flow
    dot.edge("min_turn", "min_loop")
    dot.edge("min_loop", "min_update")
    dot.edge("min_update", "min_prune")
    dot.edge("min_prune", "return_eval", label="Yes (Prune)")  # Pruning occurs
    dot.edge("min_prune", "min_loop", label="No (Continue)")  # Continue looping through children

    # End of recursion - return evaluation up the tree
    dot.edge("return_eval", "start", label="Recursive return to parent node")

    return dot

# Generate and render the flowchart
dot = create_compact_ab_minimax_flowchart()
dot.render("compact_alpha_beta_minimax", view=True)
