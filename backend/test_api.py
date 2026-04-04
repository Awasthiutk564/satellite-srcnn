import requests
import json

base_url = "http://localhost:8000/api/v1"

print("Testing Registration...")
res = requests.post(f"{base_url}/auth/register", json={
    "email": "test2@test.com",
    "password": "password123",
    "full_name": "Test User"
})
print("Reg status:", res.status_code)
print("Reg body:", res.text)

print("\nTesting Login...")
res = requests.post(f"{base_url}/auth/login", json={
    "email": "test2@test.com",
    "password": "password123"
})
print("Login status:", res.status_code)
print("Login body:", res.text)
