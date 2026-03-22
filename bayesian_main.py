from experiment_runner import perform_experiment
from data_logger import log_experiment
from bayesian_optimizer import (
    train_model_with_uncertainity,
    suggest_next_experiment_bayesian
)

import random

NUM_EXPERIMENTS = 50

for i in range(NUM_EXPERIMENTS):
    
    if i < 10:
        #initial random experiments
        params = {
            "current": random.uniform(0, 100),  
            "concentration": random.uniform(0.1, 1.0),
            "temp": random.uniform(20, 80),
            "time": random.uniform(10, 120)
        }

    else:
        model = train_model_with_uncertainity("results_bayesian.csv")
        params = suggest_next_experiment_bayesian(model)

    result = perform_experiment(params)
    log_experiment(result, filename="results_bayesian.csv")