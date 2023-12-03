from CargoGrid import Cargo_Grid
from CargoGrid import Cargo
import pandas as pd
import copy


class Transfer:

    UnloadList = []  # contains cargo that needs to be unloaded
    LoadList = []  # contains cargo getting loaded.
    # cargoList = []  # list of containers
    # nodeList = []  # list of states

    def __init__(self, CargoGrid, loadFile, unloadFile):
        self.CargoGrid = CargoGrid

        LoadHeaders = ['Cargo']
        self.LoadDF = pd.read_csv(
            loadFile, sep=',', names=LoadHeaders, engine='python')

        UnloadHeaders = ['Position']
        self.UnloadDF = pd.read_csv(
            unloadFile, sep=', ', names=UnloadHeaders, engine='python')

        self.conversion()

    def conversion(self):  # inputs data into class's list data members
        LoadCargo = Cargo()

        for x in (self.LoadDF['Cargo']):
            LoadCargo.name = x
            self.LoadList.append(copy.deepcopy(LoadCargo))

        for p in self.UnloadDF['Position']:
            x = int(p[0])
            y = int(p[2])
            self.UnloadList.append(copy.deepcopy(
                self.CargoGrid.cargo_grid[x][y]))
            # self.UnloadList.append(self.CargoGrid.cargo_grid[x][y])

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

    """
    def setGoals(self):
        totalGoals = 0
        for cargo in self.UnloadList:
            x = cargo.position[0]
            y = cargo.position[1]
            if (self.CargoGrid.cargo_grid[x+1][y].name == "UNUSED"):
                cargo.Goal = 1
            totalGoals += cargo.Goal
            cargo.GoalDistance = abs(9-x) + abs(1 - y)
        self.CargoGrid.totalGoals = totalGoals
    """

    # removes cargo from ship and places it on truck. also finds manhattan distance.
    def Unload(self, unloadCargo):
        x = unloadCargo.position[0]
        y = unloadCargo.position[1]
        if (self.CargoGrid.cargo_grid[x+1][y].name == 'UNUSED'):
            # goal is (9,1) + 2 minutes from ship to truck
            self.CargoGrid.Manhattan_Dist += abs(9 - x) + \
                abs(1 - y) + 2
            self.CargoGrid.cargo_grid[x][y].name = 'UNUSED'
            self.CargoGrid.cargo_grid[x][y].weight = 0

            self.CargoGrid.old_pos = [x, y]
            self.CargoGrid.new_pos = "Truck"
            """
            i = 0
            for cargo in self.cargoList:
                if cargo.position == unloadCargo.position:
                    self.cargoList.pop(i)
                i += 1
            """

    def Load(self, loadedCargo, position):  # loads cargo onto ship
        x = position[0]
        y = position[1]
        self.CargoGrid.cargo_grid[x][y].name = loadedCargo.name
        self.CargoGrid.cargo_grid[x][y].weight = loadedCargo.weight
        # initial position is (9,1) + 2 minutes from truck to ship
        self.CargoGrid.Manhattan_Dist += abs(9 - x) + \
            abs(1 - y) + 2
        self.CargoGrid.old_pos = "Truck"
        self.CargoGrid.new_pos = position

    def Transfer(self, filename):
        i = 0
        if (len(self.UnloadList) != 0 or len(self.LoadList) != 0):
            transfer = False
            output = ""
            self.CargoGrid.output_progression(i)
            self.UnloadList = sorted(
                self.UnloadList, key=lambda x: x.GoalDistance)

            while not transfer:
                i += 1
                if len(self.UnloadList) > 0:  # unload
                    j = 0
                    for cargo in self.UnloadList:
                        if self.CargoGrid.cargo_grid[cargo.position[0] + 1][cargo.position[1]].name != "UNUSED":
                            blockingCargo = self.CargoGrid.cargo_grid[cargo.position[0] +
                                                                      1][cargo.position[1]]
                            self.CargoGrid.change_pos(blockingCargo.position, self.CargoGrid.lowestPosition(
                                blockingCargo.position[1] + 1))  # move to right
                            self.CargoGrid.output_progression(i)
                            output += f"Move cargo from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])})\n"

                        i += 1
                        self.Unload(cargo)
                        self.UnloadList.pop(j)
                        output += f"Move cargo from ({str(self.CargoGrid.old_pos[0])},{str(self.CargoGrid.old_pos[1])}) to truck\n"
                        self.CargoGrid.output_progression(i)
                        j += 1
                        break

                if len(self.LoadList) > 0:  # load
                    loadedCargo = self.LoadList.pop(0)
                    for column in range(1, 13):
                        if (self.CargoGrid.cargo_grid[8][column].name == "UNUSED"):
                            self.Load(
                                loadedCargo, self.CargoGrid.lowestPosition(column))
                            break
                    self.CargoGrid.output_progression(i)
                    output += f"Move cargo from truck to ({str(self.CargoGrid.new_pos[0])},{str(self.CargoGrid.new_pos[1])})\n"

                if (len(self.UnloadList) == 0 and len(self.LoadList) == 0):
                    with open(filename, "w") as file:
                        file.write(output)
                    transfer = True
        else:
            return
