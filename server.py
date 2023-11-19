from flask import Flask, request, jsonify
import pandas as pd
import datetime
import os
from flask_cors import CORS
from CargoGrid import Cargo_Grid


# Functions from other files
from writeToLog import writeToLog


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


# @app.route('/sendName', methods=['POST'])
# def send_name():
#     if request.method == 'POST':
#         data = request.json  # Assuming data is sent as JSON
#         name = data.get('name')
#         print("Received name:", name)
#         return jsonify({'message': 'Name received successfully'})


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

            # Delete the old manifest if it exists
            if os.path.exists('./manifestName.txt'):
                with open('./manifestName.txt', 'r') as name_file:
                    old_manifest_name = name_file.read().strip()
                if os.path.exists(f'./{old_manifest_name}'):
                    os.remove(f'./{old_manifest_name}')

            # Process the uploaded file as needed
            if uploaded_file:
                fileName = uploaded_file.filename

                # Save the uploaded file to a specific directory
                uploaded_file.save(f'./{fileName}')

                # Save the name of the uploaded file to "manifestName.txt"
                with open('./manifestName.txt', 'w') as name_file:
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

        with open("manifestName.txt", "r") as file:
            # Read the content of the file and store it in a variable
            manifest_name = file.read().strip()

            # Print the value of the variable
            print("Manifest Name:", manifest_name)

        # Load the manifest file into a Pandas DataFrame
        headers = ['Position', 'Weight', 'Cargo']
        pandasDF_for_Manifest = pd.read_csv(
            f'./{manifest_name}', sep=', ', names=headers, engine='python')

        # Initialize and populate the Cargo_Grid
        cargo_grid = Cargo_Grid(pandasDF_for_Manifest)
        cargo_grid.array_builder()

        # Convert the Cargo_Grid to a JSON-serializable format
        grid_data = []
        for x in range(len(cargo_grid.cargo_grid)):
            for y in range(len(cargo_grid.cargo_grid[x])):
                cargo = cargo_grid.cargo_grid[x][y]
                grid_data.append({
                    "position": cargo.position,
                    "weight": cargo.weight,
                    "name": cargo.name
                })

        # Return the JSON data
        return jsonify({'success': True, 'grid': grid_data})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
