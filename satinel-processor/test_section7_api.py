"""
Test Section 7: API Routers
Tests the FastAPI endpoints via HTTP requests.
"""
import requests
import time
import subprocess
import sys
from pathlib import Path

API_BASE = "http://localhost:8000"
SERVER_PROC = None


def start_server():
    """Start the FastAPI server in background"""
    global SERVER_PROC
    print("Starting FastAPI server...")
    SERVER_PROC = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to be ready
    max_wait = 10
    for i in range(max_wait):
        try:
            resp = requests.get(f"{API_BASE}/docs", timeout=1)
            if resp.status_code == 200:
                print(f"Server ready after {i+1} seconds")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    
    print("Server failed to start within timeout")
    return False


def stop_server():
    """Stop the FastAPI server"""
    global SERVER_PROC
    if SERVER_PROC:
        print("\nStopping server...")
        SERVER_PROC.terminate()
        SERVER_PROC.wait(timeout=5)


def test_root_endpoint():
    """Test GET / returns HTML"""
    print("\nTest 1: GET / (root endpoint)")
    print("-" * 70)
    
    try:
        resp = requests.get(f"{API_BASE}/")
        print(f"Status Code: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type')}")
        
        if resp.status_code == 200 and 'text/html' in resp.headers.get('content-type', ''):
            print("SUCCESS: Root endpoint returns HTML")
            if 'Satinel Processor' in resp.text:
                print("SUCCESS: HTML contains expected title")
            return True
        else:
            print("ERROR: Unexpected response")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_task_endpoint():
    """Test POST /api/task"""
    print("\nTest 2: POST /api/task (single task)")
    print("-" * 70)
    
    payload = {
        "task_id": "api_test_single",
        "area_id": "AREA_1",
        "date": "2023-01-01",
        "imagery_source": "static"
    }
    
    try:
        resp = requests.post(f"{API_BASE}/api/task", json=payload)
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Task ID: {data.get('task_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Building Count: {data.get('building_stats', {}).get('count')}")
            print(f"Overlay URL: {data.get('overlay_url')}")
            
            if data.get('status') == 'done' and data.get('building_stats'):
                print("SUCCESS: Task executed and returned building stats")
                return True
            else:
                print("ERROR: Incomplete response")
                return False
        else:
            print(f"ERROR: HTTP {resp.status_code}")
            print(resp.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_temporal_task():
    """Test POST /api/task with temporal comparison"""
    print("\nTest 3: POST /api/task (temporal comparison)")
    print("-" * 70)
    
    payload = {
        "task_id": "api_test_temporal",
        "area_id": "AREA_1",
        "date": "2023-01-01",
        "historical_date": "2021-01-01",
        "imagery_source": "static"
    }
    
    try:
        resp = requests.post(f"{API_BASE}/api/task", json=payload)
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Task ID: {data.get('task_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Building Count: {data.get('building_stats', {}).get('count')}")
            print(f"Change Stats:")
            change = data.get('change_stats', {})
            print(f"  New: {change.get('new')}")
            print(f"  Removed: {change.get('removed')}")
            print(f"  Activity Score: {change.get('activity_score')}")
            print(f"Overlay URL: {data.get('overlay_url')}")
            
            if data.get('status') == 'done' and change.get('activity_score') is not None:
                print("SUCCESS: Temporal task executed with change detection")
                return True
            else:
                print("ERROR: Incomplete temporal response")
                return False
        else:
            print(f"ERROR: HTTP {resp.status_code}")
            print(resp.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_docs_endpoint():
    """Test API docs are accessible"""
    print("\nTest 4: GET /docs (API documentation)")
    print("-" * 70)
    
    try:
        resp = requests.get(f"{API_BASE}/docs")
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            print("SUCCESS: API docs accessible at /docs")
            return True
        else:
            print("ERROR: Docs not accessible")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main():
    print("=" * 70)
    print("SECTION 7: API ROUTERS TEST")
    print("=" * 70)
    
    # Start server
    if not start_server():
        print("Failed to start server, aborting tests")
        return False
    
    try:
        # Run tests
        results = []
        results.append(test_root_endpoint())
        results.append(test_task_endpoint())
        results.append(test_temporal_task())
        results.append(test_docs_endpoint())
        
        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        passed = sum(results)
        total = len(results)
        print(f"Tests Passed: {passed}/{total}")
        
        if all(results):
            print("\nSection 7: API Routers - COMPLETE")
            print("\nEndpoints Working:")
            print("  GET /           - Serves index.html")
            print("  POST /api/task  - Executes analysis tasks")
            print("  GET /docs       - API documentation")
            return True
        else:
            print("\nSome tests failed")
            return False
            
    finally:
        stop_server()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
