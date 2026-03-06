import numpy as np

def generate_grid_params():

    currents = np.linspace(30, 70, 5) #np.linspace(start, end, number_of_points) creates evenly spaced values
    concentartions = np.linspace(0.3, 0.7, 5)
    temps = np.linspace(30, 50, 5)
    times = np.linspace(40, 80, 5)

#Nested loops generate every possible combination of parameters from the defined ranges.
#5 values for each parameter → 5*5*5*5 = 625 total combinations. So, 625 experiments will be run in total.
    for current in currents:
        for concentration in concentartions:
            for temp in temps:
                for time in times:
                    yield {                                    #yield rather than return prodcues one parameter set at a time, instead of returning everything at once.
                        "current": current,
                        "concentration": concentration,
                        "temp": temp,
                        "time": time
                    }


#Replaced the old random generator with a grid search generator. 
#This systematically explores the parameter space by creating a grid of values for each parameter and iterating through all combinations. 
"""
import random
def generate_random_params():
    return {
        "current": random.uniform(10, 100),  
        "concentration": random.uniform(0.1, 1.0),
        "temp": random.uniform(20, 80),
        "time": random.uniform(10, 120)
    }
"""
