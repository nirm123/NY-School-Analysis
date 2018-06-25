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

# Import survey data
survey1 = pd.read_csv("Data/masterfile11_d75_final.txt", delimiter = "\t", encoding = "windows-1252")

survey2 = pd.read_csv("Data/masterfile11_gened_final.txt", delimiter = "\t", encoding = "windows-1252")

survey1["d75"] = True
survey2["d75"] = False

survey = pd.concat([survey1, survey2], axis=0)

# Format survey data
survey["DBN"] = survey["dbn"]
surveyf = ["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11",]

survey = survey.loc[:, surveyf]
data["survey"] = survey

# Condense data
clas = data["class"]
clas = clas[clas["GRADE "] == "09-12"]
clas = clas[clas["PROGRAM TYPE"] == "GEN ED"]
clas = clas.groupby("DBN").agg(np.mean)
clas.reset_index(inplace = True)
data["class"] = clas

