from flask import Flask, request, jsonify
import pandas as pd
import datetime
import os
from flask_cors import CORS
from CargoGrid import Cargo_Grid


# Functions from other files
from signInHelper import signInHelper
from manifestAccess import getManifestName
from Balance import Balance

from helpers import parse_balance_file
app = Flask(__name__)

CORS(app)
# python -m server run


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

            # Delete the old manifest if it exists
            old_manifest_name = getManifestName()

            if os.path.exists(f'./ManifestInformation/{old_manifest_name}'):
                os.remove(f'./ManifestInformation/{old_manifest_name}')

            # Process the uploaded file as needed
            if uploaded_file:
                fileName = uploaded_file.filename

                # Save the uploaded file to a specific directory
                uploaded_file.save(f'./ManifestInformation/{fileName}')

                # Save the name of the uploaded file to "manifestName.txt"
                with open(pathToManifestNameTextFile, 'w') as name_file:
                    name_file.write(fileName)

                # You can also read the content of the file if needed
                file_content = uploaded_file.read()
                # print("Received file content:", file_content)

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

        # Load the manifest file into a Pandas DataFrame
        headers = ['Position', 'Weight', 'Cargo']
        pandasDF_for_Manifest = pd.read_csv(
            f'./ManifestInformation/{manifest_name}', sep=', ', names=headers, engine='python')

        # Initialize and populate the Cargo_Grid
        cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
        cargo_grid.array_builder()

        # Convert the Cargo_Grid to a JSON-serializable format
        grid_data = [{}] * 8
        for i in range(8):
            grid_data[i] = [{}] * 12

        for eachRow in range(len(cargo_grid.cargo_grid)):
            for eachCol in range(len(cargo_grid.cargo_grid[eachRow])):

                cargo = cargo_grid.cargo_grid[eachRow][eachCol]

                position = cargo.position
                # print(position)

                if position == [0, 0]:
                    continue

                rowNum = 8 - position[0]
                colNum = position[1] - 1

                grid_data[rowNum][colNum] = {
                    "position": cargo.position,
                    "name": cargo.name,
                    "weight": cargo.weight
                }

        # Return the JSON data
        return jsonify({'success': True, 'grid': grid_data})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False, 'message': str(e)})


@app.route('/sendTransferInfo', methods=['POST'])
def storeInfo():
    if request.method == 'POST':
        data = request.json
        # print(data)

        # Directory where files will be stored
        dir_path = 'ManifestInformation/TransferInformation'

        # Ensure the directory exists
        os.makedirs(dir_path, exist_ok=True)

        # File paths
        names_file_path = os.path.join(
            dir_path, 'initialTruckContainerNames.txt')
        positions_file_path = os.path.join(
            dir_path, 'initialUnloadPositions.txt')

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

        manifestName = f"./ManifestInformation/{getManifestName()}"
        headers = ['Position', 'Weight', 'Cargo']
        pandasDF_for_Manifest = pd.read_csv(
            manifestName, sep=', ', names=headers, engine='python')
        cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
        cargo_grid.array_builder()
        # cargo_grid.print()
        balance = Balance(cargo_grid)
        balance.Balance("./ManifestInformation/Balance.txt")
        # balance.CargoGrid.print()
        progressionList = balance.ProgressionList

        moves = parse_balance_file("./ManifestInformation/Balance.txt")

        with open("./ManifestInformation/Balance.txt", "w") as balance_file:
            balance_file.truncate(0)  # This will remove all text from the file
        return jsonify({'manifestGrids': "progressionList", "listOfMoves": moves})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
