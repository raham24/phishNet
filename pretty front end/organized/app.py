from flask import Flask, request, jsonify
import main

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input1 = data.get('input1')
    input2 = data.get('input2')
    result = main.pred(input1, input2)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)