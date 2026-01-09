import requests

try:
    r = requests.get('http://localhost:5000/api/divisions', timeout=5)
    print(f'Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'Divisions count: {len(data)}')
        print('\nFirst 5 divisions:')
        for d in data[:5]:
            print(f"  {d['code']} - {d['name']}")
    else:
        print(f'Error: {r.text}')
except Exception as e:
    print(f'Error: {e}')
