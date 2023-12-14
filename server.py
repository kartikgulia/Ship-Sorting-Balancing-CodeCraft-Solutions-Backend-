from flask import send_file
from flask import Flask, request, jsonify, send_file, make_response
import pandas as pd
import datetime
import os
import shutil

from flask_cors import CORS
from CargoGrid import Cargo_Grid


# Functions from other files
from signInHelper import signInHelper
from manifestAccess import getManifestName
from manifestAccess import getManifestGridHelper

from Balance import Balance
from Transfer import Transfer
from writeToLog import getLogFileName
from helpers import parse_file, get_last_txt_file_name, updateWeightInFile, performTransfer

import time

app = Flask(__name__)

CORS(app)
# python -m server run

# dictionary of [row,col] : weight

# used to propagate weights through each ManifestMove file if any changes are made

# remember to reset everytime manifest is done
locationToLoadWeightsDictionary = {

}


@app.route("/")
def home():
    return "Hello, World!"


# add this keyword to url outputted in terminal to trigger this function to output
@app.route('/data')
def get_time():
    x = datetime.datetime.now()
    return {
        'Name': "geek",
        "Age": "22",
        "Date": x,
        "programming": "python"
    }


@app.route('/signin', methods=['POST'])
def signIn() -> bool:
    try:
        if request.method == 'POST':
            data = request.json

            # Check if 'previousUser' and 'currentUser' keys are present in the JSON data
            if 'currentUser' not in data:
                raise ValueError(
                    "Missing  or 'currentUser' in JSON data")

            currentUser = data['currentUser']

            # Takes in current user and writes to log.
            # Also updates prev user to be current user
            signInHelper(currentUser)

            return jsonify({'success': True})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False})


pathToManifestNameTextFile = "ManifestInformation/manifestName.txt"


@app.route('/sendManifest', methods=['POST'])
def receiveManifest():
    # This function does a couple of things:
    # 1) Deletes the old manifest
    # 2) Saves the new manifest (save the actual file) and (save the name of the file in manifestName.txt)

    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['textfile']

            if uploaded_file:
                fileName = uploaded_file.filename

                # Create directories if they don't exist
                if not os.path.exists('ManifestInformation'):
                    os.makedirs('ManifestInformation')

                if not os.path.exists('ManifestForEachMove'):
                    os.makedirs('ManifestForEachMove')

                # Save the uploaded file to a specific directory
                uploaded_file.save(f'ManifestInformation/{fileName}')

                # Reset the file pointer to the beginning of the file
                uploaded_file.seek(0)

                # Save the file again in another directory
                uploaded_file.save(f'ManifestForEachMove/ManifestMove0')

                # Save the name of the uploaded file to "manifestName.txt"
                with open(pathToManifestNameTextFile, 'w') as name_file:
                    name_file.write(fileName)

                # Perform any additional processing on the file content here

                return jsonify({'success': True})
        else:
            return jsonify({'success': False})


@app.route('/getGridInfo', methods=['GET'])
def getManifestGrid():

    try:

        manifest_name: str = getManifestName()

        # Print the value of the variable
        print("Manifest Name:", manifest_name)

        manifest_path = f'./ManifestInformation/{manifest_name}'

        grid_data = getManifestGridHelper(manifest_path=manifest_path)

        # Return the JSON data
        return jsonify({'success': True, 'grid': grid_data})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False, 'message': str(e)})


@app.route('/updateManifestForCurrentMove', methods=['POST'])
def getCurrentMoveManifestGrid():

    if request.method == 'POST':
        data = request.json
        print(data)

        moveNum = data['moveNum']
        manifestPath = f"ManifestForEachMove/ManifestMove{moveNum}"
        time.sleep(0.5)
        grid_data = getManifestGridHelper(manifest_path=manifestPath)
        time.sleep(0.5)
        return jsonify({'success': True, 'grid': grid_data})


