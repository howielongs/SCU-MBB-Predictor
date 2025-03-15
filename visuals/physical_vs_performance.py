from dash import dcc, html
import plotly.express as px
import pandas as pd

def physical_vs_performance():
    # Manually Define Data
    player_data = [
        {"Player": "AKAMETU, Kosy", "Height": 78, "Weight": 210, "Wingspan": 82, "PTS/G": 4.1, "R/G": 1.3, "BLK/G": 0.0, "A/G": 0.1, "STL/G": 0.0, "3/4 Sprint (s)": 3.15},
        {"Player": "BAL, Adama", "Height": 80, "Weight": 220, "Wingspan": 84, "PTS/G": 14.1, "R/G": 2.6, "BLK/G": 0.14, "A/G": 3.0, "STL/G": 0.47, "3/4 Sprint (s)": 3.20},
        {"Player": "BRYAN, Tyree", "Height": 77, "Weight": 215, "Wingspan": 81, "PTS/G": 10.9, "R/G": 4.4, "BLK/G": 0.45, "A/G": 1.5, "STL/G": 1.1, "3/4 Sprint (s)": 3.10},
        {"Player": "DOUYON, Malachi", "Height": 76, "Weight": 190, "Wingspan": 78, "PTS/G": 0.0, "R/G": 0.0, "BLK/G": 0.0, "A/G": 0.0, "STL/G": 0.0, "3/4 Sprint (s)": 3.25},
        {"Player": "ENSMINGER, Jake", "Height": 79, "Weight": 225, "Wingspan": 83, "PTS/G": 2.3, "R/G": 5.9, "BLK/G": 0.095, "A/G": 2.1, "STL/G": 0.48, "3/4 Sprint (s)": 3.30},
        {"Player": "KNAPPER, Brenton", "Height": 74, "Weight": 185, "Wingspan": 76, "PTS/G": 0.0, "R/G": 0.0, "BLK/G": 0.0, "A/G": 2.8, "STL/G": 0.75, "3/4 Sprint (s)": 3.05},
        {"Player": "MAHI, Elijah", "Height": 78, "Weight": 200, "Wingspan": 81, "PTS/G": 0.0, "R/G": 0.0, "BLK/G": 0.26, "A/G": 0.0, "STL/G": 0.53, "3/4 Sprint (s)": 3.18},
        {"Player": "O'NEIL, Johnny", "Height": 80, "Weight": 225, "Wingspan": 86, "PTS/G": 10.5, "R/G": 5.7, "BLK/G": 0.86, "A/G": 1.2, "STL/G": 0.67, "3/4 Sprint (s)": 3.28},
        {"Player": "OBOYE, Bukky", "Height": 82, "Weight": 235, "Wingspan": 88, "PTS/G": 1.5, "R/G": 2.3, "BLK/G": 0.12, "A/G": 0.0, "STL/G": 0.13, "3/4 Sprint (s)": 3.35},
        {"Player": "STEWART, Carlos", "Height": 73, "Weight": 180, "Wingspan": 75, "PTS/G": 12.0, "R/G": 2.9, "BLK/G": 0.09, "A/G": 2.8, "STL/G": 1.43, "3/4 Sprint (s)": 3.00},
        {"Player": "TILLY, Christoph", "Height": 79, "Weight": 220, "Wingspan": 84, "PTS/G": 8.5, "R/G": 4.0, "BLK/G": 0.85, "A/G": 0.4, "STL/G": 0.85, "3/4 Sprint (s)": 3.27},
        {"Player": "TONGUE, Camaron", "Height": 80, "Weight": 215, "Wingspan": 85, "PTS/G": 5.7, "R/G": 3.8, "BLK/G": 0.38, "A/G": 0.3, "STL/G": 0.43, "3/4 Sprint (s)": 3.23}
    ]

    # Convert to DataFrame
    df = pd.DataFrame(player_data)

    # Calculate Wingspan-to-Height Ratio
    df["Wingspan-to-Height"] = df["Wingspan"] / df["Height"]

    # Normalize weight for bubble size scaling
    min_size, max_size = 20, 100
    df["Scaled_Weight"] = (
        (df["Weight"] - df["Weight"].min()) /
        (df["Weight"].max() - df["Weight"].min()) * (max_size - min_size)
    ) + min_size

    # Invert Sprint Time so **faster players have larger bubbles**
    df["Inverted Sprint"] = 1 / df["3/4 Sprint (s)"]

    # Scatter Plots
    figs = {
        "Height vs. Points Per Game": px.scatter(df, x="Height", y="PTS/G", size="Scaled_Weight", hover_name="Player",
                                                 title="Height vs. Points Per Game", labels={"PTS/G": "Points Per Game", "Height": "Height (inches)"},
                                                 color_discrete_sequence=["#636EFA"], trendline="ols"),
        
        "Height vs. Rebounds Per Game": px.scatter(df, x="Height", y="R/G", size="Scaled_Weight", hover_name="Player",
                                                   title="Height vs. Rebounds Per Game", labels={"R/G": "Rebounds Per Game", "Height": "Height (inches)"},
                                                   color_discrete_sequence=["#EF553B"], trendline="ols"),

        "Height vs. Blocks Per Game": px.scatter(df, x="Height", y="BLK/G", size="Scaled_Weight", hover_name="Player",
                                                 title="Height vs. Blocks Per Game", labels={"BLK/G": "Blocks Per Game", "Height": "Height (inches)"},
                                                 color_discrete_sequence=["#00CC96"], trendline="ols"),

        "Wingspan-to-Height Ratio vs. Points Per Game": px.scatter(df, x="Wingspan-to-Height", y="PTS/G", size="Scaled_Weight", hover_name="Player",
                                                                   title="Wingspan-to-Height Ratio vs. Points Per Game",
                                                                   labels={"PTS/G": "Points Per Game", "Wingspan-to-Height": "Wingspan-to-Height Ratio"},
                                                                   color_discrete_sequence=["#FFA07A"], trendline="ols"),

        "Wingspan-to-Height Ratio vs. Blocks Per Game": px.scatter(df, x="Wingspan-to-Height", y="BLK/G", size="Scaled_Weight", hover_name="Player",
                                                                   title="Wingspan-to-Height Ratio vs. Blocks Per Game",
                                                                   labels={"BLK/G": "Blocks Per Game", "Wingspan-to-Height": "Wingspan-to-Height Ratio"},
                                                                   color_discrete_sequence=["#FFA07A"], trendline="ols"),

        "Wingspan-to-Height Ratio vs. Rebounds Per Game": px.scatter(df, x="Wingspan-to-Height", y="R/G", size="Scaled_Weight", hover_name="Player",
                                                                     title="Wingspan-to-Height Ratio vs. Rebounds Per Game",
                                                                     labels={"R/G": "Rebounds Per Game", "Wingspan-to-Height": "Wingspan-to-Height Ratio"},
                                                                     color_discrete_sequence=["#8A2BE2"], trendline="ols"),
        "3/4 Sprint vs. Points Per Game": px.scatter(df, x="3/4 Sprint (s)", y="PTS/G", size="Inverted Sprint", hover_name="Player",
                                                     title="3/4 Sprint vs. Points Per Game",
                                                     labels={"PTS/G": "Points Per Game", "3/4 Sprint (s)": "3/4 Sprint Time (seconds)"},
                                                     color_discrete_sequence=["#1f77b4"], trendline="ols").update_xaxes(autorange="reversed"),
        
        "3/4 Sprint vs. Assists Per Game": px.scatter(df, x="3/4 Sprint (s)", y="A/G", size="Inverted Sprint", hover_name="Player",
                                                      title="3/4 Sprint vs. Assists Per Game",
                                                      labels={"A/G": "Assists Per Game", "3/4 Sprint (s)": "3/4 Sprint Time (seconds)"},
                                                      color_discrete_sequence=["#ff7f0e"], trendline="ols").update_xaxes(autorange="reversed"),

        "3/4 Sprint vs. Steals Per Game": px.scatter(df, x="3/4 Sprint (s)", y="STL/G", size="Inverted Sprint", hover_name="Player",
                                                     title="3/4 Sprint vs. Steals Per Game",
                                                     labels={"STL/G": "Steals Per Game", "3/4 Sprint (s)": "3/4 Sprint Time (seconds)"},
                                                     color_discrete_sequence=["#2ca02c"], trendline="ols").update_xaxes(autorange="reversed"),
    }

    return html.Div([
        html.H3("Height, Wingspan & Speed vs. Performance", style={"textAlign": "center", "marginBottom": "10px", "fontWeight": "bold"}),
        html.P("This analysis explores the relationship between player height, wingspan, and speed with their scoring (PPG), rebounding (RPG), steals, and shot-blocking (BPG) performance. "
               "Bubble size represents the player's weight for better visualization.",
               style={"textAlign": "center", "fontSize": "16px", "marginBottom": "15px", "maxWidth": "900px", "marginLeft": "auto", "marginRight": "auto"}),

        html.Div([dcc.Graph(figure=fig) for fig in figs.values()], 
                 style={"display": "flex", "flexDirection": "column", "alignItems": "center"})
    ])
