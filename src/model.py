import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Normalize data
def normalize_data(df, columns):
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

# Train linear regression model
def train_model(df, features, target):
    X = df[features]
    y = df[target]

    model = LinearRegression()
    model.fit(X, y)
    df['predicted_score'] = model.predict(X)
    return model, df

# Classify players
def classify_players(df, residual_column):
    df['residual'] = df['points'] - df['predicted_score']
    df['classification'] = pd.cut(
        df[residual_column],
        bins=[-float('inf'), -2, 2, float('inf')],
        labels=['Red', 'Yellow', 'Green']
    )
    return df

# Calculate team average and standard deviation
def calculate_team_stats(df, metrics):
    team_stats = {
        'mean': df[metrics].mean(),
        'std': df[metrics].std()
    }
    return team_stats

# Standardize player metrics
def calculate_player_scores(df, metrics, team_stats):
    for metric in metrics:
        df[f"{metric}_zscore"] = (df[metric] - team_stats['mean'][metric]) / team_stats['std'][metric]
    return df

# Classify players by z-score
def classify_players_by_zscore(df, metrics):
    classification = []
    for i, row in df.iterrows():
        if all(-1 <= row[f"{metric}_zscore"] <= 1 for metric in metrics):
            classification.append('Green')
        elif any(1 < abs(row[f"{metric}_zscore"]) <= 2 for metric in metrics):
            classification.append('Yellow')
        else:
            classification.append('Red')
    df['classification'] = classification
    return df