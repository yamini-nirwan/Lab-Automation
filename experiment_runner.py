from reaction_model import run_reaction
#This means: “Go to the reaction model file and use the function we built.”
def perform_experiment(params):
    """
    Simulates running a single electrochemical experiment.
    """

    yield_result = run_reaction(
        current=params["current"],
        concentration=params["concentration"],
        temp=params["temp"],
        time=params["time"]    #This line: Extracts values from the dictionary, Sends them into the reactor, Gets the yield back
    )

    return {
        "parameters": params,
        "yield": yield_result
    } 
"""
perform_experiment() → runs experiment + gets yield
"""

