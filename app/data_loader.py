import os
import pandas as pd

def load_data(file_name):
    """Loads a CSV file from the data directory."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(BASE_DIR, "data", file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)

# Load main dataset
df = load_data("santa_clara_basketball_stats2.csv")

# Compute Team Averages
team_stats = {
    "Points Per Game": round(df["PTS/G"].mean(), 1),
    "Field Goal %": round(df["FG%"].mean() * 100, 1),
    "3-Point %": round(df["3FG%"].mean() * 100, 1),
    "Free Throw %": round(df["FT%"].mean() * 100, 1),
    "Rebounds Per Game": round(df["R/G"].mean(), 1),
    "Assists Per Game": round(df["A/G"].mean(), 1),
    "Steals Per Game": round(df["STL"].mean(), 1),
    "Blocks Per Game": round(df["BLK"].mean(), 1),
}
