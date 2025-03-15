# visuals/prediction_table.py

import dash
from dash import dash_table, html
import pandas as pd
from app.data_loader import df

def prediction_table():
    """
    Returns a Dash layout (DataTable) showing the predicted probabilities 
    and labels for each player.
    """
    # Define the columns you want to display
    columns_to_show = [
        "Player", 
        "PTS/G", 
        "FG%", 
        "Predicted_Probability", 
        "Predicted_Label"
    ]
    
    # Filter df to these columns only (in case some are missing)
    available_cols = [col for col in columns_to_show if col in df.columns]
    
    # Create the table
    return html.Div([
        html.H3("Player Potential Predictions"),
        dash_table.DataTable(
            data=df[available_cols].to_dict("records"),
            columns=[{"name": col, "id": col} for col in available_cols],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "left", 
                "minWidth": "80px", 
                "width": "150px", 
                "maxWidth": "200px"
            },
            style_header={"fontWeight": "bold"},
        )
    ])
