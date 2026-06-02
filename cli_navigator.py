import requests
import os

BASE_URL = "http://127.0.0.1:5000/api"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_stations():
    response = requests.get(f"{BASE_URL}/stations")
    if response.status_code == 200:
        return response.json()['stations']
    return []

def search_route(source, destination):
    response = requests.post(f"{BASE_URL}/search", 
                            json={"source": source, "destination": destination})
    if response.status_code == 200:
        return response.json()
    return None

def main():
    while True:
        clear_screen()
        print("=" * 60)
        print("🚆 AI-POWERED METRO BUS NAVIGATOR - CLI VERSION")
        print("=" * 60)
        
        # Get stations
        stations = get_stations()
        station_names = [s['station_name'] for s in stations]
        
        print("\n📋 Available Stations:")
        for i, name in enumerate(station_names[:10], 1):
            print(f"   {i}. {name}")
        print(f"   ... and {len(station_names) - 10} more stations")
        
        print("\n" + "-" * 40)
        
        # Get source
        print("\n📍 Enter source station:")
        source = input("   > ").strip()
        
        if source.lower() == 'quit':
            break
        
        # Get destination
        print("\n🏁 Enter destination station:")
        destination = input("   > ").strip()
        
        # Search route
        print("\n🔍 Searching for route...")
        result = search_route(source, destination)
        
        if result and result.get('success'):
            print("\n" + "=" * 40)
            print("✅ ROUTE FOUND!")
            print("=" * 40)
            print(f"\n📍 From: {result['source']}")
            print(f"📍 To: {result['destination']}")
            print(f"⏱️  Estimated Time: {result['estimated_time']}")
            print(f"🚉 Number of Stops: {result['number_of_stops']}")
            print("\n🗺️  Route Path:")
            for i, station in enumerate(result['path'], 1):
                print(f"   {i}. 🚉 {station}")
        else:
            print("\n❌ Route not found! Please check station names.")
        
        print("\n" + "-" * 40)
        input("\nPress Enter to search again (or type 'quit' to exit)...")

if __name__ == "__main__":
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/stats", timeout=2)
        print("✅ Connected to Metro Navigator Server!")
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Please run 'python app.py' first in another terminal.")