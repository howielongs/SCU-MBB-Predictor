from dash import dcc, html
import plotly.express as px
from app.data_loader import df

def shooting_efficiency():
    # Melt DataFrame to make it suitable for stacked bar chart
    df_melted = df.melt(id_vars=["Player"], value_vars=["FG%", "3FG%", "FT%"], var_name="Shot Type", value_name="Percentage")

    fig = px.bar(
        df_melted,
        x="Player",
        y="Percentage",
        color="Shot Type",
        title="Shooting Efficiency Breakdown",
        labels={"Percentage": "Shooting Percentage"},
        barmode="stack",
    )

    fig.update_layout(
        xaxis_title="Players",
        yaxis_title="Shooting % (FG%, 3P%, FT%)",
        xaxis=dict(tickangle=-45),
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return html.Div([dcc.Graph(figure=fig)])
