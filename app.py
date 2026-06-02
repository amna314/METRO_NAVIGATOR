from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import hashlib
import uuid
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# ============================================================
# DATA LOADING
# ============================================================

# Load CSV files
stations_df = pd.read_csv('csv_files/Stations.csv')
routes_df = pd.read_csv('csv_files/Routes.csv')
route_stations_df = pd.read_csv('csv_files/Route_Stations.csv')

# Load or create Users CSV
users_file = 'csv_files/Users.csv'
if not os.path.exists(users_file):
    pd.DataFrame(columns=['user_id', 'name', 'email', 'password_hash', 'role', 'created_at']).to_csv(users_file, index=False)

# Load or create Feedback CSV
feedback_file = 'csv_files/Feedback.csv'
if not os.path.exists(feedback_file):
    pd.DataFrame(columns=['feedback_id', 'user_id', 'message', 'rating', 'created_at', 'status']).to_csv(feedback_file, index=False)

# Load or create Travel History CSV
history_file = 'csv_files/Travel_History.csv'
if not os.path.exists(history_file):
    pd.DataFrame(columns=['history_id', 'user_id', 'source_station', 'destination_station', 'route_id', 'travel_date', 'estimated_time', 'actual_time']).to_csv(history_file, index=False)

# Load or create Notifications CSV
notifications_file = 'csv_files/Notifications.csv'
if not os.path.exists(notifications_file):
    pd.DataFrame(columns=['notification_id', 'user_id', 'title', 'message', 'type', 'created_at', 'is_read']).to_csv(notifications_file, index=False)

print("=" * 60)
print("🚆 AI-POWERED METRO BUS NAVIGATOR")
print("=" * 60)
print(f"✅ Loaded {len(stations_df)} stations")
print(f"✅ Loaded {len(routes_df)} routes")
print(f"✅ Loaded {len(route_stations_df)} connections")
print("=" * 60)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def build_graph():
    """Build graph for Dijkstra algorithm"""
    graph = {}
    for _, station in stations_df.iterrows():
        station_id = station['station_id (PK)']
        graph[station_id] = []
    
    for _, rs in route_stations_df.iterrows():
        from_id = rs['station_id (FK)']
        # Find next station on same route
        route_id = rs['route_id (FK)']
        same_route = route_stations_df[route_stations_df['route_id (FK)'] == route_id]
        current_seq = rs['sequence_number']
        next_station = same_route[same_route['sequence_number'] == current_seq + 1]
        
        if not next_station.empty:
            to_id = next_station.iloc[0]['station_id (FK)']
            time = rs.get('time_to_next', 2)
            graph[from_id].append({'to': to_id, 'weight': float(time) if pd.notna(time) else 2})
            graph[to_id].append({'to': from_id, 'weight': float(time) if pd.notna(time) else 2})
    
    return graph

def dijkstra(graph, start, end):
    """Find shortest path using Dijkstra's algorithm"""
    import heapq
    
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current == end:
            break
        
        if current_dist > distances[current]:
            continue
        
        for neighbor in graph[current]:
            distance = current_dist + neighbor['weight']
            if distance < distances[neighbor['to']]:
                distances[neighbor['to']] = distance
                previous[neighbor['to']] = current
                heapq.heappush(pq, (distance, neighbor['to']))
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    
    if not path or path[0] != start:
        return []
    return path

def get_station_name(station_id):
    """Get station name from ID"""
    station = stations_df[stations_df['station_id (PK)'] == station_id]
    if not station.empty:
        return station.iloc[0]['station_name']
    return str(station_id)

# ============================================================
# API 1: USER REGISTRATION
# ============================================================

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    # Check if user already exists
    users_df = pd.read_csv(users_file)
    if email in users_df['email'].values:
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    
    # Create new user
    user_id = f"U{str(uuid.uuid4())[:4].upper()}"
    new_user = pd.DataFrame([{
        'user_id': user_id,
        'name': name,
        'email': email,
        'password_hash': hash_password(password),
        'role': 'user',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(users_file, index=False)
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user_id': user_id,
        'name': name
    })

# ============================================================
# API 2: USER LOGIN
# ============================================================

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user login"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    users_df = pd.read_csv(users_file)
    user = users_df[users_df['email'] == email]
    
    if user.empty:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    if user.iloc[0]['password_hash'] != hash_password(password):
        return jsonify({'success': False, 'message': 'Invalid password'}), 401
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user_id': user.iloc[0]['user_id'],
        'name': user.iloc[0]['name'],
        'role': user.iloc[0]['role']
    })

