# -*- coding: utf-8 -*-
"""NBA Draft Project.ipynb

"""

import os
import pandas as pd

# Change the directory below to your google drive file location

#Jonah's Location
#drive.mount('/content/drive')
#os.chdir("drive/My Drive")

# drive.mount("/content/drive", force_remount=True)
#os.chdir("drive/My Drive/CSCI183/Project")
df = pd.read_csv("NBA Combine Stats - Stats.csv", na_values=["-"])
df.head()

"""## Data Cleaning"""

df["is_drafted"] = df["Drafted"].notna().astype(int)
df = df.drop("Drafted", axis=1)

# Function to convert to inches
def convert_to_inches(value):
    if pd.isna(value):  # Keep NaN values unchanged
        return None
    if isinstance(value, (int, float)):  # If already numeric, return as-is
        return value
    if isinstance(value, str):  # Ensure it's a string before processing
        parts = value.split("' ")
        if len(parts) == 2:
            feet = int(parts[0].strip())  # Extract feet
            inches = float(parts[1].replace("''", "").strip())  # Extract inches
            return (feet * 12) + inches
    return None  # Default case for unexpected values

# Apply conversion to all relevant columns
for col in ['HEIGHT W/O SHOES', 'STANDING REACH', 'WINGSPAN']:
    df[col] = df[col].apply(convert_to_inches)

df.head(10)

# Count missing values in each column
missing_by_column = df.isna().sum()

# Get percentage of missing values in each column
missing_percentage = (missing_by_column / len(df)) * 100

# Create a summary dataframe showing counts and percentages
missing_summary = pd.DataFrame({
    'Missing Values': missing_by_column,
    'Percentage': missing_percentage
})

# Sort by number of missing values in descending order
missing_summary = missing_summary.sort_values('Missing Values', ascending=False)

# Filter to only show columns that have missing values
missing_summary = missing_summary[missing_summary['Missing Values'] > 0]

print("Columns with missing values:")
print(missing_summary)

# Count rows with missing values
missing_rows = df.isna().any(axis=1).sum()
print(f"\nNumber of rows with missing values: {missing_rows}")
print(f"Percentage of rows with missing values: {missing_rows/len(df)*100:.2f}%")

# Count rows based on number of missing values
missing_counts = df.isna().sum(axis=1)
missing_value_distribution = {
    '1 missing value': (missing_counts == 1).sum(),
    '2 missing values': (missing_counts == 2).sum(),
    '3 missing values': (missing_counts == 3).sum(),
    '4 missing values': (missing_counts == 4).sum(),
    '5+ missing values': (missing_counts >= 5).sum()
}

# Print the distribution
print("\nDistribution of missing values per row:")
for key, value in missing_value_distribution.items():
    print(f"{key}: {value}")

# Count missing values per row
missing_counts = df.isna().sum(axis=1)

# Keep only rows with fewer than 5 missing values
df = df[missing_counts < 5]

print(f"Number of rows after deletion: {len(df)}")

# Count missing values per row
missing_counts = df.isna().sum(axis=1)

# Print count of missing values for each column
missing_by_column = df.isna().sum()
print("Missing values count per column:")
print(missing_by_column)

df = df.drop("Shuttle Run \n(seconds)", axis=1)

# Calculate the mean of the column, ignoring NaN values
mean_value = df["Three Quarter Sprint \n(seconds)"].mean()

# Fill the missing value with the mean
df["Three Quarter Sprint \n(seconds)"] = df["Three Quarter Sprint \n(seconds)"].fillna(mean_value)

unique_values = df["POS"].unique()
print(unique_values)

df["POS"] = df["POS"].replace({"SG": "G", "PG": "G", "SG-SF": "G", "C": "F", "PF": "F", "SF": "F"})

df_G = df[df["POS"] == "G"]
df_F = df[df["POS"] == "F"]

# Print the number of drafted and undrafted players in df_G and df_F
def print_draft_counts(df, df_name):
    draft_counts = df['is_drafted'].value_counts()
    print(f"Drafted and Undrafted Counts for {df_name}:")
    print(draft_counts.to_string(), "\n")

print_draft_counts(df_G, 'df_G')
print_draft_counts(df_F, 'df_F')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# List of feature columns
feature_columns = ['HAND LENGTH (inches)', 'HAND WIDTH (inches)',
                   'HEIGHT W/O SHOES', 'STANDING REACH', 'WEIGHT (LBS)', 'WINGSPAN',
                   'Lane Agility Time \n(seconds)', 'Three Quarter Sprint \n(seconds)',
                   'Standing Vertical Leap \n(inches)', 'Max Vertical Leap \n(inches)']

