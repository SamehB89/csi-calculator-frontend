import requests
import json

# Start the Flask app in background? No, I assume user might already have it running, or I can restart it. 
# Actually, I cannot restart the server myself easily if it's running in a terminal I don't control.
# But I can assume the user will restart it, or I can try to make a test request if I could spin up a test instance.
# Wait, I can just use `app.test_client()` from `app.py` directly without running the server!

from backend.app import app

def verify_fix():
    print("Verifying fix for 'Lecture hall seating'...")
    
    with app.test_client() as client:
        # 1. Test with full_code (Correct item)
        # Expected: Daily Output = 8.0, Unit = EA
        response = client.get('/api/item-details?full_code=127 101-1000')
        if response.status_code != 200:
            print(f"FAILED: Status code {response.status_code}")
            return
            
        data = response.json
        daily_output = data['productivity']['daily_output']
        unit = data['item']['unit']
        desc = data['item']['description']
        
        print(f"Item: {desc}")
        print(f"Daily Output: {daily_output}")
        print(f"Unit: {unit}")
        
        if daily_output == 8.0 and "EA" in unit:
            print("SUCCESS: Correct item returned.")
        else:
            print("FAILED: Incorrect item returned.")
            
        # 2. Test with item_code (Legacy/Ambiguous - for reference only)
        # We expect it might still fail or return the first match if full_code not provided
        # But we mostly care that sending full_code WORKS.

if __name__ == "__main__":
    verify_fix()
