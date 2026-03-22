import pandas as pd
import matplotlib.pyplot as plt

# Load the experiment results collected during Bayesian optimization.
df = pd.read_csv("results_bayesian.csv")

# Track the best yield found so far after each experiment.
cumulative_best_yields = df["yield"].cummax()

# Identify the experiment with the highest yield and collect its conditions.
best_result_index = df["yield"].idxmax()
best_experiment_number = best_result_index + 1
best_yield_value = df.loc[best_result_index, "yield"]
best_reaction_conditions = df.loc[
	best_result_index,
	["current", "concentration", "temp", "time"]
]

# Create experiment numbers starting from 1 so the plot matches lab counting.
experiment_numbers = df.index + 1

# Create a larger figure so the line and annotations are easier to read.
plt.figure(figsize=(12, 6))

# Plot the running best yield across the experiment sequence.
plt.plot(
	experiment_numbers,
	cumulative_best_yields,
	color="navy",
	linewidth=2.5,
	label="Best Yield So Far"
)

# Highlight the experiment that produced the overall best yield.
plt.scatter(
	best_experiment_number,
	best_yield_value,
	color="crimson",
	s=120,
	zorder=5,
	label="Best Yield"
)

# Build a text summary showing the reaction conditions for the best result.
best_result_summary = (
	f"Best Experiment: #{best_experiment_number}\n"
	f"Yield: {best_yield_value:.2f}%\n"
	f"Current: {best_reaction_conditions['current']:.2f} A\n"
	f"Concentration: {best_reaction_conditions['concentration']:.2f} M\n"
	f"Temperature: {best_reaction_conditions['temp']:.2f} C\n"
	f"Time: {best_reaction_conditions['time']:.2f} min"
)

# Add the summary box inside the plot so the key experimental result is easy to see.
plot_axes = plt.gca()
plot_axes.text(
	0.98,
	0.05,
	best_result_summary,
	transform=plot_axes.transAxes,
	ha="right",
	va="bottom",
	fontsize=10,
	bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="black")
)

# Point an annotation arrow at the best yield measurement.
plt.annotate(
	"Peak Yield",
	xy=(best_experiment_number, best_yield_value),
	xytext=(20, -25),
	textcoords="offset points",
	arrowprops=dict(arrowstyle="->", color="crimson", lw=1.5),
	fontsize=10,
	color="crimson"
)

plt.xlabel("Experiment Number")
plt.ylabel("Best Yield Found (%)")
plt.title("Bayesian Optimization Progress")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()