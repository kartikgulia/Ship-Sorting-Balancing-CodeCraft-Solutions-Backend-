from flask import Flask, request, jsonify
import re
import datetime

from flask_cors import CORS


app = Flask(__name__)

# Configure CORS to allow requests from http://localhost:3000
CORS(app, resources={

    r"/data": {"origins": "http://localhost:3000"},
    r"/sendName": {"origins": "http://localhost:3000"}

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


@app.route('/sendName', methods=['POST'])
def send_name():
    if request.method == 'POST':
        data = request.json  # Assuming data is sent as JSON
        name = data.get('name')
        print("Received name:", name)
        return jsonify({'message': 'Name received successfully'})


if __name__ == '__main__':
    app.run(debug=True)
