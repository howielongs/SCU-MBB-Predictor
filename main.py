from data_loader import load_combined_data
from model import normalize_data, train_model, classify_players
from visualize import scatter_plot, bar_plot

# File paths and API endpoint
API_ENDPOINT = "https://example-api-endpoint"
EXCEL_PATH = "data/performance_metrics.xlsx"

# Load and preprocess data
data = load_combined_data(API_ENDPOINT, EXCEL_PATH)
data = normalize_data(data, ['bench_press', 'vertical_jump', 'sprint_speed', 'points', 'rebounds', 'assists'])

# Train model and classify players
model, data = train_model(data, ['bench_press', 'vertical_jump', 'sprint_speed'], 'points')
data = classify_players(data, 'residual')

# Visualize results
scatter_plot(data, 'predicted_score', 'points', 'classification')
bar_plot(data, 'classification')
