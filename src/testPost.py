# client.py
import requests

data = {'key': 'value'}
response = requests.post('http://localhost:5000/test', json=data)
print(f'Server response: {response.json()}')
