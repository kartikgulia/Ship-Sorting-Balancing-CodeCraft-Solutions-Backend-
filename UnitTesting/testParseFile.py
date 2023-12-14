from testExtraction import extract_first_coordinate
from testExtraction import extract_second_coordinate
from testExtraction import extract_name, extract_times

# 0,0 represents truck
# Should return the list of moveCoordinates. ex: [[[2, 1], [0, 0]], [[2, 2], [0, 0]], [[1, 1], [0, 0]], [[1, 2], [0, 0]], [[1, 3], [0, 0]], [[1, 4], [0, 0]]]
# Should return the


def parse_file(file_path):

    moveCoordinates = []
    names = []
    with open(file_path, 'r') as file:

        for line in file:
            first_coordinate = extract_first_coordinate(line)
            second_coordinate = extract_second_coordinate(line)

            moveCoordinates.append([first_coordinate, second_coordinate])

            eachName = extract_name(line)

            names.append(eachName)

    with open(file_path, 'r') as file:
        times, times_remaining = extract_times(file)

    return moveCoordinates, names, times, times_remaining


moveCoords, names, times, times_remaining = parse_file(
    r"/Users/rayyanzaid/Desktop/Ship-Sorting-Balancing-CodeCraft-Solutions-Backend-/Transfer.txt")

print(len(moveCoords))
print(len(names))
print(len(times))
