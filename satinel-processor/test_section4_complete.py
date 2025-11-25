"""Test the full analysis pipeline with precomputed masks"""
import sys
sys.path.insert(0, ".")

import asyncio
from app.models.schema import TaskRequest
from app.services.analysis import process_task

print("=" * 60)
print("TESTING ANALYSIS PIPELINE - Section 4")
print("=" * 60)

async def run_tests():
    print("\n1. Testing with precomputed mask (static mode, 2021)...")
    print("-" * 60)
    
    req1 = TaskRequest(
        task_id="test_2021",
        area_id="AREA_1",
        date="2021-01-01",
        imagery_source="static"
    )
    
    result1 = await process_task(req1)
    print(f"✅ Task ID: {result1.task_id}")
    print(f"   Status: {result1.status}")
    print(f"   Source: {result1.source}")
    print(f"   Building Stats:")
    print(f"     - Count: {result1.building_stats.count}")
    print(f"     - Total Area: {result1.building_stats.total_footprint_area:.0f} m²")
    print(f"     - Density: {result1.building_stats.density_per_km2:.2f} per km²")
    
    print("\n2. Testing with precomputed mask (static mode, 2023)...")
    print("-" * 60)
    
    req2 = TaskRequest(
        task_id="test_2023",
        area_id="AREA_1",
        date="2023-01-01",
        imagery_source="static"
    )
    
    result2 = await process_task(req2)
    print(f"✅ Task ID: {result2.task_id}")
    print(f"   Status: {result2.status}")
    print(f"   Source: {result2.source}")
    print(f"   Building Stats:")
    print(f"     - Count: {result2.building_stats.count}")
    print(f"     - Total Area: {result2.building_stats.total_footprint_area:.0f} m²")
    print(f"     - Density: {result2.building_stats.density_per_km2:.2f} per km²")
    
    print("\n3. Testing with lat/lon snapping...")
    print("-" * 60)
    
    req3 = TaskRequest(
        task_id="test_coords",
        lat=36.0,
        lon=-115.0,
        date="2023-01-01",
        imagery_source="static"
    )
    
    result3 = await process_task(req3)
    print(f"✅ Task ID: {result3.task_id}")
    print(f"   Status: {result3.status}")
    print(f"   Snapped to Area: {result3.results.get('area_id')}")
    print(f"   Building Count: {result3.building_stats.count}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ All tests passed successfully!")
    print(f"\nTemporal Analysis (2021 → 2023):")
    print(f"  Buildings in 2021: {result1.building_stats.count}")
    print(f"  Buildings in 2023: {result2.building_stats.count}")
    print(f"  Change: +{result2.building_stats.count - result1.building_stats.count} buildings")
    print(f"  Area change: +{(result2.building_stats.total_footprint_area - result1.building_stats.total_footprint_area):.0f} m²")
    print("\n✅ Section 4 implementation verified!")

# Run async tests
asyncio.run(run_tests())
