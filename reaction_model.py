import numpy as np

def run_reaction(current, concentration, temp, time):
    """ 
    Simulated electrosynthesis yield model
    Returns yield in percent (0-100).
    """
    # Add experimental noise
    noise = np.random.normal(0, 2) 
    """
    This generates random noise from a normal distribution:
    Mean = 0
    Standard deviation = 2
    Meaning:
    If theoretical yield = 90%,
    Actual experimental yield might be 88% or 92%.
    This simulates:
    - Instrument error
    - Sampling error
    - Measurement noise
    - Reproducibility limits
     """
    
    # Non-linear peak behavior 
    yield_percent = (
        -0.05*(current - 50)**2
        -0.01*(concentration - 0.05)**2
        -0.03*(temp - 40)**2
        -0.02*(time - 60)**2
        + 95
        +noise
    )

    """
     -(parameter - optimal_value)^2
     This is a downward opening parabola.
     Meaning:
     Maximum yield occurs at the optimal value
     Yield decreases quadratically as you move away
     """
    """
    Current → 0.05
    Concentration → 0.1 (more sensitive!)
    Temp → 0.03
    Time → 0.02
    Higher coefficient = more sensitive parameter
    """
    """+95: sets the maximum theoretical yield to ~95%.
    Without it, everything would be negative."""
    """+ noise: adds randomness to the yield, simulating real-world variability.
    Optimizer would be too perfect.
    Reaction would be deterministic. """

    return max(0, min(100, yield_percent))
    # Ensure yield is between 0 and 100%


    
