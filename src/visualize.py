import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plot: Predicted vs. Actual Performance
def scatter_plot(df, x_col, y_col, classification_col):
    colors = {'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'}
    
    plt.figure(figsize=(10, 6))
    for classification, color in colors.items():
        subset = df[df[classification_col] == classification]
        plt.scatter(subset[x_col], subset[y_col], label=classification, c=color)

    plt.axline((0, 0), slope=1, color='gray', linestyle='--', label='Ideal Slope')
    plt.title('Player Performance vs Predicted')
    plt.xlabel('Predicted Performance')
    plt.ylabel('Actual Performance')
    plt.legend()
    plt.show()

# Bar plot: Player Classifications
def bar_plot(df, classification_col):
    sns.countplot(data=df, x=classification_col, palette={'Green': 'green', 'Yellow': 'yellow', 'Red': 'red'})
    plt.title('Player Classifications')
    plt.xlabel('Classification')
    plt.ylabel('Count')
    plt.show()
