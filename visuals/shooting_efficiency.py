from dash import dcc, html
import plotly.express as px
from app.data_loader import df

def shooting_efficiency():
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

    return html.Div([
        html.H3("Shooting Efficiency Breakdown", style={"textAlign": "center", "marginBottom": "10px"}),
        html.P("This chart breaks down each player's shooting efficiency in terms of Field Goals, Three-Point Shots, and Free Throws.",
               style={"textAlign": "center", "fontSize": "16px", "marginBottom": "15px", "maxWidth": "800px", "marginLeft": "auto", "marginRight": "auto"}),
        dcc.Graph(figure=fig)
    ])
