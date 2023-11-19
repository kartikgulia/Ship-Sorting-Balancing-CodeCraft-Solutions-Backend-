import pandas as pd
import numpy as np
import matplotlib as plt


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
    else:
        str_cargo += str(position[1]) + "], {"
    str_weight = str(weight)
    for x in range(0, 5 - len(str_weight)):
        str_cargo += '0'
    str_cargo += str_weight + "}, " + name
    return str_cargo


class Cargo:
    position = [0, 0]
    weight = 0
    name = "UNUSED"


class Cargo_Grid:
    cargo_grid = [[Cargo] * 13 for _ in range(9)]

    def __init__(self, pandasDF_for_Manifest):
        self.pandasDF_for_Manifest = pandasDF_for_Manifest

    # sets all positions
    def initial_array(self):
        i = 0
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                self.cargo_grid[x][y] = Cargo()
                self.cargo_grid[x][y].position = [x, y]
                i += 1

    def array_builder(self):
        self.initial_array()
        for x in range(len(self.pandasDF_for_Manifest)):
            position_weight = conversion(
                self.pandasDF_for_Manifest.at[x, 'Position'],  self.pandasDF_for_Manifest.at[x, 'Weight'])
            pos = position_weight[0]
            self.cargo_grid[pos[0]][pos[1]].name = self.pandasDF_for_Manifest.at[x, 'Cargo']
            self.cargo_grid[pos[0]][pos[1]].position = pos
            self.cargo_grid[pos[0]][pos[1]].weight = position_weight[1]

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
    def output_manifest(self, file_name):
        file = file_name
        with open(file, "w") as file:
            pass
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
        with open(file_name, "w") as file:
            file.write(output)



if __name__ == "__main__":
    # set this equal to name of txt file. Might need to change this depending on how the frontend will send the text file to the backend
    manifest = "new1.txt"
    headers = ['Position', 'Weight', 'Cargo']
    pandasDF_for_Manifest = pd.read_csv(manifest, sep=', ', names=headers, engine='python')
    print(pandasDF_for_Manifest)


    cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
    cargo_grid.array_builder()
    cargo_grid.print()

    # system can make its own textfile. just need to pass in the name you want the text file to have and it will create a new text file
    cargo_grid.output_manifest("newFile.txt")
