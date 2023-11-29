from CargoGrid import Cargo
from CargoGrid import Cargo_Grid
import copy
import pandas as pd

from manifestAccess import getManifestName
# TODO: sift, writing to log, operations list, animation.


class Balance:
    def __init__(self, CargoGrid):  # initial state
        # cargo grid object should have already read in manifest and called array_builder
        self.CargoGrid = CargoGrid
        self.cargoList = []  # list of containers
        self.nodeList = []  # list of states in search tree
        # might be able to use this for animation. stores the path of states to reach output
        self.ProgressionList = []

    def CargoList(self):
        for x in range(len(self.CargoGrid.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.CargoGrid.cargo_grid[x])):
                if (y == 0):
                    continue
                if (self.CargoGrid.cargo_grid[x][y].name != "NAN" and self.CargoGrid.cargo_grid[x][y].name != "UNUSED"):
                    self.cargoList.append(self.CargoGrid.cargo_grid[x][y])

    def Balance(self, filename):
        if not self.CargoGrid.Balance_Check():
            balanced = False
            output = ""
            # Initialize ProgressionList at the beginning of each balance operation
            self.ProgressionList.append(self.CargoGrid.cargo_grid)
            self.CargoList()
            while not balanced:
                for cargo in reversed(self.cargoList):
                    for column in range(1, 13):  # column we drop cargo off at
                        cargoNode = Cargo_Grid(
                            self.CargoGrid.pandasDF_for_Manifest)
                        cargoNode.Grid_Copy(self.CargoGrid)
                        cargoNode.change_pos(
                            cargo.position, self.CargoGrid.lowestPosition(column))
                        self.nodeList.append(cargoNode)
                self.nodeList = sorted(
                    self.nodeList, reverse=True, key=lambda x: x.Weight_Ratio)  # sort node list by how large weight ratio is
                self.CargoGrid.Grid_Copy(  # set cargo grid to grid wth largest weight ratio
                    self.nodeList[0])

                output += f"Move cargo from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])})\n"
                self.ProgressionList.append(self.nodeList[0])

                if self.CargoGrid.Balance_Check():
                    with open(filename, "w") as file:
                        file.write(output)
                    balanced = True
                    self.cargoList.clear()
                    self.nodeList.clear()
                    self.ProgressionList.clear()

        else:  # already balanced
            return  # not sure what to do if its already balanced


# manifest = "BalanceTest.txt"
# headers = ['Position', 'Weight', 'Cargo']
# pandasDF_for_Manifest = pd.read_csv(
    # manifest, sep=', ', names=headers, engine='python')
# print(pandasDF_for_Manifest)

# cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
# cargo_grid.array_builder()
# cargo_grid.print()
# balance = Balance(cargo_grid)
# balance.CargoList()
# print(balance.cargoList)
# balance.Balance("Balance.txt")
# balance.CargoGrid.print()
