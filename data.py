import pandas as pd
import numpy as np

# set this equal to name of txt file. Might need to change this depending on how the frontend will send the text file to the backend
manifest = "manifest.txt"
headers = ['Position', 'Weight', 'Cargo']
data = pd.read_csv(manifest, names=headers)
print(data)
