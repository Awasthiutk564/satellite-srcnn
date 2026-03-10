import requests
import uuid
import json

BASE_URL = "http://localhost:8000/api/v1"

def test():
    email = f"test_{uuid.uuid4().hex}@ex.com"
    res1 = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": "password123",
        "full_name": "Test User"
    })
    
    with open("error_out.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(res1.json(), indent=2))

test()
