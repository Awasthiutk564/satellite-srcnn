import requests

BASE_URL = "http://localhost:8000/api/v1"

def test():
    # 1. Register
    print("Testing Register...")
    email = "test4@ex.com"
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": "password123",
        "full_name": "Test User"
    })
    
    # 2. Login
    print("\nTesting Login...")
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": "password123"
    })
    print("Login Response:", res.status_code, res.json())
    if res.status_code != 200:
        return
        
    token = res.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Upload & Enhance
    print("\nTesting /enhance/upload...")
    with open("dummy.png", "wb") as f:
        # 4x4 image to pass the "scale factor 2" minimum check (4x4 => 2x2 lr size)
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x04\x00\x00\x00\x04\x08\x00\x00\x00\x00\x4c\x52\x05\x13\x00\x00\x00\x0cIDAT\x08\xd7\x63\xf8\x0f\x00\x01\x01\x01\x00\x1c\x82\x02\xf5\x77\xbd\x22\x33\x00\x00\x00\x00IEND\xaeB`\x82')

    with open("dummy.png", "rb") as f:
        res = requests.post(
            f"{BASE_URL}/enhance/upload",
            headers=headers,
            files={"file": ("dummy.png", f, "image/png")},
            data={"model_type": "srcnn", "scale_factor": 2}
        )
    print("Enhance Upload Response:", res.status_code, res.json())
test()
