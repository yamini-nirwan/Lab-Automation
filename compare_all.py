from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Define the CSV files and display settings for each optimization method.
comparison_configs = [
	{
		"label": "Grid Search",
		"filename": "results_grid.csv",
		"color": "royalblue"
	},
	{
		"label": "ML Optimization",
		"filename": "results_ml.csv",
		"color": "seagreen"
	},
	{
		"label": "Bayesian Optimization",
		"filename": "results_bayesian.csv",
		"color": "darkorange"
	}
]


def load_experiment_data(filename):
	"""Load one experiment history CSV file into a pandas DataFrame."""
	csv_path = Path(filename)

	if not csv_path.exists():
		raise FileNotFoundError(f"Could not find the results file: {filename}")

	return pd.read_csv(csv_path)


def build_best_result_summary(method_label, experiment_data):
	"""Create a short text summary for the best result in one method."""
	best_result_index = experiment_data["yield"].idxmax()
	best_experiment_number = best_result_index + 1
	best_yield_value = experiment_data.loc[best_result_index, "yield"]
	best_reaction_conditions = experiment_data.loc[
		best_result_index,
		["current", "concentration", "temp", "time"]
	]

	return (
		f"{method_label}\n"
		f"Best Experiment: #{best_experiment_number}\n"
		f"Yield: {best_yield_value:.2f}%\n"
		f"Current: {best_reaction_conditions['current']:.2f} A\n"
		f"Concentration: {best_reaction_conditions['concentration']:.2f} M\n"
		f"Temperature: {best_reaction_conditions['temp']:.2f} C\n"
		f"Time: {best_reaction_conditions['time']:.2f} min"
	)


# Create one figure with two subplots so both the raw yields and the running best
# yields can be compared across all optimization methods.
figure, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)

# Store the best-result summaries so they can be shown in one combined text box.
summary_blocks = []

for config in comparison_configs:
	experiment_data = load_experiment_data(config["filename"])
	experiment_numbers = experiment_data.index + 1
	experiment_yields = experiment_data["yield"]
	cumulative_best_yields = experiment_yields.cummax()

	# Plot the raw yield sequence for this method.
	axes[0].plot(
		experiment_numbers,
		experiment_yields,
		linewidth=2,
		color=config["color"],
		label=config["label"]
	)

	# Plot the running best yield so improvements over time are easy to compare.
	axes[1].plot(
		experiment_numbers,
		cumulative_best_yields,
		linewidth=2.5,
		color=config["color"],
		label=config["label"]
	)

	# Highlight the single best result for each method on the lower plot.
	best_result_index = experiment_yields.idxmax()
	best_experiment_number = best_result_index + 1
	best_yield_value = experiment_data.loc[best_result_index, "yield"]

	axes[1].scatter(
		best_experiment_number,
		best_yield_value,
		color=config["color"],
		edgecolor="black",
		s=100,
		zorder=5
	)

	summary_blocks.append(build_best_result_summary(config["label"], experiment_data))


# Label the upper plot, which shows every experiment result.
axes[0].set_title("Yield Per Experiment Across Optimization Methods")
axes[0].set_xlabel("Experiment Number")
axes[0].set_ylabel("Yield (%)")
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Label the lower plot, which shows the best yield found so far.
axes[1].set_title("Best Yield Progress Comparison")
axes[1].set_xlabel("Experiment Number")
axes[1].set_ylabel("Best Yield Found (%)")
axes[1].grid(True, alpha=0.3)
axes[1].legend()

# Add one summary box for all three methods to keep the comparison in one figure.
comparison_summary = "\n\n".join(summary_blocks)
axes[1].text(
	1.02,
	0.5,
	comparison_summary,
	transform=axes[1].transAxes,
	ha="left",
	va="center",
	fontsize=9,
	bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.95, edgecolor="black")
)

figure.suptitle("Comparison of Grid Search, ML, and Bayesian Optimization", fontsize=14)
plt.tight_layout(rect=[0, 0, 0.82, 0.97])
plt.show()
