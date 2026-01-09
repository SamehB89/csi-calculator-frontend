from backend.app import get_working_model

print("Testing Model Discovery...")
model = get_working_model()
print(f"Discovered Model: '{model}'")
