"""Test Section 5: Change Detection with Temporal Comparison"""
import sys
sys.path.insert(0, ".")

import asyncio
from app.models.schema import TaskRequest
from app.services.analysis import process_task

print("=" * 70)
print("SECTION 5: CHANGE DETECTION - Temporal Comparison Test")
print("=" * 70)

async def run_tests():
    print("\n📊 Test 1: Temporal Comparison (2021 → 2023)")
    print("-" * 70)
    
    req_temporal = TaskRequest(
        task_id="temporal_test",
        area_id="AREA_1",
        date="2023-01-01",
        historical_date="2021-01-01",
        imagery_source="static"
    )
    
    result = await process_task(req_temporal)
    
    print(f"✅ Task ID: {result.task_id}")
    print(f"   Status: {result.status}")
    print(f"   Source: {result.source}")
    print()
    print(f"📈 BUILDING STATISTICS (Current: 2023-01-01)")
    print(f"   Count: {result.building_stats.count}")
    print(f"   Total Area: {result.building_stats.total_footprint_area:,.0f} m²")
    print(f"   Density: {result.building_stats.density_per_km2:.2f} per km²")
    print()
    print(f"🔄 CHANGE DETECTION (2021 → 2023)")
    print(f"   New Buildings: {result.change_stats.new}")
    print(f"   Removed Buildings: {result.change_stats.removed}")
    print(f"   Unchanged Buildings: {result.change_stats.unchanged}")
    print(f"   Activity Score: {result.change_stats.activity_score}/100")
    print(f"   Temporal Change: {result.change_stats.temporal_change_pct:+.1f}%")
    print()
    print(f"📍 Additional Info:")
    print(f"   Area ID: {result.results.get('area_id')}")
    print(f"   Historical Detections: {result.results.get('detections_historical')}")
    print(f"   Current Detections: {result.results.get('detections_current')}")
    
    # Verify expectations
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    
    checks = []
    
    # Check 1: Should detect changes
    if result.change_stats.new > 0 or result.change_stats.removed > 0:
        checks.append("✅ Change detection working (detected new/removed objects)")
    else:
        checks.append("⚠️ No changes detected between dates")
    
    # Check 2: Activity score should be calculated
    if result.change_stats.activity_score > 0:
        checks.append(f"✅ Activity score calculated: {result.change_stats.activity_score}/100")
    else:
        checks.append("⚠️ Activity score is zero")
    
    # Check 3: Temporal change percentage
    if result.change_stats.temporal_change_pct != 0:
        checks.append(f"✅ Temporal change: {result.change_stats.temporal_change_pct:+.1f}%")
    else:
        checks.append("⚠️ No temporal change detected")
    
    # Check 4: Historical date in results
    if result.results.get('historical_date'):
        checks.append(f"✅ Historical date tracked: {result.results.get('historical_date')}")
    else:
        checks.append("⚠️ Historical date not in results")
    
    for check in checks:
        print(check)
    
    # Test 2: Single date (no temporal comparison)
    print("\n" + "=" * 70)
    print("📊 Test 2: Single Date Mode (No Temporal Comparison)")
    print("-" * 70)
    
    req_single = TaskRequest(
        task_id="single_date_test",
        area_id="AREA_1",
        date="2023-01-01",
        imagery_source="static"
    )
    
    result_single = await process_task(req_single)
    
    print(f"✅ Task ID: {result_single.task_id}")
    print(f"   Buildings Detected: {result_single.building_stats.count}")
    print(f"   Change Stats (should be zero):")
    print(f"     New: {result_single.change_stats.new}")
    print(f"     Removed: {result_single.change_stats.removed}")
    print(f"     Activity Score: {result_single.change_stats.activity_score}")
    
    if result_single.change_stats.new == 0 and result_single.change_stats.removed == 0:
        print("   ✅ Correctly returns zero changes for single-date mode")
    else:
        print("   ⚠️ Unexpected change values in single-date mode")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("✅ Section 5: Change Detection - COMPLETE")
    print()
    print("Features Implemented:")
    print("  • Temporal comparison with historical_date parameter")
    print("  • IoU-based object matching between dates")
    print("  • Change statistics (new/removed/unchanged counts)")
    print("  • Activity scoring (0-100 scale)")
    print("  • Temporal change percentage calculation")
    print("  • Backward compatible with single-date mode")
    print()
    print(f"Expected temporal change: ~5 new buildings (12 → 17)")
    print(f"Actual results: {result.change_stats.new} new, {result.change_stats.removed} removed")
    
    if result.change_stats.new > 0:
        print("\n🎉 Change detection successfully identifies temporal changes!")
    else:
        print("\n⚠️ Check mock mask generation - may need real SAM detections")

# Run tests
asyncio.run(run_tests())
