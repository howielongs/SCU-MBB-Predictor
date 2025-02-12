from dash import dcc, html
import plotly.express as px
from data_loader import df, team_stats
from visuals.scoring_analysis import scoring_performance
from visuals.shooting_efficiency import shooting_efficiency
from visuals.points_distribution import points_distribution


# Position Filter (Dropdown)
position_filter = html.Div([
    html.Label("Filter by Position:", style={"fontSize": "18px", "fontWeight": "bold", "display": "block", "textAlign": "center", "marginBottom": "5px"}),
    dcc.Dropdown(
        id="position_dropdown",
        options=[{"label": pos, "value": pos} for pos in df["Position"].unique()],
        value=df["Position"].unique()[0],  # Default to first position
        clearable=False,  # Prevent users from clearing the selection
        searchable=False,  # Removes text input box
        style={"width": "40%", "margin": "auto", "borderRadius": "5px"}
    )
], style={"textAlign": "center", "marginBottom": "20px"})

# PPG Filter (Slider)
ppg_filter = html.Div([
    html.Label("Filter by Max Points Per Game:", style={"fontSize": "18px", "fontWeight": "bold", "display": "block", "textAlign": "center", "marginBottom": "5px"}),
    dcc.Slider(
        id="ppg_slider",
        min=df["PTS/G"].min(),
        max=df["PTS/G"].max(),
        step=1,
        value=df["PTS/G"].max(),
        marks={int(ppg): str(int(ppg)) for ppg in range(int(df["PTS/G"].min()), int(df["PTS/G"].max()) + 1, 5)},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Div(id="ppg_value", style={"textAlign": "center", "fontSize": "16px", "marginTop": "10px"})  # Shows selected value
], style={"marginBottom": "20px"})

# KPI Cards
kpi_cards = html.Div([
    html.Div([
        html.H4(metric, style={"textAlign": "center", "marginBottom": "8px", "fontSize": "18px"}),
        html.P(value, style={"fontSize": "26px", "fontWeight": "bold", "textAlign": "center"})
    ], className="kpi-card") for metric, value in team_stats.items()
], className="kpi-container", style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "25px", "padding": "35px"})

# Player Points Distribution Bar Chart
points_distribution = dcc.Graph(id="points_distribution")

# Tabs for Player Performance Analysis
performance_tabs = dcc.Tabs(id="performance-tabs", value="scoring", children=[
    dcc.Tab(label="Scoring Performance", value="scoring"),
    dcc.Tab(label="Shooting Efficiency", value="shooting"),
    dcc.Tab(label="Points Distribution", value="points"),
])

performance_content = html.Div(id="performance-content")

# Final Layout
layout = html.Div([
    html.H1("SCU Men's Basketball Overview Dashboard", style={"textAlign": "center", "fontSize": "38px", "marginBottom": "35px", "fontWeight": "bold"}),
    
    position_filter,  # Position Filter
    ppg_filter,  # PPG Slider
    
    kpi_cards,  # KPI Stats
    
    html.Div([points_distribution], style={"padding": "35px"}),  # Points Distribution
    
    html.Hr(),  # Divider
    
    html.H2("Player Performance Analysis", style={"textAlign": "center", "marginBottom": "20px"}),  
    performance_tabs,  # Tabs for Player Analysis
    performance_content  # Content for each tab
])
