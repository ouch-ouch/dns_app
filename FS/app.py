import requests
from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    response = requests.put(f'http://{as_ip}:{as_port}/register', json=data)
    if response.status_code == 201:
        return jsonify({"message": "Registered successfully"}), 201
    else:
        return response.json(), response.status_code

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if not number.isdigit():
        return jsonify({"error": "Bad format"}), 400

    n = int(number)
    fib_number = fibonacci_number(n)
    return jsonify({"fibonacci": fib_number}), 200

def fibonacci_number(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)