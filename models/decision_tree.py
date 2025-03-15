import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

#converting height to inches
def feet_inches_to_inches(value):
    if pd.isna(value) or value == "":
        return np.nan
    try:
        parts = str(value).replace("’", "'").replace('"', "'").split("'")
        feet = float(parts[0])
        inches = float(parts[1]) if len(parts) > 1 else 0
        return (feet * 12) + inches
    except:
        return np.nan

# File paths
file_paths = {
    "past_players": "Formatted_Past_Player_Career_Stats.csv",
    "physical_metrics_past": "SCU_Past_Players_Formatted.csv",
    "physical_metrics_current": "SCU-MBB-Metrics.csv",
    "performance_metrics_current": "SCU-MBB-Combined-Stats.csv"
}

# Load datasets
past_players = pd.read_csv(file_paths["past_players"])
physical_metrics_past = pd.read_csv(file_paths["physical_metrics_past"])
physical_metrics_current = pd.read_csv(file_paths["physical_metrics_current"])
performance_metrics_current = pd.read_csv(file_paths["performance_metrics_current"])

# Selecting relevant columns
past_players = past_players[["Player", "PTS/G", "FG%", "STL", "BLK"]]
physical_metrics_past = physical_metrics_past[["Player", "Wingspan", "Height w/ Shoes", "Vertical Jump", "Run Jump", "3/4 Court Sprint"]]
physical_metrics_current = physical_metrics_current[["Player", "Wingspan", "Height w/ Shoes", "Vertical Jump", "Run Jump", "3/4 Court Sprint"]]
performance_metrics_current = performance_metrics_current[["Player", "PTS/G", "FG%", "STL", "BLK"]]

# Merge past players with their physical metrics
past_data = past_players.merge(physical_metrics_past, on="Player", how="left")

# Merge current players' physical and performance metrics
current_data = physical_metrics_current.merge(performance_metrics_current, on="Player", how="left")

# Convert height and wingspan to inches
convert_cols = ["Height w/ Shoes", "Wingspan", "Run Jump"]
for col in convert_cols:
    past_data[col] = past_data[col].apply(feet_inches_to_inches)
    current_data[col] = current_data[col].apply(feet_inches_to_inches)

# Imputing missing values with median
for col in ["Wingspan", "Height w/ Shoes", "Vertical Jump", "Run Jump", "3/4 Court Sprint"]:
    past_data[col] = past_data[col].fillna(past_data[col].median())
    current_data[col] = current_data[col].fillna(current_data[col].median())

# Define features
features = ["Wingspan", "Height w/ Shoes", "Vertical Jump", "Run Jump", "3/4 Court Sprint", "PTS/G", "FG%", "STL", "BLK"]

# Use quartiles to define player levels
past_data["Player_Level"] = pd.qcut(
    past_data["PTS/G"], 
    q=4,  # Divides into 4 groups
    labels=["Bench", "Role Player", "Potential Star", "Elite"]
)

# Prepare training and testing data
X_train = past_data[features].fillna(0)
y_train = past_data["Player_Level"]
X_test = current_data[features].fillna(0)

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Decision Tree model
decision_tree_model = DecisionTreeClassifier(max_depth=6, min_samples_split=3, random_state=42)
decision_tree_model.fit(X_train_scaled, y_train)

# Predict on current players
y_pred = decision_tree_model.predict(X_test_scaled)
current_data["Predicted_Level"] = y_pred

# Display predictions
print("\n=== Predicted Player Levels ===")
print(current_data[["Player", "Predicted_Level"]])

# Visualize the Decision Tree
plt.figure(figsize=(15, 10))
plot_tree(decision_tree_model, feature_names=features, class_names=["Bench", "Role Player", "Potential Star", "Elite"], filled=True)
plt.show()