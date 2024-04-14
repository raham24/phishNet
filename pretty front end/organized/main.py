from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
def pred(url):
    # Your prediction logic here
    return url

@app.route('/predict', methods=['POST'])
def predict():
    print(request.data)  # Log the raw request data
    data = request.get_json()
    url = data.get('url')
    if url is None:
        return {'error': 'No url provided'}, 400
    prediction = pred(url)
    return {'prediction': prediction}




if __name__ == '__main__':
    app.run(port=5000)