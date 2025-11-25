"""
Test Section 8 API: Batch endpoint via HTTP
"""
import requests
import subprocess
import sys
import time

API_BASE = "http://localhost:8000"
SERVER_PROC = None


def start_server():
    """Start FastAPI server"""
    global SERVER_PROC
    print("Starting FastAPI server...")
    SERVER_PROC = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    for i in range(10):
        try:
            resp = requests.get(f"{API_BASE}/docs", timeout=1)
            if resp.status_code == 200:
                print(f"Server ready after {i+1} seconds")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    
    return False


def stop_server():
    """Stop server"""
    global SERVER_PROC
    if SERVER_PROC:
        print("\nStopping server...")
        SERVER_PROC.terminate()
        SERVER_PROC.wait(timeout=5)


def test_batch_endpoint():
    """Test POST /api/batch_task"""
    print("\nTest: POST /api/batch_task")
    print("-" * 70)
    
    payload = {
        "tasks": [
            {
                "task_id": "api_batch_1",
                "area_id": "AREA_1",
                "date": "2021-01-01",
                "imagery_source": "static"
            },
            {
                "task_id": "api_batch_2",
                "area_id": "AREA_1",
                "date": "2023-01-01",
                "imagery_source": "static"
            },
            {
                "task_id": "api_batch_3_temporal",
                "area_id": "AREA_1",
                "date": "2023-01-01",
                "historical_date": "2021-01-01",
                "imagery_source": "static"
            }
        ]
    }
    
    try:
        resp = requests.post(f"{API_BASE}/api/batch_task", json=payload, timeout=30)
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Batch ID: {data.get('batch_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Total Tasks: {data.get('total_tasks')}")
            print(f"Completed: {data.get('completed')}")
            print(f"Failed: {data.get('failed')}")
            
            agg = data.get('aggregate_stats', {})
            if agg:
                print("\nAggregate Stats:")
                print(f"  Total Detections: {agg.get('total_detections')}")
                print(f"  Total Area: {agg.get('total_area_m2'):,.0f} m2")
                print(f"  Total New: {agg.get('total_new')}")
                print(f"  Total Removed: {agg.get('total_removed')}")
                print(f"  Processing Time: {agg.get('processing_time_seconds')} sec")
                
                hotspots = agg.get('hotspots', [])
                if hotspots:
                    print(f"  Hotspots: {len(hotspots)}")
            
            print("\nTask Results:")
            for task in data.get('task_results', []):
                print(f"  {task.get('task_id')}: {task.get('status')}")
            
            return True
        else:
            print(f"ERROR: HTTP {resp.status_code}")
            print(resp.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main():
    print("=" * 70)
    print("SECTION 8: BATCH API TEST")
    print("=" * 70)
    
    if not start_server():
        print("Failed to start server")
        return False
    
    try:
        success = test_batch_endpoint()
        
        print("\n" + "=" * 70)
        if success:
            print("SUCCESS: Batch API endpoint working correctly")
        else:
            print("FAILED: Batch API test failed")
        print("=" * 70)
        
        return success
    finally:
        stop_server()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
