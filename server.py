from flask import Flask, request, jsonify
import pandas as pd
import datetime
import os
from flask_cors import CORS
from CargoGrid import Cargo_Grid
from manifestAccess import getManifestGridHelper

# Functions from other files
from writeToLog import writeToLog


app = Flask(__name__)

CORS(app)
# python -m server run

manifestFileNamePath = './ManifestInformation/manifestName.txt'


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
            if 'previousUser' not in data or 'currentUser' not in data:
                raise ValueError(
                    "Missing 'previousUser' or 'currentUser' in JSON data")

            previousUser = data['previousUser']
            currentUser = data['currentUser']

            signOutText = f"{previousUser} signs out"
            signInText = f"{currentUser} signs in"

            writeToLog(signOutText)
            writeToLog(signInText)

            return jsonify({'success': True})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False})


@app.route('/sendManifest', methods=['POST'])
def receiveManifest():
    # This function does a couple of things:
    # 1) Deletes the old manifest
    # 2) Saves the new manifest (save the actual file) and (save the name of the file in manifestName.txt)

    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['textfile']

            old_manifest_name: str

            # Delete the old manifest if it exists
            if os.path.exists(manifestFileNamePath):
                with open(manifestFileNamePath, 'r') as name_file:
                    old_manifest_name = f'./ManifestInformation/{
                        name_file.read().strip()}'
                if os.path.exists(f'./{old_manifest_name}'):
                    os.remove(f'./{old_manifest_name}')

            # Process the uploaded file as needed
            if uploaded_file:
                fileName = uploaded_file.filename

                # Save the uploaded file to a specific directory
                uploaded_file.save(f'./ManifestInformation/{fileName}')

                # Save the name of the uploaded file to "manifestName.txt"
                with open(manifestFileNamePath, 'w') as name_file:
                    name_file.write(fileName)

                # You can also read the content of the file if needed
                file_content = uploaded_file.read()
                print("Received file content:", file_content)

                # Perform any additional processing on the file content here

                return jsonify({'success': True})
        else:
            return jsonify({'success': False})


@app.route('/getGridInfo', methods=['GET'])
def getManifestGrid():
    try:

        manifest_name: str = ""

        with open(manifestFileNamePath, "r") as file:
            # Read the content of the file and store it in a variable
            manifest_name = file.read().strip()

            # Print the value of the variable
            print("Manifest Name:", manifest_name)

        grid_data = getManifestGridHelper(manifest_name)

        # Return the JSON data
        return jsonify({'success': True, 'grid': grid_data})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
