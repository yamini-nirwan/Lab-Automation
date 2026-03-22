import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results_bayesian.csv")

plt.plot(df["yield"].cummax(), label="Bayesian Optimization")

plt.xlabel("Experiment")
plt.ylabel("Best Yield Found")
plt.title("Bayesian Optimization Progress")

plt.legend()
plt.show()