import pandas as pd
import numpy as np
import matplotlib as plt


class Cargo:
    position = [0, 0]
    weight = 0
    name = "NAN"


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
manifest = "new1.txt"
headers = ['Position', 'Weight', 'Cargo']
data = pd.read_csv(manifest, sep=', ', names=headers, engine='python')
print(data)

# cargo_grid = [[Cargo] * 13] * 9
# made a smaller 2D array since manifest text file only has eight slots rght now. Takes in 9 slots to fill the 3x3 portion of the array while ignoring zero row and zero column
cargo_grid = [[Cargo] * 4] * 4


# had some issues with filling the regular 2D array with just eight values. Need to make a new text file that would fit all 8x12 slots (Might be a way to get python to generate a random manifest for us).
# this algorithm basically fills the entire array. just need to change size in line of code above to the appropriate size once we have a proper manifest file to use.
i = 0
for x in cargo_grid:
    if (x == 0):
        continue
    for y in x:
        if (y == 0):
            continue
        if (i == 9):
            break
        position_weight = conversion(
            data.at[i, 'Position'],  data.at[i, 'Weight'])
        y.name = data.at[i, 'Cargo']
        y.position = position_weight[0]
        y.weight = position_weight[1]
        print(y.name, " ",
              y.position, " ", y.weight)
        i += 1
