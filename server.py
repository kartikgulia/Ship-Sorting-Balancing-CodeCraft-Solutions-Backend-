from flask import Flask
import re
import datetime

from flask_cors import CORS

x = datetime.datetime.now()

app = Flask(__name__)

# Configure CORS to allow requests from http://localhost:3000
CORS(app, resources={r"/data": {"origins": "http://localhost:3000"}})

# python -m server run


@app.route("/")
def home():
    return "Hello, World!"


# add this keyword to url outputted in terminal to trigger this function to output
@app.route('/data')
def get_time():
    return {
        'Name': "geek",
        "Age": "22",
        "Date": x,
        "programming": "python"
    }


if __name__ == '__main__':
    app.run(debug=True)
