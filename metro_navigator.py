import pandas as pd

class MetroNavigator:
    def __init__(self):
        self.stations = pd.read_csv('csv_files/Stations.csv')
        self.routes = pd.read_csv('csv_files/Routes.csv')
        self.route_stations = pd.read_csv('csv_files/Route_Stations.csv')
        print(f"✅ Loaded {len(self.stations)} stations")
        print(f"✅ Loaded {len(self.routes)} routes")
        print(f"✅ Loaded {len(self.route_stations)} connections")

    def show_all_stations(self):
        print("\n" + "=" * 50)
        print("📋 ALL STATIONS")
        print("=" * 50)
        for _, station in self.stations.iterrows():
            print(f"   🚉 {station['station_name']}")

    def show_all_routes(self):
        print("\n" + "=" * 50)
        print("📋 ALL ROUTES")
        print("=" * 50)
        for _, route in self.routes.iterrows():
            print(f"   🚌 {route['route_name']} ({route['line_color']})")

    def show_route_stations(self, route_name):
        """Show all stations on a specific route"""
        route = self.routes[self.routes['route_name'].str.contains(route_name, case=False)]
        if route.empty:
            print(f"❌ Route '{route_name}' not found")
            return
        
        route_id = route.iloc[0]['route_id (PK)']
        stations_on_route = self.route_stations[self.route_stations['route_id (FK)'] == route_id]
        stations_on_route = stations_on_route.merge(
            self.stations, 
            left_on='station_id (FK)', 
            right_on='station_id (PK)'
        )
        stations_on_route = stations_on_route.sort_values('sequence_number')
        
        print(f"\n🚆 {route.iloc[0]['route_name']} Stations:")
        print("-" * 30)
        for _, station in stations_on_route.iterrows():
            print(f"   {station['sequence_number']}. 🚉 {station['station_name']}")

# Run the program
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI-POWERED METRO BUS NAVIGATOR")
    print("=" * 50)
    
    nav = MetroNavigator()
    nav.show_all_stations()
    nav.show_all_routes()
    
    # Test show route stations
    print("\n" + "=" * 50)
    print("🔍 TESTING ROUTE STATIONS")
    print("=" * 50)
    nav.show_route_stations("Red")