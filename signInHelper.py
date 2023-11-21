import os

from writeToLog import writeToLog

def getPreviousUser():
    user_info_folder = "UserInformation"
    previous_user_file = os.path.join(user_info_folder, "PreviousUser.txt")
    
    try:
        with open(previous_user_file, "r") as file:
            previous_user = file.readline().strip()
            return previous_user
    except FileNotFoundError:
        return None

def updatePreviousUser(currentUser):
    user_info_folder = "UserInformation"
    previous_user_file = os.path.join(user_info_folder, "PreviousUser.txt")

    # Update the PreviousUser.txt file with the currentUser
    with open(previous_user_file, "w") as file:
        file.write(currentUser)

def signInHelper(currentUser):
    previousUser = getPreviousUser()

    signOutText = f"{previousUser} signs out" if previousUser else "No previous user found"
    signInText = f"{currentUser} signs in"

    # Update the PreviousUser.txt file with the currentUser
    updatePreviousUser(currentUser)

    writeToLog(signOutText)
    writeToLog(signInText)

if __name__ == "__main__":
    currentUser = "John Smith"  # Replace with the actual current user
    signInHelper(currentUser)
