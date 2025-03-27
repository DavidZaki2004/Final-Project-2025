import pandas as pd
import numpy as np

def compute_confidence_intervals(df):
    z_value = 1.96  # 95% confidence interval
    
    # Compute CIs for move times (weighted mean CI)
    move_time_stats = {}
    for col in ["Average X Move Time (s)", "Average O Move Time (s)"]:
        if col in df.columns and not df[col].isna().all():
            mean = df[col].mean()
            std = df[col].std()
            n = df.shape[0]
            ci = z_value * (std / np.sqrt(n))
            # Convert CI to percentage format
            move_time_stats[col] = (
                round((mean - ci) * 100, 2), 
                round((mean + ci) * 100, 2)
            )
    
    # Compute CIs for win/draw proportions (proportion CI)
    prop_stats = {}
    for col in ["X Wins", "O Wins", "Ties"]:
        if col in df.columns and not df[col].isna().all():
            p_hat = df[col].sum() / (df[["X Wins", "O Wins", "Ties"]].sum().sum())
            n = df.shape[0]
            ci = z_value * np.sqrt((p_hat * (1 - p_hat)) / n)
            # Convert CI to percentage format
            prop_stats[col] = (
                round((p_hat - ci) * 100, 2), 
                round((p_hat + ci) * 100, 2)
            )
    
    return move_time_stats, prop_stats

def analyze_results(filters=None, sort_by="Win Ratio (X)"):
    """
    Analyzes game results with optional filters and sorting.

    Parameters:
    - filters (dict): A dictionary where keys are column names and values are the filtering values.
                      Example: {"X Iterations": 1500, "O Depth": 10}
    - sort_by (str): Column name to sort the results by.

    Returns:
    - Tuple containing (basic_stats, advanced_stats, difficulty_stats, move_time_ci, prop_ci)
    """
    try:
        df = pd.read_csv("game_results.csv")
    except FileNotFoundError:
        print("Error: game_results.csv not found.")
        return None
    
    if df.empty:
        print("Error: game_results.csv is empty.")
        return None
    
    # Apply multiple filters
    if filters:
        for column, value in filters.items():
            if column not in df.columns:
                print(f"Error: Column '{column}' not found in data.")
                return None
            df = df[df[column] == value]
    
    if df.empty:
        print("No data available after filtering.")
        return None
    
    # Group by matchup for basic game statistics
    basic_stats = df.groupby("Matchup").agg({
        "X Wins": "sum",
        "O Wins": "sum",
        "Ties": "sum",
        "Total Moves": "mean",
        "Average X Move Time (s)": "mean",
        "Average O Move Time (s)": "mean"
    })
    
    # Compute win/loss/draw ratios
    total_games = basic_stats["X Wins"] + basic_stats["O Wins"] + basic_stats["Ties"]
    basic_stats["Win Ratio (X)"] = basic_stats["X Wins"] / total_games
    basic_stats["Win Ratio (O)"] = basic_stats["O Wins"] / total_games
    basic_stats["Draw Ratio"] = basic_stats["Ties"] / total_games
    
    if sort_by in basic_stats.columns:
        basic_stats = basic_stats.sort_values(by=sort_by, ascending=False)
    
    # Group by matchup for advanced statistics
    advanced_stats = df.groupby("Matchup").agg({
        "Blocked Wins (X)": "sum",
        "Blocked Wins (O)": "sum",
        "Missed Wins (X)": "sum",
        "Missed Wins (O)": "sum"
    }).dropna(axis=1, how='all')
    
    # Group by matchup for player difficulty settings
    difficulty_stats = df.groupby("Matchup").agg({
        "X Depth": "first",
        "O Depth": "first",
        "X Iterations": "first",
        "O Iterations": "first",
        "X Exploration Constant": "first",
        "O Exploration Constant": "first"
    }).dropna(axis=1, how='all')
    
    # Compute confidence intervals
    move_time_ci, prop_ci = compute_confidence_intervals(df)
    
    print("\nBasic Game Statistics:\n")
    print(basic_stats.to_string())
    
    print("\nAdvanced Game Statistics:\n")
    print(advanced_stats.to_string())
    
    print("\nDifficulty Settings:\n")
    print(difficulty_stats.to_string())
    
    print("\nConfidence Intervals (as percentages):\n")
    print("Move Time CI (X):", move_time_ci.get("Average X Move Time (s)", "N/A"))
    print("Move Time CI (O):", move_time_ci.get("Average O Move Time (s)", "N/A"))
    print("X Wins CI:", prop_ci.get("X Wins", "N/A"))
    print("O Wins CI:", prop_ci.get("O Wins", "N/A"))
    print("Ties CI:", prop_ci.get("Ties", "N/A"))
    
    return basic_stats, advanced_stats, difficulty_stats, move_time_ci, prop_ci


if __name__ == "__main__":

    # print("\nFiltered by X Iterations = 3000 and O Depth = 2:")
    # analyze_results(filters={"X Iterations": 1500, "O Depth": 3})


    analyze_results(filters={"O Iterations": 2000, "X Depth": 4})



