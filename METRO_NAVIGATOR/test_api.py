import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

print("=" * 60)
print("🧪 TESTING METRO NAVIGATOR API")
print("=" * 60)

# Test 1: Get all stations
print("\n1️⃣ Testing GET /stations")
try:
    response = requests.get(f"{BASE_URL}/stations")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success! Found {data['count']} stations")
        print(f"   📍 First 5 stations: {[s['station_name'] for s in data['stations'][:5]]}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Get all routes
print("\n2️⃣ Testing GET /routes")
try:
    response = requests.get(f"{BASE_URL}/routes")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success! Found {data['count']} routes")
        for route in data['routes']:
            print(f"   🚌 {route['route_name']} ({route['line_color']})")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Get system stats
print("\n3️⃣ Testing GET /stats")
try:
    response = requests.get(f"{BASE_URL}/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ System Status: {data['status']}")
        print(f"   📊 Total Stations: {data['total_stations']}")
        print(f"   📊 Total Routes: {data['total_routes']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Search route
print("\n4️⃣ Testing POST /search")
try:
    search_data = {"source": "Saddar", "destination": "Faizabad"}
    response = requests.post(f"{BASE_URL}/search", json=search_data)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Route Found!")
            print(f"   📍 From: {data['source']}")
            print(f"   📍 To: {data['destination']}")
            print(f"   🚉 Path: {' → '.join(data['path'])}")
        else:
            print(f"   ❌ Failed: {data.get('error', 'Unknown error')}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ API Testing Complete!")
print("=" * 60)