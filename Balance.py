from CargoGrid import Cargo
from CargoGrid import Cargo_Grid
import copy
import pandas as pd
from manifestAccess import getManifestName


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

        # if length id 1, move to middle
        if (len(self.cargoList) == 1):
            self.CargoGrid.output_progression(0)
            self.CargoGrid.change_pos(self.cargoList[0].position, [1, 6])
            output += "Move " + self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name + " from (" + str(self.CargoGrid.old_pos[0]) + "," + str(
                self.CargoGrid.old_pos[1]) + ") to (" + str(self.CargoGrid.new_pos[0]) + "," + str(self.CargoGrid.new_pos[1]) + "), Time: " + str(self.CargoGrid.Manhattan_Dist) + " minutes\n"
            self.CargoGrid.output_progression(1)

        # if length is two, move heavier container to middle and lighter to the right
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
                output += "Move " + self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name + " from (" + str(self.CargoGrid.old_pos[0]) + "," + str(
                    self.CargoGrid.old_pos[1]) + ") to (" + str(self.CargoGrid.new_pos[0]) + "," + str(self.CargoGrid.new_pos[1]) + "), Time: " + str(self.CargoGrid.Manhattan_Dist) + " minutes\n"
                self.CargoGrid.change_pos(
                    HeavyPos.position, [1, 6])
                self.CargoGrid.output_progression(2)
                output += "Move " + self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name + " from (" + str(self.CargoGrid.old_pos[0]) + "," + str(
                    self.CargoGrid.old_pos[1]) + ") to (" + str(self.CargoGrid.new_pos[0]) + "," + str(self.CargoGrid.new_pos[1]) + "), Time: " + str(self.CargoGrid.Manhattan_Dist) + " minutes\n"

        else:
            # move all containers to one column
            self.CargoGrid.output_progression(0)
            j = 1
            k = 1
            for cargo in reversed(self.cargoList):
                highestPos = self.CargoGrid.highestContainer(k)
                if (highestPos is not None):
                    if (highestPos[0] == 8):
                        k += 1
                self.CargoGrid.change_pos(
                    cargo.position, self.CargoGrid.lowestPosition(k))
                cargo.position = self.CargoGrid.new_pos
                output += "Move " + self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name + " from (" + str(self.CargoGrid.old_pos[0]) + "," + str(
                    self.CargoGrid.old_pos[1]) + ") to (" + str(self.CargoGrid.new_pos[0]) + "," + str(self.CargoGrid.new_pos[1]) + "), Time: " + str(self.CargoGrid.Manhattan_Dist) + " minutes\n"
                self.CargoGrid.output_progression(j)
                j += 1

            # assign goal positions for each container based on SIFT
            lowestRow = self.CargoGrid.lowestPosition(6)
            row = lowestRow[0]
            leftColumn = 5
            rightColumn = 7
            i = 1
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

            # move each container to their goal position
            self.cargoList.clear()
            self.CargoList()
            for cargo in reversed(self.cargoList):
                for container in sortedCargoList:
                    if cargo.name == container.name:
                        self.CargoGrid.change_pos(
                            cargo.position, container.position)
                        output += "Move " + self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name + " from (" + str(self.CargoGrid.old_pos[0]) + "," + str(
                            self.CargoGrid.old_pos[1]) + ") to (" + str(self.CargoGrid.new_pos[0]) + "," + str(self.CargoGrid.new_pos[1]) + "), Time: " + str(self.CargoGrid.Manhattan_Dist) + " minutes\n"
                        self.CargoGrid.output_progression(j)
                        j += 1
                        break

        with open(filename, "w") as file:
            file.write(output)
            self.cargoList.clear()
            sortedCargoList.clear()

    def Balance(self, filename):
        i = 0  # keeps track of what move we are on
        prevWeightRatio = 0
        initialGrid = Cargo_Grid(self.CargoGrid.pandasDF_for_Manifest)
        initialGrid.Grid_Copy(self.CargoGrid)

        if not self.CargoGrid.Balance_Check():

            balanced = False
            output = ""

            # outputs manifest of initial state
            self.CargoGrid.output_progression(i)

            while not balanced:
                i += 1
                for cargo in reversed(self.cargoList):
                    for column in range(1, 13):  # column we drop cargo off at
                        if (column == cargo.position[1]):
                            continue
                        cargoNode = Cargo_Grid(
                            self.CargoGrid.pandasDF_for_Manifest)
                        cargoNode.Grid_Copy(self.CargoGrid)
                        cargoNode.change_pos(
                            cargo.position, self.CargoGrid.lowestPosition(column))
                        self.nodeList.append(cargoNode)

                # self.nodeList = sorted(
                    # self.nodeList, reverse=True, key=lambda x: x.Weight_Ratio)

                # sort node list by how large weight ratio is and how low cost is
                self.nodeList = sorted(self.nodeList, reverse=True, key=lambda x: (
                    x.Weight_Ratio, -x.Manhattan_Dist))

                # set cargo grid to grid wth largest weight ratio with lowest cost
                self.CargoGrid.Grid_Copy(self.nodeList.pop(0))

                # if weight ratio doesn't change between iterations, go to SIFT
                if (self.CargoGrid.Weight_Ratio == prevWeightRatio):
                    self.CargoGrid.Grid_Copy(initialGrid)
                    self.cargoList.clear()
                    self.CargoList()
                    self.SIFT(filename)
                    return
                else:
                    prevWeightRatio = copy.deepcopy(
                        self.CargoGrid.Weight_Ratio)

                # outputs manifest of each move
                self.CargoGrid.output_progression(i)

                output += "Move " + self.CargoGrid.cargo_grid[self.CargoGrid.new_pos[0]][self.CargoGrid.new_pos[1]].name + " from (" + str(self.CargoGrid.old_pos[0]) + "," + str(
                    self.CargoGrid.old_pos[1]) + ") to (" + str(self.CargoGrid.new_pos[0]) + "," + str(self.CargoGrid.new_pos[1]) + "), Time: " + str(self.CargoGrid.Manhattan_Dist) + " minutes\n"

                if self.CargoGrid.Balance_Check():
                    with open(filename, "w") as file:
                        file.write(output)
                    self.cargoList.clear()
                    self.nodeList.clear()
                    balanced = True

                self.cargoList.clear()
                self.CargoList()

        else:
            return
