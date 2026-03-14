import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")  # Load the logged experiment results from the CSV file into a DataFrame.

plt.plot(df["yield"])
plt.xlabel("Experiment Number")  
plt.ylabel("Yield (%)")
plt.title("ML Optimization Progress")
plt.show()  
