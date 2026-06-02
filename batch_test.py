import requests
import time

BASE_URL = "http://127.0.0.1:5000/api"

# Test route combinations
test_routes = [
    ("Saddar", "Faizabad"),
    ("Saddar", "I-8 Markaz"),
    ("G-9 Markaz", "F-7 Markaz"),
    ("Faizabad", "Saddar"),
    ("Saddar", "Convention Centre"),
    ("I-8 Markaz", "G-9 Markaz"),
    ("F-7 Markaz", "Faizabad"),
    ("Blue Area", "Aabpara"),
]

print("=" * 70)
print("BATCH ROUTE TESTING - METRO NAVIGATOR")
print("=" * 70)

# Check if server is running first
try:
    requests.get(f"{BASE_URL}/stats", timeout=2)
    print("Connected to Metro Navigator Server!\n")
except requests.exceptions.ConnectionError:
    print("Cannot connect to server!")
    print("Please run 'python app.py' first in another terminal.")
    exit(1)

results = []
success_count = 0
fail_count = 0

for source, destination in test_routes:
    print(f"\nTesting: {source} -> {destination}")
    
    start_time = time.time()
    try:
        response = requests.post(f"{BASE_URL}/search", 
                                json={"source": source, "destination": destination},
                                timeout=10)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   [PASS] Found! {data['number_of_stops']} stops, {data['estimated_time']}")
                print(f"   Path: {' -> '.join(data['path'][:3])}..." if len(data['path']) > 3 else f"   Path: {' -> '.join(data['path'])}")
                print(f"   Response: {response_time:.0f}ms")
                results.append({
                    'source': source,
                    'destination': destination,
                    'success': True,
                    'stops': data['number_of_stops'],
                    'path_length': len(data['path']),
                    'time_ms': response_time,
                    'estimated_time': data['estimated_time']
                })
                success_count += 1
            else:
                print(f"   [FAIL] Failed: {data.get('error', 'Unknown error')}")
                results.append({
                    'source': source,
                    'destination': destination,
                    'success': False,
                    'error': data.get('error', 'Unknown error')
                })
                fail_count += 1
        else:
            print(f"   [FAIL] HTTP Error: {response.status_code}")
            results.append({
                'source': source,
                'destination': destination,
                'success': False,
                'error': f"HTTP {response.status_code}"
            })
            fail_count += 1
    except requests.exceptions.Timeout:
        print(f"   [FAIL] Timeout!")
        results.append({'source': source, 'destination': destination, 'success': False, 'error': 'Timeout'})
        fail_count += 1
    except Exception as e:
        print(f"   [FAIL] Error: {str(e)}")
        results.append({'source': source, 'destination': destination, 'success': False, 'error': str(e)})
        fail_count += 1

# Summary Report
print("\n" + "=" * 70)
print("TEST SUMMARY REPORT")
print("=" * 70)

print(f"\nOVERALL STATISTICS:")
print(f"   Successful: {success_count}/{len(test_routes)}")
print(f"   Failed: {fail_count}/{len(test_routes)}")
print(f"   Success Rate: {(success_count/len(test_routes))*100:.1f}%")

if success_count > 0:
    avg_response = sum(r['time_ms'] for r in results if r.get('success')) / success_count
    avg_stops = sum(r['stops'] for r in results if r.get('success')) / success_count
    print(f"\nPERFORMANCE METRICS:")
    print(f"   Average Response Time: {avg_response:.0f}ms")
    print(f"   Average Number of Stops: {avg_stops:.1f}")

print("\nDETAILED RESULTS:")
print("-" * 70)
print(f"{'Source':<20} {'Destination':<20} {'Status':<10} {'Details':<20}")
print("-" * 70)

for result in results:
    source = result['source'][:18]
    dest = result['destination'][:18]
    if result['success']:
        status = "PASS"
        details = f"{result['stops']} stops, {result['time_ms']:.0f}ms"
    else:
        status = "FAIL"
        details = result.get('error', 'Unknown')[:18]
    print(f"{source:<20} {dest:<20} {status:<10} {details:<20}")

# Save results to file (without emojis)
print("\n" + "=" * 70)
print("SAVING RESULTS FOR REPORT")
print("=" * 70)

try:
    with open('batch_test_results.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("METRO NAVIGATOR - BATCH TEST RESULTS\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Tests: {len(test_routes)}\n")
        f.write(f"Successful: {success_count}\n")
        f.write(f"Failed: {fail_count}\n")
        f.write(f"Success Rate: {(success_count/len(test_routes))*100:.1f}%\n\n")
        
        if success_count > 0:
            f.write(f"Average Response Time: {avg_response:.0f}ms\n")
            f.write(f"Average Stops: {avg_stops:.1f}\n\n")
        
        f.write("DETAILED RESULTS:\n")
        f.write("-" * 70 + "\n")
        for result in results:
            if result['success']:
                f.write(f"[PASS] {result['source']} -> {result['destination']}: {result['stops']} stops, {result['time_ms']:.0f}ms\n")
            else:
                f.write(f"[FAIL] {result['source']} -> {result['destination']}: {result.get('error', 'Failed')}\n")
    
    print("Results saved to 'batch_test_results.txt'")
except Exception as e:
    print(f"Could not save file: {e}")

# Final recommendation
print("\n" + "=" * 70)
print("RECOMMENDATION")
print("=" * 70)

if success_count == len(test_routes):
    print("ALL TESTS PASSED! Your Metro Navigator is working perfectly!")
    print("You can confidently submit your project for the pre-mid report.")
elif success_count >= len(test_routes) * 0.7:
    print("MOST TESTS PASSED! Some routes need attention.")
else:
    print("MANY TESTS FAILED! Please check your server and data.")

print("\n" + "=" * 70)