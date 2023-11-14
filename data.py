import pandas as pd
import numpy as np
import matplotlib as plt


# set this equal to name of txt file. Might need to change this depending on how the frontend will send the text file to the backend
manifest = "manifest.txt"
headers = ['Position', 'Weight', 'Cargo']
data = pd.read_csv(manifest, sep=', ', names=headers)
print(data)

# might need to iterate through database and convert position and weight into numerical values
# print(data.iloc[1])
