from dash import dcc, html
import plotly.express as px
from app.data_loader import df

def points_distribution():
    # Compute individual points from 3PT, 2PT, and FT
    df["Points_3PT"] = df["3FG%"] * df["PTS/G"]  # Approximate points from 3s
    df["Points_FT"] = (df["FG%"] - df["3FG%"]) * df["PTS/G"]  # Approximate points from 2s
    df["Points_2PT"] = df["FT%"] * df["PTS/G"]  # Approximate points from FT

    df_melted = df.melt(id_vars=["Player"], value_vars=["Points_3PT", "Points_2PT", "Points_FT"], var_name="Point Type", value_name="Points")

    fig = px.bar(
        df_melted,
        x="Player",
        y="Points",
        color="Point Type",
        title="Points Distribution Breakdown",
        labels={"Points": "Total Points"},
        barmode="stack",
    )

    fig.update_layout(
        xaxis_title="Players",
        yaxis_title="Total Points",
        xaxis=dict(tickangle=-45),
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return html.Div([dcc.Graph(figure=fig)])
