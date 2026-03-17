import pandas as pd
import matplotlib.pyplot as plt

# Load the logged experiment results from the CSV file into a DataFrame.
# This CSV contains data from grid search optimization experiments.
df = pd.read_csv("results_grid.csv")

# Extract the yield values (dependent variable) and create experiment numbers (independent variable).
experiment_yields = df["yield"]
experiment_numbers = df.index + 1  # Start numbering from 1 for readability

# Create a larger figure for better visibility.
plt.figure(figsize=(12, 6))

# Plot the yield progression over experiments with markers for each point.
plt.plot(experiment_numbers, experiment_yields, linestyle="-", color="blue", label="Yield")

# Identify the experiment with the highest yield.
highest_yield_index = experiment_yields.idxmax()
highest_experiment_number = experiment_numbers[highest_yield_index]
highest_yield_value = experiment_yields.iat[highest_yield_index]

# Highlight the highest yield point with a red marker.
plt.scatter(highest_experiment_number, highest_yield_value, color="red", s=100, zorder=5, label="Highest Yield")

# Retrieve the parameters for the highest yield experiment.
# These are the input conditions that led to the best result.
best_experiment_params = df.loc[highest_yield_index, ["current", "concentration", "temp", "time"]]

# Create a summary text box showing the key details.
summary_info = (
    f"Best Experiment (#{highest_experiment_number}):\n"
    f"Yield: {highest_yield_value:.1f}%\n"
    f"Current: {best_experiment_params['current']:.1f} A\n"
    f"Concentration: {best_experiment_params['concentration']:.2f} M\n"
    f"Temperature: {best_experiment_params['temp']:.1f} °C\n"
    f"Time: {best_experiment_params['time']:.1f} min"
)

# Get the current axes for text placement.
axes = plt.gca()

# Place the summary in the top-right corner of the plot.
axes.text(
    0.98,  # X position (98% from left)
    0.98,  # Y position (98% from bottom)
    summary_info,
    transform=axes.transAxes,  # Use axes coordinates
    ha="right",  # Horizontal alignment
    va="top",   # Vertical alignment
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="black"),
)

# Add an arrow pointing to the highest point for emphasis.
plt.annotate(
    "Peak Yield",
    (highest_experiment_number, highest_yield_value),
    textcoords="offset points",
    xytext=(20, 20),  # Offset the text
    arrowprops=dict(arrowstyle="->", lw=1.5, color="red", alpha=0.8),
    fontsize=9,
    ha="left",
    color="red",
)

# Label the axes and title.
plt.xlabel("Experiment Number")
plt.ylabel("Yield (%)")
plt.title("Grid Search Optimization: Yield Over Experiments")
plt.legend()  # Show the legend for the plot lines
plt.grid(True, alpha=0.3)  # Add a subtle grid for easier reading
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()