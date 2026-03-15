import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results_grid.csv")  # Load the logged experiment results from the CSV file into a DataFrame.

plt.plot(df["yield"])
plt.xlabel("Experiment Number")  
plt.ylabel("Yield (%)")
plt.title("Yield Across Experiments")
plt.show()  
# This code visualizes the yield across all experiments by plotting the yield against the experiment number.