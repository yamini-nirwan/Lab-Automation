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