import pandas as pd
import numpy as np
import matplotlib as plt


class Cargo:
    position = [0, 0]
    weight = 0
    name = "NAN"


class Cargo_Grid:
    # cargo_grid = [[Cargo] * 13] * 9
    # made a smaller 2D array since manifest text file only has 9 slots rght now. Takes in 9 slots to fill the 3x3 portion of the array while ignoring zero row and zero column
    # array_builder function works for any array size, just need to modify sizes of cargo grid
    cargo_grid = [[Cargo] * 4 for _ in range(4)]

    def __init__(self, data):
        self.data = data

    def array_builder(self):
        i = 0
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                position_weight = conversion(
                    self.data.at[i, 'Position'],  self.data.at[i, 'Weight'])
                self.cargo_grid[x][y] = Cargo()
                self.cargo_grid[x][y].name = self.data.at[i, 'Cargo']
                self.cargo_grid[x][y].position = position_weight[0]
                self.cargo_grid[x][y].weight = position_weight[1]
                i += 1

    def print(self):
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                print(self.cargo_grid[x][y].name, " ",
                      self.cargo_grid[x][y].position, " ",  self.cargo_grid[x][y].weight)

    # this function should be used when writing the updated cargo grid array back to the manifest
    def output_manifest(self, file__name):
        output = ""
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                output += num_to_string(
                    self.cargo_grid[x][y].position, self.cargo_grid[x][y].weight, self.cargo_grid[x][y].name)
                output += '\n'
        with open(file__name, "w") as file:
            file.write(output)


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


def num_to_string(position, weight, name):  # converts position and weight back to string
    str_cargo = '[0' + str(position[0]) + ','
    if (position[1] < 10):
        str_cargo += '0' + str(position[1]) + "], {"
    str_weight = str(weight)
    for x in range(0, 5 - len(str_weight)):
        str_cargo += '0'
    str_cargo += str_weight + "}, " + name
    return str_cargo


# set this equal to name of txt file. Might need to change this depending on how the frontend will send the text file to the backend
manifest = "new1.txt"
headers = ['Position', 'Weight', 'Cargo']
data = pd.read_csv(manifest, sep=', ', names=headers, engine='python')
print(data)


cargo_grid = Cargo_Grid(data)
cargo_grid.array_builder()
cargo_grid.print()

# print(num_to_string(cargo_grid.cargo_grid[2][3].position,
# cargo_grid.cargo_grid[2][3].weight, cargo_grid.cargo_grid[2][3].name))

# need to find a way to have the system either make a new text file or clear the original manifest
cargo_grid.output_manifest("new1OUTBOUND.txt")
