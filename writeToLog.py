import os
import datetime

def getLogFileName(): 
    log_file  : str

    log_folder = "LogFolder"

    # Get the list of files in the LogFolder
    files_in_folder = os.listdir(log_folder)

    # Check if there is exactly one file in the folder
    if len(files_in_folder) == 1:
        log_file = os.path.join(log_folder, files_in_folder[0])

    return log_file

def writeToLog(text: str):
    formattedDate = dateAndTimeForLog()
    
    # Specify the folder path
    log_folder = "LogFolder"

    # Get the list of files in the LogFolder
    files_in_folder = os.listdir(log_folder)

    # Check if there is exactly one file in the folder
    if len(files_in_folder) == 1:
        log_file = os.path.join(log_folder, files_in_folder[0])

        with open(log_file, "a") as file:
            file.write(f"{formattedDate}: {text}\n")
    else:
        print("There should be exactly one file in the LogFolder.")

def dateAndTimeForLog() -> str:
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%m/%d/%y: %H:%M")
    return formatted_date_time

if __name__ == "__main__":
    writeToLog("John Smith signs out")
