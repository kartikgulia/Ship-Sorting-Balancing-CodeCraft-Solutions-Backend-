from typing import List, Dict, Any
import pandas as pd

from CargoGrid import Cargo_Grid
import os

pathToManifestNameTextFile = "ManifestInformation/manifestName.txt"


def getManifestName():
    if os.path.exists(pathToManifestNameTextFile):
        with open(pathToManifestNameTextFile, 'r') as name_file:
            old_manifest_name = name_file.read().strip()

    return old_manifest_name


def getManifestGridHelper(manifest_path):
    headers = ['Position', 'Weight', 'Cargo']
    pandasDF_for_Manifest = pd.read_csv(
        f'{manifest_path}', sep=', ', names=headers, engine='python')

    # Initialize and populate the Cargo_Grid
    cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
    cargo_grid.array_builder()

    # Convert the Cargo_Grid to a JSON-serializable format
    grid_data = [{}] * 8
    for i in range(8):
        grid_data[i] = [{}] * 12

    for eachRow in range(len(cargo_grid.cargo_grid)):
        for eachCol in range(len(cargo_grid.cargo_grid[eachRow])):

            cargo = cargo_grid.cargo_grid[eachRow][eachCol]

            position = cargo.position
            # print(position)

            if position == [0, 0]:
                continue

            rowNum = 8 - position[0]
            colNum = position[1] - 1

            grid_data[rowNum][colNum] = {
                "position": cargo.position,
                "name": cargo.name,
                "weight": cargo.weight
            }

    return grid_data


