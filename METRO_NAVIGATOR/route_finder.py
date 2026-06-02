import pandas as pd
import heapq

print("=" * 60)
print("🚆 CHAPTER 3: DIJKSTRA ROUTE FINDING ALGORITHM")
print("=" * 60)

class MetroRouteFinder:
    def __init__(self):
        # Load data
        self.stations = pd.read_csv('csv_files/Stations.csv')
        self.routes = pd.read_csv('csv_files/Routes.csv')
        self.route_stations = pd.read_csv('csv_files/Route_Stations.csv')
        
        # Build graph
        self.graph = {}
        self.build_graph()
        
        print(f"\n✅ Loaded {len(self.stations)} stations")
        print(f"✅ Loaded {len(self.routes)} routes")
        print(f"✅ Built graph with {len(self.graph)} nodes")
    
    def build_graph(self):
        """Build graph from stations and connections"""
        # Add all stations as nodes
        for _, station in self.stations.iterrows():
            station_id = station['station_id (PK)']
            self.graph[station_id] = []
        
        # Add edges based on route_stations (consecutive stations)
        sorted_route_stations = self.route_stations.sort_values(['route_id', 'stop_sequence'])
        
        for route_id in sorted_route_stations['route_id'].unique():
            route_stations = sorted_route_stations[sorted_route_stations['route_id'] == route_id]
            station_ids = route_stations['station_id'].tolist()
            
            # Connect consecutive stations
            for i in range(len(station_ids) - 1):
                from_id = station_ids[i]
                to_id = station_ids[i + 1]
                # Add edge both directions
                self.graph[from_id].append({'to': to_id, 'weight': 1})
                self.graph[to_id].append({'to': from_id, 'weight': 1})
    
    def dijkstra(self, start_id, end_id):
        """Find shortest path using Dijkstra's algorithm"""
        distances = {node: float('infinity') for node in self.graph}
        distances[start_id] = 0
        previous = {node: None for node in self.graph}
        pq = [(0, start_id)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current == end_id:
                break
            
            if current_dist > distances[current]:
                continue
            
            for neighbor in self.graph[current]:
                distance = current_dist + neighbor['weight']
                if distance < distances[neighbor['to']]:
                    distances[neighbor['to']] = distance
                    previous[neighbor['to']] = current
                    heapq.heappush(pq, (distance, neighbor['to']))
        
        # Reconstruct path
        path = []
        current = end_id
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        
        if path[0] != start_id:
            return []
        return path
    
    def get_station_name(self, station_id):
        """Get station name by ID"""
        station = self.stations[self.stations['station_id (PK)'] == station_id]
        if not station.empty:
            return station.iloc[0]['station_name']
        return str(station_id)
    
    def find_route(self, source_name, dest_name):
        """Find route between two stations by name"""
        # Find station IDs
        source = self.stations[self.stations['station_name'].str.contains(source_name, case=False)]
        dest = self.stations[self.stations['station_name'].str.contains(dest_name, case=False)]
        
        if source.empty:
            return {'error': f"Station '{source_name}' not found"}
        if dest.empty:
            return {'error': f"Station '{dest_name}' not found"}
        
        source_id = source.iloc[0]['station_id (PK)']
        dest_id = dest.iloc[0]['station_id (PK)']
        
        # Find path
        path_ids = self.dijkstra(source_id, dest_id)
        
        if not path_ids:
            return {'error': 'No route found between these stations'}
        
        # Convert IDs to names
        path_names = [self.get_station_name(sid) for sid in path_ids]
        
        return {
            'source': source_name,
            'destination': dest_name,
            'path': path_names,
            'number_of_stations': len(path_names),
            'number_of_stops': len(path_names) - 1,
            'estimated_time': f"{len(path_names) * 2} minutes",
            'success': True
        }
    
    def show_all_stations(self):
        """Display all stations"""
        print("\n" + "=" * 60)
        print("📋 ALL METRO STATIONS")
        print("=" * 60)
        for _, station in self.stations.iterrows():
            print(f"   🚉 {station['station_name']}")
    
    def show_all_routes(self):
        """Display all routes"""
        print("\n" + "=" * 60)
        print("📋 ALL METRO ROUTES")
        print("=" * 60)
        for _, route in self.routes.iterrows():
            print(f"   🚌 {route['route_name']}")

# Test the route finder
if __name__ == "__main__":
    nav = MetroRouteFinder()
    nav.show_all_stations()
    nav.show_all_routes()
    
    # Test route finding
    print("\n" + "=" * 60)
    print("🔍 TESTING ROUTE FINDING")
    print("=" * 60)
    
    result = nav.find_route("Saddar", "Faizabad")
    if 'error' in result:
        print(f"❌ {result['error']}")
    else:
        print(f"\n✅ Route found!")
        print(f"   From: {result['source']}")
        print(f"   To: {result['destination']}")
        print(f"   Stops: {result['number_of_stops']}")
        print(f"   Time: {result['estimated_time']}")
        print(f"\n   📍 Route:")
        for i, station in enumerate(result['path'], 1):
            print(f"      {i}. 🚉 {station}")
    
    print("\n" + "=" * 60)
    print("✅ CHAPTER 3 COMPLETE: Dijkstra Algorithm Working!")
    print("=" * 60)