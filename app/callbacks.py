from dash.dependencies import Input, Output
import plotly.express as px
from data_loader import df
from visuals.scoring_analysis import scoring_performance
from visuals.shooting_efficiency import shooting_efficiency
from visuals.points_distribution import points_distribution

def register_callbacks(app):
    # ✅ Callback: Update Player Points Distribution Based on Position & PPG Filters
    @app.callback(
        Output("points_distribution", "figure"),
        Input("position_dropdown", "value"),
        Input("ppg_slider", "value")
    )
    def update_points_distribution(selected_position, max_ppg):
        # Filter based on selected position and PPG range
        filtered_df = df[(df["Position"] == selected_position) & (df["PTS/G"] <= max_ppg)]

        fig = px.bar(
            filtered_df,
            x="PTS/G",
            y="Player",
            title=f"Player Points Distribution ({selected_position})",
            orientation="h",
            color_discrete_sequence=["#636EFA"]
        ).update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Points Per Game",
            yaxis_title="Players",
            yaxis=dict(autorange="reversed"),
            margin=dict(l=150, r=40, t=50, b=50),
            xaxis=dict(gridcolor='rgba(200,200,200,0.3)')
        )

        return fig

    # ✅ Callback: Display Selected PPG Value
    @app.callback(
        Output("ppg_value", "children"),
        Input("ppg_slider", "value")
    )
    def update_ppg_value(max_ppg):
        return f"Selected Max PPG: {max_ppg}"

    # ✅ Callback: Switch Between Performance Tabs
    @app.callback(
        Output("performance-content", "children"),
        Input("performance-tabs", "value")
    )
    def update_performance_tab(selected_tab):
        if selected_tab == "scoring":
            return scoring_performance()
        elif selected_tab == "shooting":
            return shooting_efficiency()
        elif selected_tab == "points":
            return points_distribution()
        return scoring_performance()  # Default Tab