# ============================================================
# API 3: GET ALL STATIONS
# ============================================================

@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Get all metro stations"""
    stations = stations_df[['station_id (PK)', 'station_name']].to_dict('records')
    return jsonify({
        'success': True,
        'count': len(stations),
        'stations': stations
    })

# ============================================================
# API 4: GET ALL ROUTES
# ============================================================

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Get all metro routes"""
    routes = routes_df[['route_id (PK)', 'route_name', 'line_color']].to_dict('records')
    return jsonify({
        'success': True,
        'count': len(routes),
        'routes': routes
    })

# ============================================================
# API 5: SEARCH ROUTE (CORE FUNCTIONALITY)
# ============================================================

@app.route('/api/search', methods=['POST'])
def search_route():
    """Find optimal route between stations"""
    data = request.json
    source_name = data.get('source')
    dest_name = data.get('destination')
    user_id = data.get('user_id', None)
    
    if not source_name or not dest_name:
        return jsonify({'success': False, 'error': 'Source and destination required'}), 400
    
    # Find station IDs
    source = stations_df[stations_df['station_name'].str.contains(source_name, case=False)]
    dest = stations_df[stations_df['station_name'].str.contains(dest_name, case=False)]
    
    if source.empty:
        return jsonify({'success': False, 'error': f'Station "{source_name}" not found'}), 404
    if dest.empty:
        return jsonify({'success': False, 'error': f'Station "{dest_name}" not found'}), 404
    
    source_id = source.iloc[0]['station_id (PK)']
    dest_id = dest.iloc[0]['station_id (PK)']
    
    # Find path using Dijkstra
    graph = build_graph()
    path_ids = dijkstra(graph, source_id, dest_id)
    
    if not path_ids:
        return jsonify({'success': False, 'error': 'No route found'}), 404
    
    # Convert IDs to names
    path_names = [get_station_name(sid) for sid in path_ids]
    
    # Calculate total time
    total_time = len(path_names) * 3  # 3 minutes per stop average
    
    # Save to travel history if user_id provided
    if user_id:
        history_df = pd.read_csv(history_file)
        new_history = pd.DataFrame([{
            'history_id': str(uuid.uuid4())[:8],
            'user_id': user_id,
            'source_station': source_name,
            'destination_station': dest_name,
            'route_id': 'RT01',
            'travel_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estimated_time': total_time,
            'actual_time': None
        }])
        history_df = pd.concat([history_df, new_history], ignore_index=True)
        history_df.to_csv(history_file, index=False)
    
    return jsonify({
        'success': True,
        'source': source_name,
        'destination': dest_name,
        'path': path_names,
        'number_of_stops': len(path_names) - 1,
        'number_of_stations': len(path_names),
        'estimated_time': f"{total_time} minutes",
        'total_time_minutes': total_time,
        'message': f"Found route from {source_name} to {dest_name}"
    })

# ============================================================
# API 6: SUBMIT FEEDBACK
# ============================================================

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')
    rating = data.get('rating')
    
    if not user_id or not message or not rating:
        return jsonify({'success': False, 'message': 'All fields required'}), 400
    
    feedback_df = pd.read_csv(feedback_file)
    new_feedback = pd.DataFrame([{
        'feedback_id': str(uuid.uuid4())[:8],
        'user_id': user_id,
        'message': message,
        'rating': rating,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'pending'
    }])
    
    feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
    feedback_df.to_csv(feedback_file, index=False)
    
    return jsonify({
        'success': True,
        'message': 'Feedback submitted successfully'
    })

# ============================================================
# API 7: GET FEEDBACK (for user)
# ============================================================

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """Get user's own feedback"""
    user_id = request.args.get('user_id')
    
    feedback_df = pd.read_csv(feedback_file)
    user_feedback = feedback_df[feedback_df['user_id'] == user_id].to_dict('records')
    
    return jsonify({
        'success': True,
        'feedback': user_feedback
    })

