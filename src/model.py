import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

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
