import random
def generate_random_params():
    return {
        "current": random.uniform(10, 100),  
        "concentration": random.uniform(0.1, 1.0),
        "temp": random.uniform(20, 80),
        "time": random.uniform(10, 120)
    }
"""This function randomly chooses experimental conditions.
It mimics:
A chemist randomly trying different conditions.
"""
