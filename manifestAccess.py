from typing import List, Dict, Any
import pandas as pd

from CargoGrid import Cargo_Grid


def getManifestName():
    print()


def getManifestGridHelper(manifest_name) -> List[Dict[str, Any]]:
    headers = ['Position', 'Weight', 'Cargo']
    pandasDF_for_Manifest = pd.read_csv(
        f'./ManifestInformation/{manifest_name}', sep=', ', names=headers, engine='python')

    # Initialize and populate the Cargo_Grid
    cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
    cargo_grid.array_builder()

    # Convert the Cargo_Grid to a JSON-serializable format
    grid_data = []
    for x in range(len(cargo_grid.cargo_grid)):
        for y in range(len(cargo_grid.cargo_grid[x])):
            cargo = cargo_grid.cargo_grid[x][y]
            grid_data.append({
                "position": cargo.position,
                "weight": cargo.weight,
                "name": cargo.name
            })

    return grid_data
