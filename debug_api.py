import requests
import json

url = "http://localhost:5000/api/ai"
payload = {
    "query": "120 cum raft",
    "lang": "en"
}

try:
    print(f"Sending POST to {url}...")
    resp = requests.post(url, json=payload)
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
