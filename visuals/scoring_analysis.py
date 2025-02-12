from dash import dcc, html
import plotly.express as px
from app.data_loader import df

def scoring_performance():
    # Define color coding for efficiency (FG% over 50% = Green)
    df["Efficiency"] = df["FG%"].apply(lambda x: "High Efficiency" if x > 0.50 else "Low Efficiency")

    fig = px.bar(
        df,
        x="Player",
        y="PTS/G",
        color="Efficiency",
        title="Scoring Performance (PPG vs Efficiency)",
        labels={"PTS/G": "Points Per Game", "Player": "Players"},
        color_discrete_map={"High Efficiency": "green", "Low Efficiency": "red"},
    )

    fig.update_layout(
        xaxis_title="Players",
        yaxis_title="Points Per Game",
        xaxis=dict(tickangle=-45),
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return html.Div([dcc.Graph(figure=fig)])
