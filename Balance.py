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
        self.CargoList()

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

    def SIFT(self, filename):
        output = ""
        sortedCargoList = []

        for cargo in self.cargoList:
            sortedCargoList.append(copy.deepcopy(cargo))

        sortedCargoList = sorted(
            sortedCargoList, reverse=True, key=lambda x: x.weight)

        if sortedCargoList[len(sortedCargoList) - 1].weight / sortedCargoList[0].weight <= 0.05:

            if (len(self.cargoList) == 1):
                self.CargoGrid.output_progression(0)
                self.CargoGrid.change_pos(self.cargoList[0].position, [1, 6])
                output += f"Move {self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name} from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])}), Time: {str(self.CargoGrid.Manhattan_Dist)} minutes\n"
                self.CargoGrid.output_progression(1)

            elif (len(self.cargoList) == 2):
                weight1 = self.cargoList[0].weight
                weight2 = self.cargoList[1].weight

                if (min(weight1, weight2) / max(weight1, weight2) < 0.9):

                    self.CargoGrid.output_progression(0)

                    if weight1 >= weight2:
                        HeavyPos = self.cargoList[0].position
                        LighterPos = self.cargoList[1].position

                    else:
                        HeavyPos = self.cargoList[1].position
                        LighterPos = self.cargoList[0].position

                    self.CargoGrid.change_pos(
                        LighterPos, [1, 7])
                    self.CargoGrid.output_progression(1)
                    output += f"Move {self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name} from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])}), Time: {str(self.CargoGrid.Manhattan_Dist)} minutes\n"
                    self.CargoGrid.change_pos(
                        HeavyPos.position, [1, 6])
                    self.CargoGrid.output_progression(2)
                    output += f"Move {self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name} from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])}), Time: {str(self.CargoGrid.Manhattan_Dist)} minutes\n"

            else:
                i = 1
                row = 1
                leftColumn = 5
                rightColumn = 7
                start = True
                for cargo in sortedCargoList:
                    if start == True:
                        cargo.position = [row, 6]
                        start = False
                        i += 1
                    elif i % 2 == 0:
                        cargo.position = [row, rightColumn]
                        rightColumn += 1
                        i += 1
                    elif i % 2 != 0:
                        cargo.position = [row, leftColumn]
                        leftColumn -= 1
                        i += 1
                    if rightColumn == 12 and leftColumn == 1:
                        row += 1
                        leftColumn = 5
                        rightColumn = 7
                        start = True

                self.CargoGrid.output_progression(0)
                j = 1
                for cargo in reversed(self.cargoList):
                    self.CargoGrid.change_pos(
                        cargo.position, self.CargoGrid.lowestPosition(1))
                    cargo.position = self.CargoGrid.new_pos
                    output += f"Move {self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name} from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])}), Time: {str(self.CargoGrid.Manhattan_Dist)} minutes\n"
                    self.CargoGrid.output_progression(j)
                    j += 1

                for cargo in (self.cargoList):
                    for container in sortedCargoList:
                        if cargo.name == container.name:
                            self.CargoGrid.change_pos(
                                cargo.position, container.position)
                            output += f"Move {self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name} from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])}), Time: {str(self.CargoGrid.Manhattan_Dist)} minutes\n"
                            self.CargoGrid.output_progression(j)
                            j += 1

            with open(filename, "w") as file:
                file.write(output)
                self.cargoList.clear()
                sortedCargoList.clear()
            return 1

        else:
            sortedCargoList.clear()
            return 0

    def Balance(self, filename):
        i = 0  # keeps track of what move we are on
        if not self.CargoGrid.Balance_Check():

            sift = self.SIFT(filename)
            if sift == True:
                return

            balanced = False
            output = ""

            # outputs manifest of initial state
            self.CargoGrid.output_progression(i)
            # self.CargoList()
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

                # self.nodeList = sorted(
                    # self.nodeList, reverse=True, key=lambda x: x.Weight_Ratio)  # sort node list by how large weight ratio is
                self.nodeList = sorted(
                    self.nodeList, reverse=True, key=lambda x: (x.Weight_Ratio, -x.Manhattan_Dist))  # sort node list by how large weight ratio is
                self.CargoGrid.Grid_Copy(  # set cargo grid to grid wth largest weight ratio
                    self.nodeList.pop(0))
                # outputs manifest of each move
                self.CargoGrid.output_progression(i)
                output += f"Move {self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name} from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])}), Time: {str(self.CargoGrid.Manhattan_Dist)} minutes\n"

                if self.CargoGrid.Balance_Check():
                    with open(filename, "w") as file:
                        file.write(output)
                    self.cargoList.clear()
                    self.nodeList.clear()
                    balanced = True

        else:
            return
