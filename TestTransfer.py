from Transfer import Transfer
from CargoGrid import Cargo_Grid
from CargoGrid import Cargo
import pandas as pd

"""
Testing inputs:

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
print(transfer.UnloadList)
for x in transfer.LoadList:
    print(x.name)
"""

manifest = "TransferTestCase.txt"
headers = ['Position', 'Weight', 'Cargo']
pandasDF_for_Manifest = pd.read_csv(
    manifest, sep=', ', names=headers, engine='python')
cargoGrid = Cargo_Grid(pandasDF_for_Manifest)
cargoGrid.array_builder()
file1 = "TransferTestCaseLoad.txt"
file2 = "TransferTestCaseUnload.txt"
transfer = Transfer(cargoGrid, file1, file2)

# # testing load
# # car = Cargo()
# # car.name = "Mustang"
# # transfer.Load(car, cargoGrid.lowestPosition(1))
# # transfer.CargoGrid.output_manifest("File.txt")

# # testing unload
# # transfer.Unload(transfer.CargoGrid.cargo_grid[1][4])
# # transfer.CargoGrid.output_manifest("File.txt")

# # testing transfer
transfer.Transfer("Transfer.txt")


# manifest = "ManifestInformation/ShipCase1.txt"
# headers = ['Position', 'Weight', 'Cargo']
# pandasDF_for_Manifest = pd.read_csv(
#     manifest, sep=', ', names=headers, engine='python')
# cargoGrid = Cargo_Grid(pandasDF_for_Manifest)
# cargoGrid.array_builder()
# file1 = "./TransferInformation/initialTruckContainerNames.txt"
# file2 = "./TransferInformation/initialUnloadPositions.txt"
# transfer = Transfer(cargoGrid, file1, file2)

# # testing transfer
# transfer.Transfer("ManifestInformation/Transfer.txt")
