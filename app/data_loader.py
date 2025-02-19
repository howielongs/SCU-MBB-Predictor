import os
import pandas as pd

def load_data(file_name):
    """Loads a CSV file from the data directory."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(BASE_DIR, "data", file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = ["Player", "PTS/G", "FG%", "3FG%", "FT%", "R/G", "A/G", "STL", "BLK", "Position"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # 🔹 Manually Define Height & Weight if Missing
    height_weight_mapping = {
        "AKAMETU, Kosy": (78, 210),  # (Height in inches, Weight in lbs)
        "BAL, Adama": (80, 220),
        "BRYAN, Tyree": (77, 215),
        "DOUYON, Malachi": (76, 190),
        "ENSMINGER, Jake": (79, 225),
        "KNAPPER, Brenton": (74, 185),
        "MAHI, Elijah": (78, 200),
        "MCELDON, Luke": (81, 230),
        "O'NEIL, Johnny": (80, 225),
        "OBOYE, Bukky": (82, 235),
        "STEWART, Carlos": (73, 180),
        "TILLY, Christoph": (79, 220),
        "TONGUE, Camaron": (80, 215),
        "YARUSSO, Brendan": (75, 195)
    }

    # Add Height & Weight columns if missing
    if "Height" not in df.columns or "Weight" not in df.columns:
        df["Height"] = df["Player"].map(lambda player: height_weight_mapping.get(player, (None, None))[0])
        df["Weight"] = df["Player"].map(lambda player: height_weight_mapping.get(player, (None, None))[1])

    # Fill missing height and weight values with column averages
    df["Height"] = df["Height"].fillna(df["Height"].mean())
    df["Weight"] = df["Weight"].fillna(df["Weight"].mean())

    # 🔹 Manually Define Strength Metrics if Missing
    strength_mapping = {
        "AKAMETU, Kosy": (10, 30),  # (Bench Press reps, Vertical Jump inches)
        "BAL, Adama": (12, 32),
        "BRYAN, Tyree": (8, 28),
        "DOUYON, Malachi": (9, 29),
        "ENSMINGER, Jake": (11, 31),
        "KNAPPER, Brenton": (7, 26),
        "MAHI, Elijah": (13, 33),
        "MCELDON, Luke": (14, 35),
        "O'NEIL, Johnny": (10, 30),
        "OBOYE, Bukky": (15, 36),
        "STEWART, Carlos": (6, 25),
        "TILLY, Christoph": (12, 32),
        "TONGUE, Camaron": (9, 29),
        "YARUSSO, Brendan": (8, 28)
    }

    # Add Bench Press & Vertical Jump columns if missing
    if "Bench Press" not in df.columns or "Vertical Jump" not in df.columns:
        df["Bench Press"] = df["Player"].map(lambda player: strength_mapping.get(player, (None, None))[0])
        df["Vertical Jump"] = df["Player"].map(lambda player: strength_mapping.get(player, (None, None))[1])

    # Fill missing strength metrics with column averages
    df["Bench Press"] = df["Bench Press"].fillna(df["Bench Press"].mean())
    df["Vertical Jump"] = df["Vertical Jump"].fillna(df["Vertical Jump"].mean())

    return df

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
