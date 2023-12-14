import re


def extract_name(line):
    match = re.search(r'Move (.+?) from', line)
    return match.group(1) if match else None

def extract_times(lines):
    times = []
    previous_time = 0
    
    for line in lines:
        match = re.search(r'Time: (\d+) minutes', line)
        if match:
            cumulative_time = int(match.group(1))
            current_time = cumulative_time - previous_time
            times.append(current_time)
            previous_time = cumulative_time


    remaining_times = []

    currentRemainingTime = 0
    for i in range(len(times)-1, -1, -1):

        timeOfCurrentMove = times[i]

        currentRemainingTime += timeOfCurrentMove

        remaining_times.insert(0,currentRemainingTime)



    return times, remaining_times



def extract_first_coordinate(line):
    match = re.search(r'from (\w+|\(\d+,\d+\))', line)
    if match:
        coord = match.group(1)
        if coord.lower() == "truck":
            return [0,0]
        else:
            return [int(c) for c in coord.strip("()").split(',')]
    return None

# Function to extract the second coordinate
def extract_second_coordinate(line):
    match = re.search(r'to (\w+|\(\d+,\d+\))', line)
    if match:
        coord = match.group(1)
        if coord.lower() == "truck":
            return [0,0]
        else:
            return [int(c) for c in coord.strip("()").split(',')]
    return None



if __name__ == "__main__":
    # text_lines = ["Move Cat from (2,1) to truck, Time: 9 minutes" , "Move Doe from truck can to (9,2), Time: 29 minutes"]
    # extracted_first_coordinates = [extract_first_coordinate(line) for line in text_lines if "Move" in line]
    # extracted_second_coordinates = [extract_second_coordinate(line) for line in text_lines if "Move" in line]

    # print(extracted_first_coordinates)
    # print(extracted_second_coordinates)


    # text_line = "Move Cat Parts yay from (2,1) to truck, Time: 9 minutes"

    # print(extract_name(text_line))

    text_lines = ["Move Cat from (2,1) to truck, Time: 9 minutes",
                    "Move Doe from (2,2) to truck, Time: 29 minutes",
                    "Move Ewe from (1,1) to truck, Time: 49 minutes",
                    "Move Cow from (1,2) to truck, Time: 71 minutes",
                    "Move Dog from (1,3) to truck, Time: 95 minutes",
                    "Move Rat from (1,4) to truck, Time: 121 minutes"]

    times, times_remaining = extract_times(text_lines)

    print(times_remaining)