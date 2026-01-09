import requests
import json

url = 'http://localhost:5000/api/calculate-assembly'
headers = {'Content-Type': 'application/json'}
data = {'assembly_id': 1, 'quantity': 100}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
    if 'response' in locals():
        print(response.text)
