from flask import Flask, request, jsonify
import re
import datetime
import os
from flask_cors import CORS


# Functions from other files
from writeToLog import writeToLog


app = Flask(__name__)

CORS(app, resources={
    r"/data": {"origins": "*"},
    r"/sendName": {"origins": "*"},
    r"/signIn": {"origins": "*"},
    r"/sendManifest": {"origins": "*"}
})
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


if __name__ == '__main__':
    app.run(debug=True)
