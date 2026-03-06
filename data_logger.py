import pandas as pd
import os

def log_experiment(result,filename= "results.csv"):
    """
    Appends experiment results to a CSV file.
    """
    data = {
        "current": result["parameters"]["current"],
        "concentration": result["parameters"]["concentration"],
        "temp": result["parameters"]["temp"],
        "time": result["parameters"]["time"],
        "yield": result["yield"]
    } 
    #NOTE: This creates a dictionary with the parameters (current, concentration, temp, time, yield) and yield from the experiment result. 

    df = pd.DataFrame([data])  # Convert dictionary to DataFrame, [data] → [] brackets indicate we are creating one row. 


    # Check if file exists. If not, first experiment.  If it already exists, we must append new experiment.
    if not os.path.exists(filename):
        df.to_csv(filename, index=False)  # Create new file with header
    else:
        df.to_csv(filename, mode='a', header=False, index=False)  # mode = 'a' means append to existing file without writing the header (column names) again

