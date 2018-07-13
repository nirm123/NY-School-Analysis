import pandas as pd
import numpy as np
import folium
from folium import plugins
from folium.plugins import MarkerCluster

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

# Condense class data
clas = data["class"]
clas = clas[clas["GRADE "] == "09-12"]
clas = clas[clas["PROGRAM TYPE"] == "GEN ED"]
clas = clas.groupby("DBN").agg(np.mean)
clas.reset_index(inplace = True)
data["class"] = clas

# Condense demographics data
dem = data["demographics"]
dem = dem[dem["schoolyear"] == 20112012]
data["demographics"] = dem

# Condense math data
math = data["math"]
math = math[math["Year"] == 2011]
math = math[math["Grade"] == "8"]
data["math"] = math

# Condense graduation data
grad = data["grad"]
grad = grad[grad["Cohort"] == "2006"]
grad = grad[grad["Demographic"] == "Total Cohort"]
data["grad"] = grad

# Compute avg SAT cumulative score
data["sat"]["SAT Critical Reading Avg. Score"] = pd.to_numeric(data["sat"]["SAT Critical Reading Avg. Score"], errors = "coerce")
data["sat"]["SAT Math Avg. Score"] = pd.to_numeric(data["sat"]["SAT Math Avg. Score"], errors = "coerce")
data["sat"]["SAT Writing Avg. Score"] = pd.to_numeric(data["sat"]["SAT Writing Avg. Score"], errors = "coerce")

data["sat"]["total"] = data["sat"]["SAT Writing Avg. Score"] + data["sat"]["SAT Math Avg. Score"] + data["sat"]["SAT Critical Reading Avg. Score"]

# Convert latitude and longitude from string to float
data["school"]["Longitude"] = pd.to_numeric(data["school"]["Longitude"])
data["school"]["Latitude"] = pd.to_numeric(data["school"]["Latitude"])

# Code to check data
#for k,v in data.items():
#    print("\n" + k + "\n")
#    print(v)

# Combine data
sub = [a for a,b in data.items()]
sub_data = [data[a] for a in sub]
full = sub_data[4]
for i,g in enumerate(sub_data):
    name = sub[i]
    #print(name)
    #print(len(g["DBN"]) - len(g["DBN"].unique()))
    join = "inner"
    if name in ["ap", "sat", "grad"]:
        join = "outer"
    if name != "math":
        full = full.merge(g, on = "DBN", how = join)

# Cleaning AP
for a in ["AP Test Takers ", "Total Exams Taken", "Number of Exams with scores 3 4 or 5"]:
    full[a] = pd.to_numeric(full[a], errors = "coerce")
    full[a] = full[a].fillna(value=0)

# Add school district
full["schoold"] = full["DBN"].apply(lambda x: x[:2])

# Remove null values
full = full.fillna(full.mean())

# Compute correlation
corr = full.corr()["total"]
html = "<html><body><h1>Correlation</h1>" 
for i, v in corr.iteritems():
    html += "<b>" + str(i) + "</b>"
    html += "   :   "
    html += str(v)
    html += "<br />"
html += "</body></html>"
html_corr = open("docs/Results/correlation.html","w")
html_corr.write(html)
html_corr.close()

# Display map
smap = folium.Map(location=[full["Latitude"].mean(), full["Longitude"].mean()], zoom_start = 10)
marky = MarkerCluster().add_to(smap)
for a, b in full.iterrows():
    name = b["DBN"]
    trial = "test"
    folium.Marker([b["Latitude"], b["Longitude"]], popup = name ).add_to(marky)
smap.save(outfile = "docs/Maps/location.html")

sheat = folium.Map(location=[full['Latitude'].mean(), full['Longitude'].mean()], zoom_start=10)
sheat.add_child(plugins.HeatMap([[row["Latitude"], row["Longitude"]] for name, row in full.iterrows()]))
sheat.save(outfile = "docs/Maps/heatmap.html")

