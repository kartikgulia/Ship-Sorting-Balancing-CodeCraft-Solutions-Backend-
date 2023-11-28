import pandas as pd
import numpy as np
import matplotlib as plt
import copy


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
    # buffer = [[Cargo] * 25 for _ in range(5)]
    Manhattan_Dist = 0

    old_pos = [0, 0]  # use for operations list
    new_pos = [0, 0]  # use for operations list

    starboardMass = 0
    portSideMass = 0
    Weight_Ratio = 0

    def __init__(self, pandasDF_for_Manifest):
        self.pandasDF_for_Manifest = pandasDF_for_Manifest

    def __getitem__(self, index):
        if isinstance(index, tuple):
            x, y = index
            return self.cargo_grid[x][y]
        elif isinstance(index, int):
            x = index
            return self.cargo_grid[x]
        elif index is None:
            return self.cargo_grid

    def initial_array(self):  # sets all positions for grid and buffer

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
        """
        i = 0
        for x in range(len(self.buffer)):
            if (x == 0):
                continue
            for y in range(len(self.buffer[x])):
                if (y == 0):
                    continue
                self.buffer[x][y] = Cargo()
                self.buffer[x][y].position = [x, y]
                i += 1
        """

    def array_builder(self):
        self.initial_array()
        for x in range(len(self.pandasDF_for_Manifest)):
            position_weight = conversion(
                self.pandasDF_for_Manifest.at[x, 'Position'],  self.pandasDF_for_Manifest.at[x, 'Weight'])
            pos = position_weight[0]
            self.cargo_grid[pos[0]][pos[1]
                                    ].name = self.pandasDF_for_Manifest.at[x, 'Cargo']
            self.cargo_grid[pos[0]][pos[1]].position = pos
            self.cargo_grid[pos[0]][pos[1]].weight = position_weight[1]

        self.Weight_Calc()  # get weights for starboard and portside

    def Grid_Copy(self, grid):
        """
        for x in range(len(grid.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(grid.cargo_grid[x])):
                if (y == 0):
                    continue

                self.cargo_grid[x][y].name = copy.deepcopy(grid.cargo_grid[x][y].name)
                self.cargo_grid[x][y].position = copy.deegrid.cargo_grid[x][y].position
                self.cargo_grid[x][y].weight = grid.cargo_grid[x][y].weight

                self.cargo_grid[x][y] = copy.deepcopy(grid.cargo_grid[x][y])
        """
        self.cargo_grid = copy.deepcopy(grid.cargo_grid)
        self.Manhattan_Dist = grid.Manhattan_Dist
        self.portSideMass = grid.portSideMass
        self.starboardMass = grid.starboardMass
        self.Weight_Ratio = grid.Weight_Ratio
        self.old_pos = grid.old_pos
        self.new_pos = grid.new_pos

    def Weight_Calc(self):  # sets weights for starboard and portside
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                if (y < 7):
                    self.portSideMass += self.cargo_grid[x][y].weight
                else:
                    self.starboardMass += self.cargo_grid[x][y].weight
        self.Weight_Ratio = min(self.portSideMass, self.starboardMass) / \
            max(self.starboardMass, self.portSideMass)

    def Balance_Check(self):
        # if (abs(self.starboardMass - self.portSideMass) <= (max(self.starboardMass, self.portSideMass) * 0.10)):
        if (self.Weight_Ratio > 0.9):
            return True
        else:
            return False

    # want to get lowest position we can place cargo in for a given column
    def lowestPosition(self, column):
        """
        for col in range(1, len(self.cargo_grid[0])):
            if (col == column):
                for row in range(1, len(self.cargo_grid)):
                    if (self.cargo_grid[row][col].name == "UNUSED"):
                        return [row, col]
        """
        cargo_column = [row[column] for row in self.cargo_grid]
        for x in range(1, len(cargo_column)):
            if (cargo_column[x].name == "UNUSED"):
                return cargo_column[x].position

    def valid_pos(self, old_pos, new_pos):  # makes sure move is valid
        x = new_pos[0]
        y = new_pos[1]
        # old position has a container above it
        if (self.cargo_grid[old_pos[0] + 1][old_pos[1]].name != "UNUSED"):
            return False
        # new position is already filled or is nan
        elif (self.cargo_grid[x][y].name != "UNUSED"):
            return False
        # new position has nothing beneath it to hold cargo and position below it is not the zero row or old position is beneath new position
        elif ((self.cargo_grid[x-1][y].name == "UNUSED" and (x-1 != 0)) or (y == old_pos[1] and x-1 == old_pos[0])):
            return False
        else:
            return True

    # moves cargo to new positon and find manhattan distance and weights of starboard and portside. Used with valid_pos to make transfers
    def change_pos(self, old_pos, new_pos):

        self.old_pos = old_pos
        self.new_pos = new_pos

        old_row = old_pos[0]
        old_column = old_pos[1]
        new_row = new_pos[0]
        new_column = new_pos[1]

        if (self.valid_pos(old_pos, new_pos)):

            self.Manhattan_Dist += abs(new_row - old_row) + \
                abs(new_column - old_column)

            self.cargo_grid[new_row][new_column].weight = self.cargo_grid[old_row][old_column].weight
            self.cargo_grid[new_row][new_column].name = self.cargo_grid[old_row][old_column].name
            self.cargo_grid[old_row][old_column].weight = 0
            self.cargo_grid[old_row][old_column].name = "UNUSED"

            if (new_column < 7):
                self.portSideMass += self.cargo_grid[new_row][new_column].weight
                self.starboardMass -= self.cargo_grid[new_row][new_column].weight
            else:
                self.portSideMass -= self.cargo_grid[new_row][new_column].weight
                self.starboardMass += self.cargo_grid[new_row][new_column].weight

            self.Weight_Ratio = min(self.portSideMass, self.starboardMass) / \
                max(self.starboardMass, self.portSideMass)
            # want to make a tree with multiple states for cargo grid
            # return copy.deepcopy(self)

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
    # manifest = "new1.txt"
    manifest = "ManifestChristian.txt"
    headers = ['Position', 'Weight', 'Cargo']
    pandasDF_for_Manifest = pd.read_csv(
        manifest, sep=', ', names=headers, engine='python')
    print(pandasDF_for_Manifest)

    cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
    cargo_grid.array_builder()
    # cargo_grid.print()

    # test cases
    cargo_grid.change_pos([1, 9], [2, 8])
    # print(cargo_grid.Manhattan_Dist)
    cargo_grid.change_pos([2, 8], [2, 4])
    cargo_grid.change_pos([2, 4], [2, 6])
    print(str(cargo_grid.starboardMass) +
          " " + str(cargo_grid.portSideMass))
    print(str(cargo_grid.Weight_Ratio))
    print(str(cargo_grid.lowestPosition(8)))

    # system can make its own textfile. just need to pass in the name you want the text file to have and it will create a new text file
    cargo_grid.output_manifest("newFile.txt")
