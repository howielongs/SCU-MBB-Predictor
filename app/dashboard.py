import dash
import sys
import os

# Add the parent directory to sys.path to access 'visuals'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from layout import layout
from callbacks import register_callbacks

# Initialize Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Set Layout
app.layout = layout

# Register Callbacks
register_callbacks(app)

# Run App
if __name__ == "__main__":
    app.run_server(debug=True)