from imblearn.over_sampling import SMOTE

def apply_smote(df):

    # Drop rows with missing values
    df = df.dropna(subset=feature_columns + ['is_drafted'])

    # Define features (X) and target (y)
    X = df[feature_columns]
    y = df['is_drafted']

    # Apply SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Convert back to DataFrame
    df_resampled = pd.DataFrame(X_resampled, columns=feature_columns)
    df_resampled['is_drafted'] = y_resampled

    return df_resampled

# Apply SMOTE to df_G and df_F
df_G_balanced = apply_smote(df_G)
df_F_balanced = apply_smote(df_F)

print_draft_counts(df_G_balanced, 'df_G')
print_draft_counts(df_F_balanced, 'df_F')

import matplotlib.pyplot as plt
import seaborn as sns

"""## EDA HERE"""

# Calculate correlations for all features with is_drafted for guards
numeric_cols = df_G.select_dtypes(include=['float64', 'int64']).columns.tolist()
if 'is_drafted' in numeric_cols:
    numeric_cols.remove('is_drafted')  # Remove target from features list

# Calculate all correlations with is_drafted
guards_correlations = {}
for feature in numeric_cols:
    correlation = df_G[feature].corr(df_G['is_drafted'])
    guards_correlations[feature] = correlation

# Convert to DataFrame
guards_corr_df = pd.DataFrame(list(guards_correlations.items()), columns=['Feature', 'Correlation'])

# Get top 2 positive and top 2 negative correlations
top_positive = guards_corr_df.sort_values('Correlation', ascending=False).head(2)
top_negative = guards_corr_df.sort_values('Correlation', ascending=True).head(2)

# Combine them for our feature list
selected_features = pd.concat([top_positive, top_negative])
print("Selected features with strongest correlations (Guards):")
print(selected_features)

# Get feature names for plotting
feature_list = selected_features['Feature'].tolist()

# Create scatter plots for the selected feature pairs
plt.figure(figsize=(20, 15))

