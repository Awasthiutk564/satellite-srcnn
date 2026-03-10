import requests
import uuid
import json

BASE_URL = "http://localhost:8000/api/v1"

def test():
    email = f"test_{uuid.uuid4().hex}@ex.com"
    password = "password123"
    print(f"Registering {email}...")
    res1 = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Test User"
    })
    
    if res1.status_code != 200:
        print("Register failed:", res1.json())
        return

    print("Login...")
    res2 = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    with open("login_out.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(res2.json(), indent=2))
        
    print("Login status:", res2.status_code)

test()
