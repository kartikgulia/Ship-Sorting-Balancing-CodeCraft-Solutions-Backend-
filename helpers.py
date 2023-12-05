import os
import pandas as pd

from CargoGrid import Cargo_Grid
from Transfer import Transfer
from manifestAccess import getManifestName
# Functions from other files




from Balance import Balance
from Transfer import Transfer
def parse_balance_file(file_path):
    movements = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            from_coords = [int(coord)
                           for coord in parts[3].strip('()').split(',')]
            to_coords = [int(coord)
                         for coord in parts[5].strip('()').split(',')]
            movements.append([from_coords, to_coords])
    return movements

def parse_transfer_file(file_path):
    movements = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            
            # Process from_coords
            from_coord_parts = parts[3].strip('()').split(',')
            from_coords = [0, 0] if from_coord_parts[0] == "truck" else [int(coord) for coord in from_coord_parts]

            # Process to_coords
            to_coord_parts = parts[5].strip('()').split(',')
            to_coords = [0, 0] if to_coord_parts[0] == "truck" else [int(coord) for coord in to_coord_parts]

            movements.append([from_coords, to_coords])
    return movements

# # Usage
# file_path = './ManifestInformation/Balance.txt'
# movement_list = parse_balance_file(file_path)
# print(movement_list)

def updateWeightInFile(row,col,stringWeight,file_path):

    

    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the specific line
    for i, line in enumerate(lines):
        if line.startswith(f"[{row:02d},{col:02d}]"):
            parts = line.split('}')
            first_part = parts[0].split('{')[0]
            second_part = parts[1]
            # Reconstruct the line, preserving its original end character
            lines[i] = f"{first_part}{{{stringWeight}}}{second_part}"
            if not lines[i].endswith('\n') and i < len(lines) - 1:
                lines[i] += '\n'

    # Write the changes back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)


def performTransfer():
    manifestName = getManifestName()
    manifestNamePath = f"ManifestInformation/{manifestName}"
    
    headers = ['Position', 'Weight', 'Cargo']
    pandasDF_for_Manifest = pd.read_csv(
        manifestNamePath, sep=', ', names=headers, engine='python')
    cargoGrid = Cargo_Grid(pandasDF_for_Manifest)
    cargoGrid.array_builder()
    file1 = "TransferInformation/initialTruckContainerNames.txt"
    file2 = "TransferInformation/initialUnloadPositions.txt"
    transfer = Transfer(cargoGrid, file1, file2)
    transfer.Transfer("ManifestInformation/Transfer.txt")
# def getWeightInFile(row, col, file_path):
#     try:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
            
#             # Formatting row and col to match the file's format
#             row_str = f"{row:02d}" 
#             col_str = f"{col:02d}"  

#             # Searching for the correct line
#             for line in lines:
#                 if line.startswith(f"[{row_str},{col_str}]"):
#                     # Extracting the weight
#                     start = line.find('{') + 1
#                     end = line.find('}')
#                     return line[start:end]
            
#             return "Not found"  # Return this if the specified row and col are not found
#     except FileNotFoundError:
#         return "File not found"
#     except Exception as e:
#         return str(e)  # General error handling


    

        
def get_last_txt_file_name(folder_path):
    """
    This function takes a folder path and returns the name of the last txt file in that folder,
    with the .txt extension removed.
    """
    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        return "Folder not found"

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out only txt files
    txt_files = [file for file in files]

    # Sort the files to find the last one
    txt_files.sort()

    # Get the last txt file, if there is any
    if txt_files:
        last_txt_file = txt_files[-1]
        # Remove the .txt extension and return
        return os.path.splitext(last_txt_file)[0]
    else:
        return "No txt files found in the folder"