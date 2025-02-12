import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

def create_kpi_cards(team_stats):
    """Generates KPI cards for team stats."""
    return html.Div([
        html.Div([
            html.H4(metric, style={"textAlign": "center", "marginBottom": "8px", "fontSize": "18px"}),
            html.P(value, style={"fontSize": "26px", "fontWeight": "bold", "textAlign": "center"})
        ], className="kpi-card") for metric, value in team_stats.items()
    ], className="kpi-container", style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "25px", "padding": "35px"})

def player_points_distribution(df):
    """Creates a horizontal bar chart for player points distribution."""
    return dcc.Graph(
        id="points_distribution",
        figure=px.bar(
            df, x="PTS/G", y="Player", title="Player Points Distribution", orientation="h", color_discrete_sequence=["#636EFA"]
        ).update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Points Per Game",
            yaxis_title="Players",
            yaxis=dict(autorange="reversed"),
            margin=dict(l=150, r=40, t=50, b=50),
            xaxis=dict(gridcolor='rgba(200,200,200,0.3)')
        )
    )
