import numpy as np
import pandas as pd
from reaction_model import run_reaction

#Define factor ranges + coding (convert real values ↔ coded values (−1 to +1)
# Factor ranges (based on your model optimum)
ranges = {
    "current": (30, 70),
    "concentration": (0.02, 0.08),
    "temp": (25, 55),
    "time": (30, 90)
}

def decode(code, low, high):
    return code * (high - low)/2 + (low + high)/2

#Run a fractional factorial design (using 8 experiments)
design = [
    (-1,-1,-1,-1),
    (-1,-1, 1, 1),
    (-1, 1,-1, 1),
    (-1, 1, 1,-1),
    ( 1,-1,-1, 1),
    ( 1,-1, 1,-1),
    ( 1, 1,-1,-1),
    ( 1, 1, 1, 1),
]

data = []

for row in design:
    c, conc, t, ti = row
    
    real_vals = [
        decode(c, *ranges["current"]),
        decode(conc, *ranges["concentration"]),
        decode(t, *ranges["temp"]),
        decode(ti, *ranges["time"]),
    ]
    
    y = run_reaction(*real_vals)
    data.append(list(row) + real_vals + [y])

df = pd.DataFrame(data, columns=[
    "Current_code","Conc_code","Temp_code","Time_code",
    "current","concentration","temp","time",
    "yield"
])

print(df)

#Fit a linear model (screening)
from sklearn.linear_model import LinearRegression

X = df[["Current_code","Conc_code","Temp_code","Time_code"]]
y = df["yield"]

model = LinearRegression().fit(X, y)

print("R²:", model.score(X, y))
print("Coefficients:", dict(zip(X.columns, model.coef_)))

"""Based on the coefficients, we can identify which factors have the most significant impact on yield."""

#Add center points (detect curvature)
center_results = []

for _ in range(5):
    real_vals = [
        decode(0, *ranges["current"]),
        decode(0, *ranges["concentration"]),
        decode(0, *ranges["temp"]),
        decode(0, *ranges["time"]),
    ]
    
    y = run_reaction(*real_vals)
    center_results.append(y)

print("Center yields:", center_results)
print("Mean center:", np.mean(center_results))
print("Mean factorial:", df["yield"].mean())

"""If:
mean(center) ≠ mean(factorial)
You have curvature """

#Build CCD (Central Composite Design) for adding star points
star_points = [
    (1,0,0,0), (-1,0,0,0),
    (0,1,0,0), (0,-1,0,0),
    (0,0,1,0), (0,0,-1,0),
    (0,0,0,1), (0,0,0,-1),
]
ccd_data = []

#factorial + star + center
full_design = design + star_points + [(0,0,0,0)]*5

for row in full_design:
    c, conc, t, ti = row
    
    real_vals = [
        decode(c, *ranges["current"]),
        decode(conc, *ranges["concentration"]),
        decode(t, *ranges["temp"]),
        decode(ti, *ranges["time"]),
    ]
    
    y = run_reaction(*real_vals)
    ccd_data.append(list(row) + [y])

ccd_df = pd.DataFrame(ccd_data, columns=[
    "current_code","conc_code","temp_code","time_code",
    "yield"
])

#Fit quadratic model
##add interaction + squared terms
ccd_df["current²"] = ccd_df["current_code"]**2
ccd_df["conc²"] = ccd_df["conc_code"]**2
ccd_df["temp²"] = ccd_df["temp_code"]**2
ccd_df["time²"] = ccd_df["time_code"]**2

ccd_df["current*conc"] = ccd_df["current_code"] * ccd_df["conc_code"]
ccd_df["current*temp"] = ccd_df["current_code"] * ccd_df["temp_code"]
ccd_df["current*time"] = ccd_df["current_code"] * ccd_df["time_code"]
ccd_df["conc*temp"] = ccd_df["conc_code"] * ccd_df["temp_code"]
ccd_df["conc*time"] = ccd_df["conc_code"] * ccd_df["time_code"]
ccd_df["temp*time"] = ccd_df["temp_code"] * ccd_df["time_code"]

x = ccd_df.drop(columns=["yield"])
y = ccd_df["yield"]

model_quad = LinearRegression().fit(x, y)

print("R² (quadratic):", model_quad.score(x, y))

"""R² jumped significantly
Quadratic terms are important
“curvature detected → CCD used to model it”
"""
#Find Optimum

from scipy.optimize import minimize
def objective(x):
    return -run_reaction(*x)  ##because we want to maximize yield, we minimize negative yield, so minus sign is used

"""
x is the vector of real values (current, concentration, temp, time)
x = [current, concentration, temp, time]
So:

x[0] = current
x[1] = concentration
x[2] = temp
x[3] = time
"""
initial_guess = [50, 0.05, 40, 60]  

result = minimize(objective, initial_guess)

print("Optimal conditions:", result.x)
print("Max yield:", -result.fun)

"""
result.fun = minimum value of objective function
but objective = negative yield
"""