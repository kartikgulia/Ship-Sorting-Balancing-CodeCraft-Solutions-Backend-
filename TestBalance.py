from Balance import Balance
from CargoGrid import Cargo_Grid
import pandas as pd


# testing Balance
# manifest = "ShipCase1.txt"
# manifest = "ShipCase2.txt"
# manifest = "ShipCase3.txt"
# manifest = "TransferTestCase.txt"
manifest = "SIFTCase.txt"


headers = ['Position', 'Weight', 'Cargo']
pandasDF_for_Manifest = pd.read_csv(
    manifest, sep=', ', names=headers, engine='python')
cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
cargo_grid.array_builder()
balance = Balance(cargo_grid)
balance.Balance("Balance.txt")

"""
# testing SIFT
manifest = "SIFTCase.txt"
headers = ['Position', 'Weight', 'Cargo']
pandasDF_for_Manifest = pd.read_csv(
    manifest, sep=', ', names=headers, engine='python')
cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
cargo_grid.array_builder()
balance = Balance(cargo_grid)

# testing SIFT function only
# balance.SIFT("SIFTSolution.txt")

# testing SIFT function integrated with balance
balance.Balance("SIFTSolution.txt")
"""
