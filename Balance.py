from CargoGrid import Cargo
from CargoGrid import Cargo_Grid
import copy
import pandas as pd

from manifestAccess import getManifestName
# TODO: sift, writing to log, operations list, animation.


class Balance:
    # starboardMass = 0
    # portSideMass = 0
    cargoList = []  # list of containers on the heavier side
    nodeList = []  # list of states in search tree
    # might be able to use this for animation. stores the path of states to reach output
    ProgressionList = []
    # portSideList = []
    # starBoardList = []

    def __init__(self, CargoGrid):  # initial state
        # cargo grid object should have already read in manifest and called array_builder
        self.CargoGrid = CargoGrid

    def CargoList(self):
        for x in range(len(self.CargoGrid.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.CargoGrid.cargo_grid[x])):
                if (y == 0):
                    continue
                """
                if (y < 7):
                    if (self.CargoGrid.cargo_grid[x][y].name != "NAN" and self.CargoGrid.cargo_grid[x][y].name != "UNUSED"):
                        self.portSideList.append(
                            self.CargoGrid.cargo_grid[x][y])
                if (y > 6):
                    if (self.CargoGrid.cargo_grid[x][y].name != "NAN" and self.CargoGrid.cargo_grid[x][y].name != "UNUSED"):
                        self.starBoardList.append(
                            self.CargoGrid.cargo_grid[x][y])
                """
                if (self.CargoGrid.cargo_grid[x][y].name != "NAN" and self.CargoGrid.cargo_grid[x][y].name != "UNUSED"):
                    self.cargoList.append(self.CargoGrid.cargo_grid[x][y])

    # want to get lowest position we can place cargo in for a given column

    """

    def lowestPosition(self, CargoGrid, column):
        if (CargoGrid.cargo_grid[1][column].name == "UNUSED"):
            return [1, column]
        cargo_column = [row[column] for row in CargoGrid.cargo_grid]
        for x in range(1, len(cargo_column)):
            if (cargo_column[x].name == "UNUSED"):
                return CargoGrid.cargo_grid[x][column].position
    """

    def Balance(self, filename):
        # start = 0
        # stop = 0

        if (self.CargoGrid.Balance_Check() == False):
            balanced = False
            with open(filename, "w") as file:
                pass
                output = ""
            self.ProgressionList.append(self.CargoGrid.cargo_grid)
            # if ship container is unbalanced, make a list of all containers
            self.CargoList()
            while (balanced == False):
                # cargo we put crane over. goes from top row to bottom row, right to left
                for cargo in reversed(self.cargoList):
                    for column in range(1, 13):  # column we drop cargo off at
                        cargoNode = Cargo_Grid(
                            self.CargoGrid.pandasDF_for_Manifest)
                        cargoNode.Grid_Copy(self.CargoGrid)
                        cargoNode.change_pos(
                            cargo.position, self.CargoGrid.lowestPosition(column))
                        self.nodeList.append(cargoNode)
                self.nodeList = sorted(
                    # sort node list by how large weight ratio is
                    self.nodeList, reverse=True, key=lambda x: x.Weight_Ratio)
                self.CargoGrid.Grid_Copy(  # set cargo grid to grid wth largest weight ratio
                    self.nodeList[0])

                output += f"Move cargo from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({
                    str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])})\n"
                self.ProgressionList.append(
                    self.nodeList[0])
                # check if new cargo grid is balanced
                if (self.CargoGrid.Balance_Check() == True):
                    with open(filename, "w") as file:  # output operations list
                        file.write(output)
                    balanced = True

        else:  # already balanced
            return  # not sure what to do if its already balanced


# manifest = f"./ManifestInformation/{getManifestName()}"
# headers = ['Position', 'Weight', 'Cargo']
# pandasDF_for_Manifest = pd.read_csv(
#     manifest, sep=', ', names=headers, engine='python')
# cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
# cargo_grid.array_builder()
# cargo_grid.print()
# balance = Balance(cargo_grid)
# balance.Balance("Balance.txt")
# balance.CargoGrid.print()


"""
for cargo in reversed(balance.cargoList):
    print(cargo.position)
    for column in range(1, 3):  # column we drop cargo off at
        cargoNode = copy.deepcopy(balance.CargoGrid)
        cargoNode.print()
        cargoNode.change_pos(
            cargo.position, balance.CargoGrid.lowestPosition(column))
        balance.nodeList.append(copy.deepcopy(cargoNode))
    balance.nodeList = sorted(
        balance.nodeList, reverse=True, key=lambda x: x.Weight_Ratio)

balance.nodeList[1].print()
print(str(balance.CargoGrid.Weight_Ratio))

cargo = balance.cargoList[0]
for column in range(1, 3):
    balance.nodeList.append(copy.deepcopy(balance.CargoGrid))
    # balance.nodeList[len(balance.nodeList) - 1].change_pos(cargo.position,
    # balance.CargoGrid.lowestPosition(column))
    print(str(column))
balance.nodeList[0].portSideMass = 4
# balance.nodeList[0].print()
# print(str(balance.nodeList[0].portSideMass) +
# str(balance.CargoGrid.portSideMass))
# balance.nodeList[1].print()
balance.CargoGrid.print()
"""

"""
for cargo in reversed(balance.cargoList):
    for column in range(1, 3):
        cargoGridCopy = Cargo_Grid(pandasDF_for_Manifest)
        # cargoGridCopy.initial_array()
        cargoGridCopy.Grid_Copy(cargo_grid)
        cargoGridCopy.print()
        cargoGridCopy.change_pos(cargo.position,
                                 balance.CargoGrid.lowestPosition(7))
        balance.nodeList.append(cargoGridCopy)

# cargoGridCopy.print()
cargo_grid.print()

# balance.nodeList[0].print()
cargo_grid.Grid_Copy(balance.nodeList[0])
cargo_grid.print()
"""
