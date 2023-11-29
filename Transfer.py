from CargoGrid import Cargo_Grid
from CargoGrid import Cargo
import pandas as pd
import copy


class Transfer:

    UnloadList = []  # contains cargo that needs to be unloaded
    ShipGoal = [1, 13]
    TruckLoadList = []  # contains load list

    def __init__(self, CargoGrid, loadFile, unloadFile):
        self.CargoGrid = CargoGrid
        LoadHeaders = ['Cargo']
        self.LoadDF = pd.read_csv(
            loadFile, sep=',', names=LoadHeaders, engine='python')
        UnloadHeaders = ['Position']
        self.UnloadDF = pd.read_csv(
            unloadFile, sep=', ', names=UnloadHeaders, engine='python')

    def conversion(self):  # inputs data from manifest into class's list data members
        LoadCargo = Cargo()
        for x in (self.LoadDF['Cargo']):
            LoadCargo.name = x
            self.TruckLoadList.append(copy.deepcopy(LoadCargo))
        for x in self.UnloadDF['Position']:
            self.UnloadList.append([int(x[0]), int(x[2])])

    def CargoList(self):
        for x in range(len(self.CargoGrid.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.CargoGrid.cargo_grid[x])):
                if (y == 0):
                    continue
                if (self.CargoGrid.cargo_grid[x][y].name != "NAN" and self.CargoGrid.cargo_grid[x][y].name != "UNUSED"):
                    self.cargoList.append(self.CargoGrid.cargo_grid[x][y])


manifest = "ShipCase2.txt"
headers = ['Position', 'Weight', 'Cargo']
pandasDF_for_Manifest = pd.read_csv(
    manifest, sep=', ', names=headers, engine='python')
cargoGrid = Cargo_Grid(pandasDF_for_Manifest)
cargoGrid.array_builder()
file1 = "initialTruckContainerNames.txt"
file2 = "initialUnloadPositions.txt"
transfer = Transfer(cargoGrid, file1, file2)
print(transfer.LoadDF)
print(transfer.UnloadDF)

transfer.conversion()
print(transfer.UnloadList)
for x in transfer.TruckLoadList:
    print(x.name)