# Plot 1: Top positive feature vs Top negative feature
plt.subplot(2, 2, 1)
sns.scatterplot(data=df_G, x=feature_list[0], y=feature_list[2],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[0]} (+) vs {feature_list[2]} (-) (Guards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

# Plot 2: Second positive feature vs Second negative feature
plt.subplot(2, 2, 2)
sns.scatterplot(data=df_G, x=feature_list[1], y=feature_list[3],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[1]} (+) vs {feature_list[3]} (-) (Guards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

# Plot 3: Top two positive features
plt.subplot(2, 2, 3)
sns.scatterplot(data=df_G, x=feature_list[0], y=feature_list[1],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[0]} (+) vs {feature_list[1]} (+) (Guards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

# Plot 4: Top two negative features
plt.subplot(2, 2, 4)
sns.scatterplot(data=df_G, x=feature_list[2], y=feature_list[3],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[2]} (-) vs {feature_list[3]} (-) (Guards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

plt.tight_layout()
plt.show()

# Calculate correlations for all features with is_drafted for forwards
numeric_cols = df_F.select_dtypes(include=['float64', 'int64']).columns.tolist()
if 'is_drafted' in numeric_cols:
    numeric_cols.remove('is_drafted')  # Remove target from features list

# Calculate all correlations with is_drafted
forwards_correlations = {}
for feature in numeric_cols:
    correlation = df_F[feature].corr(df_F['is_drafted'])
    forwards_correlations[feature] = correlation

# Convert to DataFrame
forwards_corr_df = pd.DataFrame(list(forwards_correlations.items()), columns=['Feature', 'Correlation'])

# Get top 2 positive and top 2 negative correlations
top_positive = forwards_corr_df.sort_values('Correlation', ascending=False).head(2)
top_negative = forwards_corr_df.sort_values('Correlation', ascending=True).head(2)

# Combine them for our feature list
selected_features = pd.concat([top_positive, top_negative])
print("Selected features with strongest correlations (Forwards):")
print(selected_features)

# Get feature names for plotting
feature_list = selected_features['Feature'].tolist()

# Create scatter plots for the selected feature pairs
plt.figure(figsize=(20, 15))

# Plot 1: Top positive feature vs Top negative feature
plt.subplot(2, 2, 1)
sns.scatterplot(data=df_F, x=feature_list[0], y=feature_list[2],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[0]} (+) vs {feature_list[2]} (-) (Forwards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

# Plot 2: Second positive feature vs Second negative feature
plt.subplot(2, 2, 2)
sns.scatterplot(data=df_F, x=feature_list[1], y=feature_list[3],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[1]} (+) vs {feature_list[3]} (-) (Forwards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

# Plot 3: Top two positive features
plt.subplot(2, 2, 3)
sns.scatterplot(data=df_F, x=feature_list[0], y=feature_list[1],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[0]} (+) vs {feature_list[1]} (+) (Forwards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

# Plot 4: Top two negative features
plt.subplot(2, 2, 4)
sns.scatterplot(data=df_F, x=feature_list[2], y=feature_list[3],
                hue='is_drafted', palette=['#ff7f0e', '#1f77b4'], s=100, alpha=0.7)
plt.title(f'{feature_list[2]} (-) vs {feature_list[3]} (-) (Forwards)')
plt.legend(title='Drafted', labels=['No', 'Yes'])

plt.tight_layout()
plt.show()

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add position identifier to each dataframe
df_G['Position_Group'] = 'Guard'
df_F['Position_Group'] = 'Forward'

# Combine for comparison
combined_df = pd.concat([df_G, df_F])

# Function to create comparison plot for a feature
def compare_feature(feature_name):
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=[f"{feature_name} - Guards", f"{feature_name} - Forwards"])

    # Add histograms
    fig.add_trace(
        go.Histogram(x=df_G[df_G['is_drafted']==1][feature_name],
                    name="Drafted", marker_color='blue', opacity=0.6),
        row=1, col=1
    )
    fig.add_trace(
        go.Histogram(x=df_G[df_G['is_drafted']==0][feature_name],
                    name="Not Drafted", marker_color='orange', opacity=0.6),
        row=1, col=1
    )

    fig.add_trace(
        go.Histogram(x=df_F[df_F['is_drafted']==1][feature_name],
                    name="Drafted", marker_color='blue', opacity=0.6, showlegend=False),
        row=1, col=2
    )
    fig.add_trace(
        go.Histogram(x=df_F[df_F['is_drafted']==0][feature_name],
                    name="Not Drafted", marker_color='orange', opacity=0.6, showlegend=False),
        row=1, col=2
    )

    fig.update_layout(barmode='overlay', height=400, width=900,
                     title=f"Comparison of {feature_name} between Guards and Forwards")
    fig.show()

# Create comparative scatter plots
def compare_scatter(feature_x, feature_y):
    fig = go.Figure()

    # Guards - Not Drafted
    fig.add_trace(go.Scatter(
        x=df_G[df_G['is_drafted']==0][feature_x],
        y=df_G[df_G['is_drafted']==0][feature_y],
        mode='markers',
        name='Guards - Not Drafted',
        marker=dict(color='orange', symbol='circle', size=10)
    ))

    # Guards - Drafted
    fig.add_trace(go.Scatter(
        x=df_G[df_G['is_drafted']==1][feature_x],
        y=df_G[df_G['is_drafted']==1][feature_y],
        mode='markers',
        name='Guards - Drafted',
        marker=dict(color='blue', symbol='circle', size=10)
    ))

    # Forwards - Not Drafted
    fig.add_trace(go.Scatter(
        x=df_F[df_F['is_drafted']==0][feature_x],
        y=df_F[df_F['is_drafted']==0][feature_y],
        mode='markers',
        name='Forwards - Not Drafted',
        marker=dict(color='orange', symbol='square', size=10)
    ))

    # Forwards - Drafted
    fig.add_trace(go.Scatter(
        x=df_F[df_F['is_drafted']==1][feature_x],
        y=df_F[df_F['is_drafted']==1][feature_y],
        mode='markers',
        name='Forwards - Drafted',
        marker=dict(color='blue', symbol='square', size=10)
    ))

    fig.update_layout(
        title=f"{feature_x} vs {feature_y} - Guards and Forwards",
        xaxis_title=feature_x,
        yaxis_title=feature_y,
        height=600,
        width=800
    )
    fig.show()

# Function to compare correlations between guards and forwards
def compare_correlations():
    # Get top correlations for both groups
    g_correlations = pd.Series({f: df_G[f].corr(df_G['is_drafted'])
                              for f in df_G.select_dtypes(include=['float64', 'int64']).columns
                              if f != 'is_drafted'})

    f_correlations = pd.Series({f: df_F[f].corr(df_F['is_drafted'])
                              for f in df_F.select_dtypes(include=['float64', 'int64']).columns
                              if f != 'is_drafted'})

    # Combine into a dataframe
    corr_df = pd.DataFrame({
        'Guards': g_correlations,
        'Forwards': f_correlations
    })

    # Sort by average absolute correlation
    corr_df['avg_abs'] = (corr_df['Guards'].abs() + corr_df['Forwards'].abs()) / 2
    corr_df = corr_df.sort_values('avg_abs', ascending=False).drop('avg_abs', axis=1)

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=corr_df.index,
        x=corr_df['Guards'],
        name='Guards',
        orientation='h',
        marker_color='royalblue'
    ))

    fig.add_trace(go.Bar(
        y=corr_df.index,
        x=corr_df['Forwards'],
        name='Forwards',
        orientation='h',
        marker_color='darkorange'
    ))

    fig.update_layout(
        title='Feature Correlations with Draft Status',
        barmode='group',
        height=600,
        width=900
    )
    fig.show()

    return corr_df

# Usage example:
# 1. Compare distributions of a specific feature
compare_feature('WINGSPAN')

# 2. Create a scatter plot comparing two features
compare_scatter('WINGSPAN', 'HEIGHT W/O SHOES')

# 3. Compare correlations between guards and forwards
corr_df = compare_correlations()
print(corr_df)  # Print the correlation comparison table

"""## Models

"""

def perform_logistic_regression(df, df_name):
    # Drop rows with missing values
    df = df.dropna(subset=feature_columns + ['is_drafted'])

    # Define features (X) and target (y)
    X = df[feature_columns]
    y = df['is_drafted']

    # Split into training and test sets (70-30 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Logistic Regression Model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Results for {df_name}:")
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:")
    print(report)
    print("-" * 50)

# Run the Model
perform_logistic_regression(df_G, 'df_G')
perform_logistic_regression(df_G_balanced, 'df_G_balanced')
perform_logistic_regression(df_F, 'df_F')
perform_logistic_regression(df_F_balanced, 'df_F_balanced')

df2 = pd.read_csv("SCU_Players_Stats.csv", na_values=["-"])

df2.head()

# Function to convert height format "6'8.25" to inches
def new_height_to_inches(height):
    if isinstance(height, str) and "'" in height:
        feet, inches = height.split("'")
        return int(feet) * 12 + float(inches)
    return None  # Handle invalid values

# List of columns to convert
columns_to_convert = ['Height w/o Shoes', 'Standing Reach', 'Wingspan']

# Apply conversion to each column
for col in columns_to_convert:
    df2[col] = df2[col].apply(new_height_to_inches)

df_SCU_G = df2[df2["Position"] == "G"]
df_SCU_F = df2[df2["Position"] == "F"]

df_SCU_F.head()

from sklearn.preprocessing import StandardScaler

# Feature name mapping
feature_map = {
    'Height w/o Shoes': 'HEIGHT W/O SHOES',
    'Standing Reach': 'STANDING REACH',
    'Weight (lbs)': 'WEIGHT (LBS)',
    'Wingspan': 'WINGSPAN',
    '3/4 Court Sprint': 'Three Quarter Sprint \n(seconds)',
    'Vertical Jump': 'Standing Vertical Leap \n(inches)',
    'Run Jump': 'Max Vertical Leap \n(inches)'
}

# Function to predict if players will go pro
def predict_draft_status(model, scaler, df_scu, position):
    # Select relevant features and rename them
    df_scu = df_scu[['Player'] + list(feature_map.keys())].dropna()
    df_scu.rename(columns=feature_map, inplace=True)

    # Standardize features
    X_scu = scaler.transform(df_scu.drop(columns=['Player']))

    # Make predictions
    predictions = model.predict(X_scu)

    # Print results
    for player, pred in zip(df_scu['Player'].values, predictions):
        draft_status = 'Drafted' if pred == 1 else 'Not Drafted'
        print(f"Player: {player}, Position: {position}, Predicted Draft Status: {draft_status}")

# Train models using df_G_balanced and df_F_balanced
scaler_G = StandardScaler()
X_G = df_G_balanced[[feature_map[col] for col in feature_map.keys()]].dropna()
y_G = df_G_balanced['is_drafted']
X_G_scaled = scaler_G.fit_transform(X_G)
model_G = LogisticRegression()
model_G.fit(X_G_scaled, y_G)

scaler_F = StandardScaler()
X_F = df_F_balanced[[feature_map[col] for col in feature_map.keys()]].dropna()
y_F = df_F_balanced['is_drafted']
X_F_scaled = scaler_F.fit_transform(X_F)
model_F = LogisticRegression()
model_F.fit(X_F_scaled, y_F)

# Predict for SCU players
predict_draft_status(model_G, scaler_G, df_SCU_G, 'Guard')
predict_draft_status(model_F, scaler_F, df_SCU_F, 'Forward')