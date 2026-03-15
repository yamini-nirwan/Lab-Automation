import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def train_model(filename = "results.csv"):
    """
    Train ML model to predict reaction yield.
    """
    # Load the experimental data
    df = pd.read_csv("results_ml.csv")
    
    # Define features and target
    X = df[["current", "concentration", "temp", "time"]] #define input variables
    y = df["yield"] # define output variable
    
    # Initialize the model
    model = RandomForestRegressor(n_estimators=100)
    
    # Train the model
    model.fit(X, y) #this step teaches the model the relationship between the input variables (reaction parameters) and the output variable (yield)
    
    return model #returns the trained model to be used for making predictions


def suggest_next_experiments(model, n_candidates=5000):
    
    """
    Use the trained model to predict promising experiments.
    """
    # Generate random candidate experiments
    candidates = [] #create list to store candidate experiments which will hold (predicted yield, parameters)

    for _ in range(n_candidates): #generate many random experiments

        params = {
            "current": np.random.uniform(10, 100),  
            "concentration": np.random.uniform(0.1, 1.0),
            "temp": np.random.uniform(20, 80),
            "time": np.random.uniform(10, 120)
        } #generate random reaction parameters within specified ranges

        #Convert parameters into ML input format
        #Machine learning models expect input as a 2D array.
        X = pd.DataFrame([params]) #feature names match the column names used during training (current, concentration, temp, time) and [params] creates a DataFrame with one row containing the

        #Predict yield
        predicted_yield = model.predict(X)[0]  #[0] extracts the first element from the predicted yield array returned by the model
        
        candidates.append((predicted_yield, params))
        
    # Sort candidates by predicted yield
    candidates.sort(key=lambda x: x[0], reverse=True) #best experiment is at the top within the list
    return candidates[0][1] 
