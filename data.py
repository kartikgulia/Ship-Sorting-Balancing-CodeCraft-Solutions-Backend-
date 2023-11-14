import pandas as pd
import numpy as np
import matplotlib as plt


class Cargo:
    position = [0, 0]
    weight = 0
    name = ""

    def init(input, cargo_description):
        position = input[0]
        weight = input[1]
        name = cargo_description


def conversion(position, weight):  # converts string data to numbers

    x_position = position[1:3]  # getting x coord
    if (x_position[0] == '0'):
        x_position = int(x_position[1])
    else:
        x_position = int(x_position)

    y_position = position[4:6]  # getting y coord
    if (y_position[0] == '0'):
        y_position = int(y_position[1])
    else:
        y_position = int(y_position)

    XY = [x_position, y_position]

    i = 0
    for c in weight:
        if (c == '}'):
            cargo_weight = 0
        elif (c != '0' and c != '{'):
            cargo_weight = int(weight[i:6])
            break
        i += 1
    return [XY, cargo_weight]


# set this equal to name of txt file. Might need to change this depending on how the frontend will send the text file to the backend
manifest = "manifest.txt"
headers = ['Position', 'Weight', 'Cargo']
data = pd.read_csv(manifest, sep=', ', names=headers)
print(data)

# all positions and weights are strings. need to convert to numbers. planning to ignore the zero column and zero row
cargo_grid = [[Cargo] * 12] * 8

# print(conversion(data.at[7, 'Position'], data.at[7, 'Weight']))
for x in data.index:
    print(conversion(data.at[x, 'Position'], data.at[x, 'Weight']))
