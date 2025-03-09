import os
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

# ----- Helper Functions -----
def feet_inches_to_inches(value):
    """Convert feet-inches strings to total inches"""
    if pd.isna(value) or value == "":
        return np.nan
    try:
        parts = str(value).replace("’", "'").replace('"', "'").split("'")
        feet = float(parts[0])
        inches = float(parts[1]) if len(parts) > 1 else 0
        return (feet * 12) + inches
    except:
        return np.nan

# ----- File Paths -----
input_file = os.path.join("data", "SCU-MBB-Combined-Stats.csv")
output_csv = os.path.join("data", "Player_Predictions.csv")
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)
model_file = os.path.join("models", "final_logistic_regression.pkl")
scaler_file = os.path.join("models", "final_scaler.pkl")

# ----- Data Loading & Preprocessing -----
df = pd.read_csv(input_file)

# Convert height measurements to inches
height_cols = ["Height w/o Shoes", "Height w/ Shoes", "Wingspan"]
for col in height_cols:
    df[col] = df[col].apply(feet_inches_to_inches)

# ----- Feature Engineering -----
df["Wingspan/Height Ratio"] = df["Wingspan"] / df["Height w/ Shoes"]
df["3/4 Court Sprint"] = pd.to_numeric(df["3/4 Court Sprint"], errors="coerce")
df["Sprint_Inverted"] = 1 / df["3/4 Court Sprint"]

# ----- Data Cleaning -----
critical_features = ["Wingspan/Height Ratio", "Vertical Jump", "Run Jump", "Sprint_Inverted"]
df["Vertical Jump"] = df["Vertical Jump"].fillna(df["Vertical Jump"].median())
df["Run Jump"] = df["Run Jump"].fillna(df["Run Jump"].median())
df = df.dropna(subset=["Sprint_Inverted"])

# ----- Target Definition -----
final_features = [
    "Wingspan/Height Ratio", "Vertical Jump", "Run Jump", 
    "Sprint_Inverted", "PTS/G", "FG%", "STL", "BLK"
]
df["Good_Player_Label"] = (df["PTS/G"] >= df["PTS/G"].quantile(0.65)).astype(int)

# Add synthetic data if needed
if len(df) < 20:
    synthetic_players = [
        {"Wingspan/Height Ratio": 1.05, "Vertical Jump": 35, "Run Jump": 42,
         "Sprint_Inverted": 0.33, "PTS/G": 13.5, "FG%": 0.48, "STL": 1.5, 
         "BLK": 0.9, "Good_Player_Label": 1, "Player": "Synthetic Star"},
        {"Wingspan/Height Ratio": 1.0, "Vertical Jump": 28, "Run Jump": 35,
         "Sprint_Inverted": 0.28, "PTS/G": 8.2, "FG%": 0.40, "STL": 0.8,
         "BLK": 0.4, "Good_Player_Label": 0, "Player": "Synthetic Bench"}
    ]
    df = pd.concat([df, pd.DataFrame(synthetic_players)], ignore_index=True)

# ----- Model Training -----
X = df[final_features].fillna(0)
y = df["Good_Player_Label"]

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)
except ValueError:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(
    penalty='l2', C=0.1, class_weight='balanced', solver='lbfgs', max_iter=1000
)
model.fit(X_train_scaled, y_train)

# ----- Generate Predictions -----
# For all players (train + test)
X_full_scaled = scaler.transform(X)
df["Predicted_Probability"] = model.predict_proba(X_full_scaled)[:, 1]
df["Predicted_Label"] = model.predict(X_full_scaled)

# ----- Save Outputs -----
# Save model artifacts
joblib.dump(model, model_file)
joblib.dump(scaler, scaler_file)

# Save predictions CSV
output_columns = [
    "Player", "Good_Player_Label", "Predicted_Probability", "Predicted_Label",
    "Height w/ Shoes", "Wingspan", "Vertical Jump", "PTS/G", "FG%"
]
df[output_columns].to_csv(output_csv, index=False)

# ----- Evaluation Metrics -----
y_pred = model.predict(X_test_scaled)
print("\n=== Evaluation Metrics ===")
print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Test F1-Score: {f1_score(y_test, y_pred):.2f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print(f"\n✅ Predictions saved to: {output_csv}")

# Feature Importance
feature_importance = pd.DataFrame({
    "Feature": final_features,
    "Coefficient": model.coef_[0]
}).sort_values("Coefficient", ascending=False)
print("\n=== Feature Importance ===")
print(feature_importance)