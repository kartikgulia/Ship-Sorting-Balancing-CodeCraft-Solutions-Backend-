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