# ============================================================
# API 8: GET TRAVEL HISTORY
# ============================================================

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get user's travel history"""
    user_id = request.args.get('user_id')
    
    history_df = pd.read_csv(history_file)
    user_history = history_df[history_df['user_id'] == user_id].to_dict('records')
    
    return jsonify({
        'success': True,
        'history': user_history
    })

# ============================================================
# API 9: SAVE TRAVEL HISTORY
# ============================================================

@app.route('/api/history', methods=['POST'])
def save_history():
    """Save a trip to history"""
    data = request.json
    user_id = data.get('user_id')
    source = data.get('source')
    destination = data.get('destination')
    estimated_time = data.get('estimated_time')
    
    history_df = pd.read_csv(history_file)
    new_history = pd.DataFrame([{
        'history_id': str(uuid.uuid4())[:8],
        'user_id': user_id,
        'source_station': source,
        'destination_station': destination,
        'route_id': 'RT01',
        'travel_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'estimated_time': estimated_time,
        'actual_time': None
    }])
    
    history_df = pd.concat([history_df, new_history], ignore_index=True)
    history_df.to_csv(history_file, index=False)
    
    return jsonify({
        'success': True,
        'message': 'Trip saved to history'
    })

# ============================================================
# API 10: GET NOTIFICATIONS
# ============================================================

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Get user notifications"""
    user_id = request.args.get('user_id')
    
    notifications_df = pd.read_csv(notifications_file)
    user_notifications = notifications_df[notifications_df['user_id'] == user_id].to_dict('records')
    
    # Also add some default notifications if none exist
    if len(user_notifications) == 0:
        default_notifications = [
            {'notification_id': 'N001', 'user_id': user_id, 'title': 'Welcome!', 'message': 'Welcome to Metro Navigator!', 'type': 'info', 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'is_read': 'no'},
            {'notification_id': 'N002', 'user_id': user_id, 'title': 'Route Update', 'message': 'Red Line service is operating normally.', 'type': 'info', 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'is_read': 'no'},
        ]
        return jsonify({'success': True, 'notifications': default_notifications})
    
    return jsonify({
        'success': True,
        'notifications': user_notifications
    })

# ============================================================
# API 11: MARK NOTIFICATION AS READ
# ============================================================

@app.route('/api/notifications/read', methods=['POST'])
def mark_notification_read():
    """Mark a notification as read"""
    data = request.json
    notification_id = data.get('notification_id')
    user_id = data.get('user_id')
    
    notifications_df = pd.read_csv(notifications_file)
    notifications_df.loc[notifications_df['notification_id'] == notification_id, 'is_read'] = 'yes'
    notifications_df.to_csv(notifications_file, index=False)
    
    return jsonify({'success': True, 'message': 'Notification marked as read'})

# ============================================================
# API 12: SYSTEM STATS
# ============================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    return jsonify({
        'success': True,
        'total_stations': len(stations_df),
        'total_routes': len(routes_df),
        'total_connections': len(route_stations_df),
        'status': 'running',
        'version': '2.0'
    })

# ============================================================
# RUN THE APP
# ============================================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🌐 SERVER RUNNING")
    print("=" * 60)
    print("📍 http://127.0.0.1:5000")
    print("📍 http://127.0.0.1:5000/api/stations")
    print("📍 http://127.0.0.1:5000/api/routes")
    print("📍 http://127.0.0.1:5000/api/stats")
    print("=" * 60)
    print("\n📋 AVAILABLE APIs:")
    print("   POST /api/register - User Registration")
    print("   POST /api/login - User Login")
    print("   GET  /api/stations - List Stations")
    print("   GET  /api/routes - List Routes")
    print("   POST /api/search - Find Route")
    print("   POST /api/feedback - Submit Feedback")
    print("   GET  /api/feedback - Get Feedback")
    print("   GET  /api/history - Travel History")
    print("   POST /api/history - Save to History")
    print("   GET  /api/notifications - Get Notifications")
    print("   GET  /api/stats - System Stats")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)