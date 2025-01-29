import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Spider plot with average
def plot_spider_with_average(player_name, player_metrics, average_metrics, metrics, classification):
    player_stats = np.concatenate((player_metrics, [player_metrics[0]]))
    avg_stats = np.concatenate((average_metrics, [average_metrics[0]]))
    labels = np.concatenate((metrics, [metrics[0]]))

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Plot the average metrics
    ax.plot(angles, avg_stats, color='blue', linewidth=2, linestyle='--', label='Team Average')
    ax.fill(angles, avg_stats, color='blue', alpha=0.2)

    # Plot the player's metrics
    ax.plot(angles, player_stats, color=classification, linewidth=2, label=player_name)
    ax.fill(angles, player_stats, color=classification, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([])
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    ax.set_title(f"{player_name} vs Team Average", size=16)
    plt.show()
