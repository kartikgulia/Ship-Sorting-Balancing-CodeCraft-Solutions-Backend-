import os

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

def updateWeightInFile(row,col,stringWeight,moveNum):

    file_path = f"ManifestForEachMove/ManifestMove{moveNum}"

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