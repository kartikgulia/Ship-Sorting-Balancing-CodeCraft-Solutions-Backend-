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

# # Usage
# file_path = './ManifestInformation/Balance.txt'
# movement_list = parse_balance_file(file_path)
# print(movement_list)


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