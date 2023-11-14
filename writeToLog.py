import datetime


def writeToLog(text: str):

    formattedDate = dateAndTimeForLog()

    messageForLog = f"{formattedDate}: {text}"

    with open("Keogh2023.txt", "a") as file:
        file.write(messageForLog + "\n")


def dateAndTimeForLog() -> str:
    now = datetime.datetime.now()
    # "Date": "Tue, 14 Nov 2023 11:50:05 GMT"
    formatted_date_time = now.strftime("%m/%d/%y: %H:%M")

    return formatted_date_time


if __name__ == "__main__":
    writeToLog("John Smith signs out")
