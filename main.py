from optimizer import generate_grid_params
from experiment_runner import perform_experiment
from data_logger import log_experiment
"""
This connects your system:
generate_grid_params() → chooses experiment conditions
perform_experiment() → runs experiment + gets yield
log_experiment() → logs experiment results
main.py controls the whole lab.
"""


best_yield = 0
best_params = None

for i, params in enumerate(generate_grid_params()):  #enumerate() gives us both the index (i) and the parameter set (params) for each experiment
    
    result = perform_experiment(params)
    log_experiment(result, filename="results_grid.csv")

    print(f"\nExperiment {i+1}") # {i+1} → shows experiment number (starting from 1) because range(50) starts from 0 so experiment number becomes 1-50 instead of 0 to 49
    print(f"Parameters: {params}")
    print(f"Yield: {result['yield']:.2f}%") #This formats the number: Show 2 decimal places and makes output clean


    if result["yield"] > best_yield:
        best_yield = result["yield"]
        best_params = params
        print("New best yield found!")

print("\nOptimization complete!")
print(f"Best Yield: {best_yield:.2f}%")
print(f"Best Parameters: {best_params}")