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

manifest = "ShipCase3.txt"
headers = ['Position', 'Weight', 'Cargo']
pandasDF_for_Manifest = pd.read_csv(
    manifest, sep=', ', names=headers, engine='python')
cargoGrid = Cargo_Grid(pandasDF_for_Manifest)
cargoGrid.array_builder()
file1 = "ShipCase3Load.txt"
file2 = "ShipCase3Unload.txt"
transfer = Transfer(cargoGrid, file1, file2)

transfer.Transfer("ShipCase3Result.txt")


