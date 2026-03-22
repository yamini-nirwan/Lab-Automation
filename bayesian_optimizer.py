import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_model_with_uncertainity(filename= "results_ml.csv"):

    df = pd.read_csv(filename)

    x = df[["current", "concentration", "temp", "time"]]
    y = df["yield"]

    
    #Use multiple trees

    model = RandomForestRegressor(n_estimators=200)
    model.fit(x, y)

    return model

def predict_with_uncertainity(model, x):
    # Get predictions from each tree in the forest
    predictions = np.array([tree.predict(x) for tree in model.estimators_])
    
    # Calculate mean and standard deviation of predictions
    mean_prediction = np.mean(predictions, axis=0)
    std_prediction = np.std(predictions, axis=0)

    return mean_prediction, std_prediction

    #mean → predicted yield
    #std → uncertainty
    #k → exploration factor

def suggest_next_experiment_bayesian(model, n_candidates=2000, k=2.0):
    best_score = -np.inf #-np.inf = negative infinity (very very small number) i.e. "Any real score will be better than this"
    best_params = None
    
    for _ in range(n_candidates): #loop over many candidate experinments
        
        #generate random experiment parameters 
        params = {
            "current": np.random.uniform(0, 100),  
            "concentration": np.random.uniform(0.1, 1.0),  
            "temp": np.random.uniform(20, 80),  
            "time": np.random.uniform(10, 120) 
        }
        x = pd.DataFrame([params]) #convert to ML input format
        #IMPORTANT
        mean, std = predict_with_uncertainity(model, x) #predict mean and uncertainity

        #Compute acquisition Score
        score = mean[0] + k * std[0]

        if score > best_score:
            best_score = score
            best_params = params

    return best_params #return best experiment
"""
Generate 2000 possible experiments
        ↓
Predict yield + uncertainty for each
        ↓
Compute score = mean + k * std
        ↓
Pick the best one
        ↓
Return it
"""
