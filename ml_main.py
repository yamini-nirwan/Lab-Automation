from experiment_runner import perform_experiment
from data_logger import log_experiment
from ml_optimizer import train_model, suggest_next_experiments

NUM_EXPERIMENTS = 150

for i in range(NUM_EXPERIMENTS):
    
    if i < 10:
        #Initital random experiments
        import random
        params = {
            "current": random.uniform(10, 100),  
            "concentration": random.uniform(0.1, 1.0),
            "temp": random.uniform(20, 80),
            "time": random.uniform(10, 120)
        }
    else:
        model = train_model() 
        params = suggest_next_experiments(model) 

    result = perform_experiment(params)

    log_experiment(result)

    print(f"\nExperiment {i+1}")
    print (params)
    print(f"Yield: {result['yield']:.2f}%")

    """
    Machine learning needs initial data.
    So we do:
    10 random experiments
    ↓
    train ML model
    ↓
    ML chooses better experiments
    """
