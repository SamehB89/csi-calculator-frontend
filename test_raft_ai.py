import requests
import json

url = 'http://localhost:5000/api/ai'
headers = {'Content-Type': 'application/json'}

# Test cases for Raft Foundation
test_queries = [
    "raft foundation 500m3",
    "صب لبشة 1000 متر مكعب",
    "mat foundation 200 m3"
]

for q in test_queries:
    print(f"\nTesting query: '{q}'")
    data = {'query': q}
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            res_json = response.json()
            print("Response Strategy:", res_json.get('strategy'))
            # Check if it identified as raft/mat
            text = res_json.get('plan', {}).get('text', '')
            print("Plan Text Summary:", text.split('\n')[0]) 
            
            if "Raft" in text or "Mat" in text or "لبشة" in text:
                print("PASS: Correctly identified as Raft/Mat foundation.")
            else:
                print("FAIL: Did not identify as Raft/Mat foundation.")
        else:
            print(f"Error: Status Code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception: {e}")
