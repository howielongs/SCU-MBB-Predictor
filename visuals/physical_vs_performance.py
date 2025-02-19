from dash import dcc, html
import plotly.express as px
from app.data_loader import df

def physical_vs_performance():
    # Ensure no NaN values for Height, Weight, and Blocks Per Game
    df_filtered = df.dropna(subset=["Height", "Weight", "BLK"])

    # 🔹 Normalize weight to scale bubble sizes effectively
    min_size, max_size = 20, 100
    df_filtered["Scaled_Weight"] = (
        (df_filtered["Weight"] - df_filtered["Weight"].min()) /
        (df_filtered["Weight"].max() - df_filtered["Weight"].min()) * (max_size - min_size)
    ) + min_size

    # Scatter Plot: Height vs. Points Per Game
    height_ppg_fig = px.scatter(
        df_filtered, x="Height", y="PTS/G", size="Scaled_Weight", hover_name="Player",
        title="Height vs. Points Per Game",
        labels={"PTS/G": "Points Per Game", "Height": "Height (inches)"},
        color_discrete_sequence=["#636EFA"], trendline="ols"
    )

    # Scatter Plot: Height vs. Rebounds Per Game
    height_reb_fig = px.scatter(
        df_filtered, x="Height", y="R/G", size="Scaled_Weight", hover_name="Player",
        title="Height vs. Rebounds Per Game",
        labels={"R/G": "Rebounds Per Game", "Height": "Height (inches)"},
        color_discrete_sequence=["#EF553B"], trendline="ols"
    )

    # Scatter Plot: Height vs. Blocks Per Game (NEW)
    height_blk_fig = px.scatter(
        df_filtered, x="Height", y="BLK", size="Scaled_Weight", hover_name="Player",
        title="Height vs. Blocks Per Game",
        labels={"BLK": "Blocks Per Game", "Height": "Height (inches)"},
        color_discrete_sequence=["#00CC96"], trendline="ols"
    )

    return html.Div([
        html.H3("Height & Weight vs. Performance", style={"textAlign": "center", "marginBottom": "10px", "fontWeight": "bold"}),
        html.P("This analysis explores the relationship between player height and weight with their scoring (PPG), rebounding (RPG), and shot-blocking (BPG) performance. "
               "The size of each point represents the player's weight, scaled for better visibility.",
               style={"textAlign": "center", "fontSize": "16px", "marginBottom": "15px", "maxWidth": "900px", "marginLeft": "auto", "marginRight": "auto"}),

        html.Div([
            dcc.Graph(figure=height_ppg_fig),
            dcc.Graph(figure=height_reb_fig),
            dcc.Graph(figure=height_blk_fig),  # New Height vs. BPG plot
        ], style={"display": "flex", "flexDirection": "column", "alignItems": "center"})
    ])