@app.route('/sendTransferInfo', methods=['POST'])
def storeInfo():
    if request.method == 'POST':
        data = request.json
        # print(data)

        # Directory where files will be stored
        dir_path = 'TransferInformation'

        # Ensure the directory exists
        os.makedirs(dir_path, exist_ok=True)

        # File paths
        names_file_path = f"{dir_path}/initialTruckContainerNames.txt"
        positions_file_path = f"{dir_path}/initialUnloadPositions.txt"

        # Writing names to the file
        with open(names_file_path, 'w') as names_file:
            for name in data['selectedNames']:
                names_file.write(name + '\n')

        # Writing positions to the file
        with open(positions_file_path, 'w') as positions_file:
            for position in data['selectedPositions']:
                line = f"{position['rowIndex']},{position['colIndex']}\n"
                positions_file.write(line)

        return jsonify({'success': True})

    # Return a response for non-POST requests or in case of an error
    return jsonify({'success': False, 'message': 'Invalid request method or error occurred'})

@app.route('/balance', methods=['GET'])
def returnBalanceInfo():
    if request.method == 'GET':

        manifestName = getManifestName()
        manifestNamePath = f"./ManifestInformation/{manifestName}"
        headers = ['Position', 'Weight', 'Cargo']
        pandasDF_for_Manifest = pd.read_csv(
            manifestNamePath, sep=', ', names=headers, engine='python')
        cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
        cargo_grid.array_builder()
        # cargo_grid.print()
        balance = Balance(cargo_grid)
        balance.Balance("./ManifestInformation/Balance.txt")
        # balance.CargoGrid.print()
        # progressionList = balance.ProgressionList

        move = []
        if (os.path.exists("./ManifestInformation/Balance.txt")):
            moveCoordinates, names, times, times_remaining = parse_file("./ManifestInformation/Balance.txt")



        return jsonify({
            "moveCoordinates": moveCoordinates,
            "names" : names,
            "times" : times,
            "timesRemaining" : times_remaining
            
            })


@app.route('/transfer', methods=['GET'])
def returnTransferInfo():
    if request.method == 'GET':
        time.sleep(1)
        performTransfer()
        time.sleep(1)
        moveCoordinates, names, times, times_remaining = parse_file("ManifestInformation/Transfer.txt")
        time.sleep(1)
        return jsonify({
            "moveCoordinates": moveCoordinates,
            "names" : names,
            "times" : times,
            "timesRemaining" : times_remaining
            
            })
    
@app.route('/fetchOperationData', methods=['POST'])
def returnOperationData():
    if request.method == 'POST':
        
        data = request.json
        isBalance = data['isBalance']

        time.sleep(0.5)
        
        manifestName = getManifestName()
        manifestNamePath = f"./ManifestInformation/{manifestName}"
        headers = ['Position', 'Weight', 'Cargo']
        pandasDF_for_Manifest = pd.read_csv(
            manifestNamePath, sep=', ', names=headers, engine='python')
        cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
        cargo_grid.array_builder()
        # cargo_grid.print()

        time.sleep(0.5)

        if(isBalance == 1):
            balance = Balance(cargo_grid)
            balance.Balance("ManifestInformation/Balance.txt")
            # balance.CargoGrid.print()
            # progressionList = balance.ProgressionList
        
        else:
            
            performTransfer()
        
        time.sleep(0.5)
            

        if (os.path.exists("./ManifestInformation/Balance.txt")):
            moveCoordinates, names, times, times_remaining = parse_file("ManifestInformation/Balance.txt")

        else:
            moveCoordinates, names, times, times_remaining = parse_file("ManifestInformation/Transfer.txt")

        time.sleep(0.5)

        return jsonify({
            "moveCoordinates": moveCoordinates,
            # "names" : names,
            # "times" : times,
            # "timesRemaining" : times_remaining
            
            })



@app.route('/updateWeight', methods=['POST'])
def updateWeight():
    if request.method == 'POST':
        data = request.json

        # Format weight as a 5-digit number
        stringWeight = f"{int(data['weight']):05d}"
        row = data['row']
        col = data['column']
        moveNum = data['moveNum']

        print(data)

        # function that takes in a file path, row, col, and weight, and updates the weight

        # Construct the file path

        file_path = f"ManifestForEachMove/ManifestMove{moveNum}"
        updateWeightInFile(row, col, stringWeight, file_path)

        # add to dictionary

        locationToLoadWeightsDictionary[(row, col)] = stringWeight
        return {"status": "success"}

    else:
        return {"status": "error"}


