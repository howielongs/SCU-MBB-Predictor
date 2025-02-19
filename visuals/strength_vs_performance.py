from dash import dcc, html
import plotly.express as px
from app.data_loader import df

def strength_vs_performance():
    # Ensure no NaN values for Strength Metrics
    df_filtered = df.dropna(subset=["Bench Press", "Vertical Jump", "BLK"])

    # 🔹 Normalize strength metrics to scale bubble sizes effectively
    min_size, max_size = 20, 100
    df_filtered["Scaled_Bench_Press"] = (
        (df_filtered["Bench Press"] - df_filtered["Bench Press"].min()) /
        (df_filtered["Bench Press"].max() - df_filtered["Bench Press"].min()) * (max_size - min_size)
    ) + min_size
    
    df_filtered["Scaled_Vertical_Jump"] = (
        (df_filtered["Vertical Jump"] - df_filtered["Vertical Jump"].min()) /
        (df_filtered["Vertical Jump"].max() - df_filtered["Vertical Jump"].min()) * (max_size - min_size)
    ) + min_size

    # Scatter Plot: Bench Press vs. Points Per Game
    bench_ppg_fig = px.scatter(
        df_filtered, x="Bench Press", y="PTS/G", size="Scaled_Bench_Press", hover_name="Player",
        title="Bench Press vs. Points Per Game",
        labels={"PTS/G": "Points Per Game", "Bench Press": "Bench Press (Reps)"},
        color_discrete_sequence=["#636EFA"], trendline="ols"
    )

    # Scatter Plot: Vertical Jump vs. Rebounds Per Game
    vert_rpg_fig = px.scatter(
        df_filtered, x="Vertical Jump", y="R/G", size="Scaled_Vertical_Jump", hover_name="Player",
        title="Vertical Jump vs. Rebounds Per Game",
        labels={"R/G": "Rebounds Per Game", "Vertical Jump": "Vertical Jump (inches)"},
        color_discrete_sequence=["#EF553B"], trendline="ols"
    )

    # Scatter Plot: Vertical Jump vs. Steals Per Game
    vert_stl_fig = px.scatter(
        df_filtered, x="Vertical Jump", y="STL", size="Scaled_Vertical_Jump", hover_name="Player",
        title="Vertical Jump vs. Steals Per Game",
        labels={"STL": "Steals Per Game", "Vertical Jump": "Vertical Jump (inches)"},
        color_discrete_sequence=["#19D3F3"], trendline="ols"
    )

    # Scatter Plot: Vertical Jump vs. Blocks Per Game (NEW)
    vert_blk_fig = px.scatter(
        df_filtered, x="Vertical Jump", y="BLK", size="Scaled_Vertical_Jump", hover_name="Player",
        title="Vertical Jump vs. Blocks Per Game",
        labels={"BLK": "Blocks Per Game", "Vertical Jump": "Vertical Jump (inches)"},
        color_discrete_sequence=["#FF6699"], trendline="ols"
    )

    return html.Div([
        html.H3("Strength Metrics vs. In-Game Performance", style={"textAlign": "center", "marginBottom": "10px", "fontWeight": "bold"}),
        html.P("This analysis explores the relationship between player strength (bench press & vertical jump) and key in-game metrics (PPG, RPG, Steals, BPG). "
               "Bubble size represents the strength metric for better visual comparison.",
               style={"textAlign": "center", "fontSize": "16px", "marginBottom": "15px", "maxWidth": "900px", "marginLeft": "auto", "marginRight": "auto"}),

        html.Div([
            dcc.Graph(figure=bench_ppg_fig),
            dcc.Graph(figure=vert_rpg_fig),
            dcc.Graph(figure=vert_stl_fig),
            dcc.Graph(figure=vert_blk_fig),  # New Vertical Jump vs. BPG plot
        ], style={"display": "flex", "flexDirection": "column", "alignItems": "center"})
    ])
