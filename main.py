from optimizer import generate_random_params
from experiment_runner import perform_experiment
"""
This connects your system:
generate_random_params() → chooses experiment conditions
perform_experiment() → runs experiment + gets yield
So now main.py controls the whole lab.
"""

NUM_EXPERIMENTS = 50
best_yield = 0
best_params = None

for i in range(NUM_EXPERIMENTS):
    params = generate_random_params()  
    result = perform_experiment(params)

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