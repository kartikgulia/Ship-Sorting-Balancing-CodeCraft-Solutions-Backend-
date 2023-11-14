import pandas as pd
import numpy as np

manifest = "manifest.txt"  # set this equal to name of txt file
headers = ['Position', 'Weight', 'Cargo']
data = pd.read_csv(manifest, names=headers)
print(data)
