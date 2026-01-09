import requests
import json
import time

BASE_URL = 'http://localhost:5000/api/chat'

def print_separator():
    print("-" * 50)

def chat_test():
    print("STARTING CHATBOT SELF-TEST")
    print_separator()

    history = []
    
    # 1. Initial Vague Request
    user_msg_1 = "I need to pour concrete"
    print(f"USER: {user_msg_1}")
    
    payload = {'message': user_msg_1, 'history': history}
    try:
        start = time.time()
        res = requests.post(BASE_URL, json=payload, timeout=60)
        duration = time.time() - start
        
        if res.status_code != 200:
            print(f"ERROR: Status {res.status_code}")
            print(res.text)
            return

        data = res.json()
        ai_response = data['response']
        history = data['history']
        
        print(f"AI ({duration:.1f}s): {ai_response}")
        print_separator()
        
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")
        return

    # 2. Refined Request (Should trigger tool)
    user_msg_2 = "It is for separate footings, 30MPa strength, quantity 10m3"
    print(f"USER: {user_msg_2}")
    
    payload = {'message': user_msg_2, 'history': history}
    try:
        start = time.time()
        res = requests.post(BASE_URL, json=payload, timeout=60)
        duration = time.time() - start
        
        data = res.json()
        ai_response = data['response']
        
        print(f"AI ({duration:.1f}s): {ai_response}")
        
        if data.get('is_final'):
            print("SUCCESS: Conversation concluded with structured data!")
            results = data.get('results', [])
            print(f"Found {len(results)} items in DB.")
            for item in results:
                print(f"   - {item['full_code']}: {item['description']}")
        else:
            print("NOTE: LLM did not trigger search yet. This might be valid if it needs more info, or a prompting issue.")
            
        print_separator()

    except Exception as e:
        print(f"CONNECTION ERROR: {e}")

if __name__ == "__main__":
    chat_test()
