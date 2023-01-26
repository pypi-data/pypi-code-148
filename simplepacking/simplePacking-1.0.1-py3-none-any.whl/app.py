from flask import Flask, jsonify,request
from waitress import serve

from example import example

app = Flask(__name__)

@app.route('/postExample',methods=['POST'])
def calc():
    request_data = request.get_json()
    number = request_data['number']
    obj = example(number)
    res=example.get_param(obj)
    response={
        "status":"start",
        "result":res
    }
    return response


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7000)
