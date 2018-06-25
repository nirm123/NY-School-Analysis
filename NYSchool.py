import pandas as pd
import numpy as np

# File names
files = ["ap.csv", "class.csv", "demographics.csv", "grad.csv", "math.csv", "sat.csv", "school.csv"]

# Importing data
data = {}
for f in files:
    d = pd.read_csv("Data/" + f)
    data[f.replace(".csv","")] = d

# Adding DBN
data["school"]["DBN"] = data["school"]["dbn"]
data["class"]["DBN"] = data["class"].apply(lambda x: "{0:02d}{1}".format(x["CSD"],x["SCHOOL CODE"]), axis=1)

# Code to check data
#for k,v in data.items():
#    print("\n" + k + "\n")
#    print(v.head())



