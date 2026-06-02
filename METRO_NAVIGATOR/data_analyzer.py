import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("📊 METRO DATA ANALYZER")
print("=" * 60)

# Load data
stations = pd.read_csv('csv_files/Stations.csv')
routes = pd.read_csv('csv_files/Routes.csv')
route_stations = pd.read_csv('csv_files/Route_Stations.csv')

print(f"\n✅ Loaded {len(stations)} stations")
print(f"✅ Loaded {len(routes)} routes")
print(f"✅ Loaded {len(route_stations)} connections")

# Station name analysis
print("\n" + "-" * 40)
print("📋 STATION NAME ANALYSIS")
print("-" * 40)

# Count stations by area (Rawalpindi vs Islamabad)
rwp_keywords = ['Saddar', 'Marri', 'Liaquat', 'Committee', 'Waris', 'Chandni', 'Rehmanabad', '6th Road', 'Shamsabad', 'Faizabad']
isb_keywords = ['I-8', 'I-9', 'G-7', 'G-8', 'G-9', 'G-10', 'F-7', 'F-8', 'F-10', 'H-8', 'H-9', 'D-12']

rwp_count = sum(1 for s in stations['station_name'] if any(kw in str(s) for kw in rwp_keywords))
isb_count = sum(1 for s in stations['station_name'] if any(kw in str(s) for kw in isb_keywords))

print(f"📍 Rawalpindi Stations: ~{rwp_count}")
print(f"📍 Islamabad Stations: ~{isb_count}")
print(f"📍 Other/Unknown: {len(stations) - rwp_count - isb_count}")

# Route analysis
print("\n" + "-" * 40)
print("🚌 ROUTE ANALYSIS")
print("-" * 40)

for _, route in routes.iterrows():
    route_id = route['route_id (PK)']
    route_name = route['route_name']
    line_color = route['line_color']
    
    stations_on_route = route_stations[route_stations['route_id (FK)'] == route_id]
    print(f"\n🚆 {route_name} ({line_color})")
    print(f"   📍 Route ID: {route_id}")
    print(f"   🚉 Stations: {len(stations_on_route)} stops")
    
    # Show first and last station
    if len(stations_on_route) > 0:
        first_station_id = stations_on_route[stations_on_route['sequence_number'] == stations_on_route['sequence_number'].min()]['station_id (FK)'].iloc[0]
        last_station_id = stations_on_route[stations_on_route['sequence_number'] == stations_on_route['sequence_number'].max()]['station_id (FK)'].iloc[0]
        
        first_station = stations[stations['station_id (PK)'] == first_station_id]['station_name'].iloc[0]
        last_station = stations[stations['station_id (PK)'] == last_station_id]['station_name'].iloc[0]
        
        print(f"   ▶️ From: {first_station}")
        print(f"   ■ To: {last_station}")

# Find stations with most connections
print("\n" + "-" * 40)
print("🔄 BUSIEST STATIONS (Most Connections)")
print("-" * 40)

station_connections = route_stations.groupby('station_id (FK)').size().reset_index(name='connection_count')
station_connections = station_connections.merge(
    stations[['station_id (PK)', 'station_name']], 
    left_on='station_id (FK)', 
    right_on='station_id (PK)'
)
top_stations = station_connections.nlargest(5, 'connection_count')

for _, station in top_stations.iterrows():
    print(f"   🚉 {station['station_name']}: {station['connection_count']} connections")

# Create chart
try:
    plt.figure(figsize=(10, 6))
    route_counts = route_stations.groupby('route_id (FK)').size()
    
    # Get route names
    route_names_dict = {}
    for _, route in routes.iterrows():
        route_names_dict[route['route_id (PK)']] = route['route_name']
    
    route_labels = [route_names_dict.get(rid, f"Route {rid}") for rid in route_counts.index]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    bars = plt.bar(range(len(route_counts)), route_counts.values, color=colors[:len(route_counts)])
    plt.xticks(range(len(route_counts)), route_labels, rotation=45, ha='right')
    plt.xlabel('Metro Routes', fontsize=12)
    plt.ylabel('Number of Stations', fontsize=12)
    plt.title('Number of Stations per Metro Route', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('route_analysis_chart.png', dpi=150)
    print("\n📊 Chart saved as 'route_analysis_chart.png'")
    print("   📁 Open this file to see the visualization!")
except Exception as e:
    print(f"\n⚠️ Could not create chart: {e}")

# Additional Statistics
print("\n" + "-" * 40)
print("📈 SYSTEM STATISTICS")
print("-" * 40)

# Average stops per route
avg_stops = route_stations.groupby('route_id (FK)').size().mean()
print(f"📊 Average stops per route: {avg_stops:.1f}")

# Total distance covered (if distance_to_next exists)
if 'distance_to_next' in route_stations.columns:
    total_distance = route_stations['distance_to_next'].sum()
    print(f"📏 Total network distance: {total_distance:.2f} km")

# Most connected station
most_connected = top_stations.iloc[0]
print(f"⭐ Most connected station: {most_connected['station_name']} ({most_connected['connection_count']} connections)")

print("\n" + "=" * 60)
print("✅ Analysis Complete!")
print("=" * 60)