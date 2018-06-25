import pandas as pd
import numpy as np

files = ["ap.csv", "class.csv", "demographics.csv", "grad.csv", "math.csv", "sat.csv", "school.csv"]

data = {}
for f in files:
    d = pd.read_csv("Data/" + f)
    data[f.replace(".csv","")] = d

data["school"]["DBN"] = data["school"]["dbn"]

for k,v in data.items():
    print("\n" + k + "\n")
    print(v.head())

