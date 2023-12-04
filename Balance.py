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

    def CargoList(self):
        for x in range(len(self.CargoGrid.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.CargoGrid.cargo_grid[x])):
                if (y == 0):
                    continue
                if (self.CargoGrid.cargo_grid[x][y].name != "NAN" and self.CargoGrid.cargo_grid[x][y].name != "UNUSED"):
                    self.cargoList.append(copy.deepcopy(
                        self.CargoGrid.cargo_grid[x][y]))

    def Balance(self, filename):
        i = 0  # keeps track of what move we are on
        if not self.CargoGrid.Balance_Check():
            balanced = False
            output = ""

            # outputs manifest of initial state
            self.CargoGrid.output_progression(i)
            self.CargoList()
            while not balanced:
                i += 1
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
                # outputs manifest of each move
                self.CargoGrid.output_progression(i)
                output += f"Move {self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name} from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])})\n"

                if self.CargoGrid.Balance_Check():
                    with open(filename, "w") as file:
                        file.write(output)
                    self.cargoList.clear()
                    self.nodeList.clear()
                    balanced = True

        else:  # already balanced
            return  # not sure what to do if its already balanced


"""
manifest = "ShipCase2.txt"
headers = ['Position', 'Weight', 'Cargo']
pandasDF_for_Manifest = pd.read_csv(
    manifest, sep=', ', names=headers, engine='python')
cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
cargo_grid.array_builder()
balance = Balance(cargo_grid)
balance.Balance("Balance.txt")
"""
