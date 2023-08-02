# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    # print(f'Received data: {data}')
    return jsonify({'status': 'success', 'received_data': data})

if __name__ == "__main__":
    app.run(port=5000)
