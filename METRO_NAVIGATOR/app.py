from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load data from csv_files
stations_df = pd.read_csv('csv_files/Stations.csv')
routes_df = pd.read_csv('csv_files/Routes.csv')

print(f"✅ Loaded {len(stations_df)} stations")
print(f"✅ Loaded {len(routes_df)} routes")

@app.route('/')
def home():
    return jsonify({
        'message': '🚆 Metro Navigator API is Running!',
        'endpoints': {
            'stations': '/api/stations',
            'routes': '/api/routes',
            'search': '/api/search (POST)',
            'stats': '/api/stats'
        }
    })

@app.route('/api/stations', methods=['GET'])
def get_stations():
    stations = stations_df[['station_id (PK)', 'station_name']].to_dict('records')
    return jsonify({
        'success': True,
        'count': len(stations),
        'stations': stations
    })

@app.route('/api/routes', methods=['GET'])
def get_routes():
    routes = routes_df[['route_id (PK)', 'route_name', 'line_color']].to_dict('records')
    return jsonify({
        'success': True,
        'count': len(routes),
        'routes': routes
    })

@app.route('/api/search', methods=['POST'])
def search_route():
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    
    result = {
        'success': True,
        'source': source,
        'destination': destination,
        'estimated_time': '25 minutes',
        'number_of_stops': 5,
        'path': [source, 'Intermediate Station', destination]
    }
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'total_stations': len(stations_df),
        'total_routes': len(routes_df),
        'status': 'running'
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚆 METRO NAVIGATOR API")
    print("=" * 50)
    print(f"📍 Stations: {len(stations_df)}")
    print(f"📍 Routes: {len(routes_df)}")
    print("=" * 50)
    print("🌐 http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)