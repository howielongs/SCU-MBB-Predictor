from dash import dcc, html
import plotly.express as px
import pandas as pd

def strength_vs_performance():
    # Manually Define Data
    player_data = [
        {"Player": "AKAMETU, Kosy", "Bench Press": 10, "Vertical Jump": 30, "PTS/G": 4.1, "R/G": 1.3, "BLK/G": 0.0, "STL/G": 0.0},
        {"Player": "BAL, Adama", "Bench Press": 12, "Vertical Jump": 32, "PTS/G": 14.1, "R/G": 2.6, "BLK/G": 0.14, "STL/G": 0.48},
        {"Player": "BRYAN, Tyree", "Bench Press": 8, "Vertical Jump": 28, "PTS/G": 10.9, "R/G": 4.4, "BLK/G": 0.45, "STL/G": 1.1},
        {"Player": "DOUYON, Malachi", "Bench Press": 9, "Vertical Jump": 29, "PTS/G": 0.0, "R/G": 0.0, "BLK/G": 0.0, "STL/G": 0.0},
        {"Player": "ENSMINGER, Jake", "Bench Press": 11, "Vertical Jump": 31, "PTS/G": 2.3, "R/G": 5.9, "BLK/G": 0.095, "STL/G": 0.48},
        {"Player": "KNAPPER, Brenton", "Bench Press": 7, "Vertical Jump": 26, "PTS/G": 0.0, "R/G": 0.0, "BLK/G": 0.0, "STL/G": 0.75},
        {"Player": "MAHI, Elijah", "Bench Press": 13, "Vertical Jump": 33, "PTS/G": 0.0, "R/G": 0.0, "BLK/G": 0.26, "STL/G": 0.53},
        {"Player": "O'NEIL, Johnny", "Bench Press": 10, "Vertical Jump": 30, "PTS/G": 10.5, "R/G": 5.7, "BLK/G": 0.86, "STL/G": 0.67},
        {"Player": "OBOYE, Bukky", "Bench Press": 15, "Vertical Jump": 36, "PTS/G": 1.5, "R/G": 2.3, "BLK/G": 0.12, "STL/G": 0.12},
        {"Player": "STEWART, Carlos", "Bench Press": 6, "Vertical Jump": 25, "PTS/G": 12.0, "R/G": 2.9, "BLK/G": 0.09, "STL/G": 1.43},
        {"Player": "TILLY, Christoph", "Bench Press": 12, "Vertical Jump": 32, "PTS/G": 8.5, "R/G": 4.0, "BLK/G": 0.85, "STL/G": 0.85},
        {"Player": "TONGUE, Camaron", "Bench Press": 9, "Vertical Jump": 29, "PTS/G": 5.7, "R/G": 3.8, "BLK/G": 0.38, "STL/G": 0.43}
    ]

    # Convert to DataFrame
    df = pd.DataFrame(player_data)

    # Normalize strength metrics for bubble size
    min_size, max_size = 20, 100
    df["Scaled_Bench_Press"] = (
        (df["Bench Press"] - df["Bench Press"].min()) /
        (df["Bench Press"].max() - df["Bench Press"].min()) * (max_size - min_size)
    ) + min_size
    
    df["Scaled_Vertical_Jump"] = (
        (df["Vertical Jump"] - df["Vertical Jump"].min()) /
        (df["Vertical Jump"].max() - df["Vertical Jump"].min()) * (max_size - min_size)
    ) + min_size

    # Scatter Plots
    figs = {
        "Bench Press vs. Points Per Game": px.scatter(df, x="Bench Press", y="PTS/G", size="Scaled_Bench_Press", hover_name="Player",
                                                      title="Bench Press vs. Points Per Game", labels={"PTS/G": "Points Per Game", "Bench Press": "Bench Press (Reps)"},
                                                      color_discrete_sequence=["#636EFA"], trendline="ols"),
        
        "Vertical Jump vs. Rebounds Per Game": px.scatter(df, x="Vertical Jump", y="R/G", size="Scaled_Vertical_Jump", hover_name="Player",
                                                          title="Vertical Jump vs. Rebounds Per Game", labels={"R/G": "Rebounds Per Game", "Vertical Jump": "Vertical Jump (inches)"},
                                                          color_discrete_sequence=["#EF553B"], trendline="ols"),

        "Vertical Jump vs. Blocks Per Game": px.scatter(df, x="Vertical Jump", y="BLK/G", size="Scaled_Vertical_Jump", hover_name="Player",
                                                        title="Vertical Jump vs. Blocks Per Game", labels={"BLK/G": "Blocks Per Game", "Vertical Jump": "Vertical Jump (inches)"},
                                                        color_discrete_sequence=["#FF6699"], trendline="ols"),

        "Vertical Jump vs. Steals Per Game": px.scatter(df, x="Vertical Jump", y="STL/G", size="Scaled_Vertical_Jump", hover_name="Player",
                                                        title="Vertical Jump vs. Steals Per Game", labels={"STL/G": "Steals Per Game", "Vertical Jump": "Vertical Jump (inches)"},
                                                        color_discrete_sequence=["#19D3F3"], trendline="ols"),
    }

    return html.Div([
        html.H3("Strength Metrics vs. In-Game Performance", style={"textAlign": "center", "marginBottom": "10px", "fontWeight": "bold"}),
        html.P("This analysis explores the relationship between player strength (bench press & vertical jump) and key in-game metrics (PPG, RPG, Steals, BPG). "
               "Bubble size represents the strength metric for better visual comparison.",
               style={"textAlign": "center", "fontSize": "16px", "marginBottom": "15px", "maxWidth": "900px", "marginLeft": "auto", "marginRight": "auto"}),

        html.Div([dcc.Graph(figure=fig) for fig in figs.values()], 
                 style={"display": "flex", "flexDirection": "column", "alignItems": "center"})
    ])