@app.route('/propagateWeights', methods=['POST'])
def propagateWeights():

    # this route is called every time the next button is pressed.

    # input:
    #   1) the current move's FROM row and col
    #   2) the current move's TO row and col
    #   3) index of current move

    # goal : send weight from ManifestMove{n} to ManifestMove{n+1}

    # Algorithm
    #   iterate through each element in the dictionary. for each position:

    #   check if FROM exists in the locationToLoadWeightsDictionary
    #   if yes,
    #       1) In the ManifestMove{n+1}, set the weight at the TO row and col
    #       2) Change the key in the dictionary to represent the new TO position

    #   else, just take the position in the dictionary and in the ManifestMove{n+1}, set the weight at the position

    print()

    if (request.method == 'POST'):

        data = request.json

        fromRow = data['fromRow']
        fromCol = data['fromCol']

        toRow = data['toRow']
        toCol = data['toCol']
        moveNum = data['moveNum']
        totalNumMoves = data['totalNumMoves']
        print(totalNumMoves)
        currentManifestFile = f"ManifestForEachMove/ManifestMove{moveNum-1}"
        nextManifestFile = f"ManifestForEachMove/ManifestMove{moveNum}"

        for key, value in locationToLoadWeightsDictionary.items():

            currentMoveFromPosition = (fromRow, fromCol)

            if currentMoveFromPosition in locationToLoadWeightsDictionary:  # we're moving a "loaded container"

                print()

            else:   # not moving, just propagate the weight

                # get the weight in the current move
                weight = value
                # print(weight)

                # send weight to the next file

                updateWeightInFile(key[0], key[1], weight, nextManifestFile)

    return {"status": "success"}


@app.route('/downloadLog', methods=['GET'])
def downloadLog():
    log_file = getLogFileName()
    log_filename = os.path.basename(log_file)

    if os.path.exists(log_file):
        response = send_file(log_file, as_attachment=True)
        response.headers['Content-Disposition'] = 'attachment; filename=\"{}\"'.format(
            log_filename)
        return response
    else:
        return jsonify({'success': False, 'message': 'Log file not found'})


@app.route('/downloadUpdatedManifest', methods=['GET'])
def downloadUpdatedManifest():

    # Send the specific text file to the frontend
    # Assuming getManifestName() is a function you've defined
    manifest_name = getManifestName()
    manifest_name = manifest_name.rstrip('.txt')

    updatedManifestPath = f"ManifestForEachMove/{
        get_last_txt_file_name("./ManifestForEachMove")}"

    # Now construct the outbound_file_path using the modified manifestName
    outbound_file_path = f"./ManifestInformation/{manifest_name}_OUTBOUND.txt"

    shutil.copyfile(updatedManifestPath, outbound_file_path)

    file_to_send = f"ManifestInformation/{manifest_name}_OUTBOUND.txt"
    print(file_to_send)
    
    time.sleep(0.5)

    if os.path.exists(file_to_send):
        return send_file(file_to_send, as_attachment=True)
    else:
        return "File not found", 404


@app.route('/getOutboundName', methods=['GET'])
def getOutboundName():
    # Send the specific text file to the frontend
    # Assuming getManifestName() is a function you've defined
    manifest_name = getManifestName()
    manifest_name = manifest_name.rstrip('.txt')

    file_to_send = f"{manifest_name}_OUTBOUND.txt"
    print(file_to_send)

    return jsonify({'fileName': file_to_send})


@app.route('/resetFilesForNewShip', methods=['GET'])
def deleteFiles():

    dir_names = ["TransferInformation",
                 "ManifestInformation", "ManifestForEachMove"]

    for dir_name in dir_names:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
            print(f"Deleted directory: {dir_name}")
        else:
            print(f"Directory not found: {dir_name}")

    # reset dictionary
    locationToLoadWeightsDictionary = {}

    # balancePath = "./ManifestInformation/Balance.txt"
    # if(os.path.exists(balancePath)):
    #     with open(balancePath, "w") as balance_file:
    #             balance_file.truncate(0)  # This will remove all text from the file
    
    # else:
    #     with open("./ManifestInformation/Transfer.txt", "w") as transfer_file:
    #         transfer_file.truncate(0)


    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
