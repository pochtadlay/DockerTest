from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/generate')
def generate():
    number = random.randint(1, 100)
    return jsonify({"number": number})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)