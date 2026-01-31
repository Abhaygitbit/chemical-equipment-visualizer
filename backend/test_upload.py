import requests

# Test health
print("Testing health endpoint...")
response = requests.get('http://localhost:8000/api/health/')
print(f"Health: {response.status_code} - {response.json()}")

# Test upload
print("\nTesting upload...")
with open('../sample_equipment_data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/upload/', files=files)
    print(f"Upload: {response.status_code}")
    print(response.json())