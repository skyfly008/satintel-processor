"""
Test Section 6: Overlay Generation
Verifies visualization overlay generation for detections and temporal changes.
"""
import asyncio
import sys
from pathlib import Path

from app.models.schema import TaskRequest
from app.services.analysis import process_task


async def test_section6():
    print("=" * 70)
    print("SECTION 6: OVERLAY GENERATION TEST")
    print("=" * 70)
    
    # Test 1: Single-date overlay (red polygons for all detections)
    print("\nTest 1: Single-Date Overlay Generation")
    print("-" * 70)
    req_single = TaskRequest(
        task_id="overlay_single_test",
        area_id="AREA_1",
        date="2023-01-01",
        imagery_source="static"
    )
    
    resp_single = await process_task(req_single)
    print(f"Task ID: {resp_single.task_id}")
    print(f"   Status: {resp_single.status}")
    print(f"   Building Count: {resp_single.building_stats.count}")
    print(f"   Overlay URL: {resp_single.overlay_url}")
    
    if resp_single.overlay_url:
        overlay_path = Path(resp_single.overlay_url)
        if overlay_path.exists():
            print(f"   Overlay file created: {overlay_path.name}")
            print(f"   File size: {overlay_path.stat().st_size:,} bytes")
        else:
            print(f"   ERROR: Overlay file not found!")
            return False
    else:
        print("   ERROR: No overlay URL returned!")
        return False
    
    # Test 2: Temporal overlay (green for new, red for removed, yellow for unchanged)
    print("\nTest 2: Temporal Change Overlay Generation")
    print("-" * 70)
    req_temporal = TaskRequest(
        task_id="overlay_temporal_test",
        area_id="AREA_1",
        date="2023-01-01",
        historical_date="2021-01-01",
        imagery_source="static"
    )
    
    resp_temporal = await process_task(req_temporal)
    print(f"Task ID: {resp_temporal.task_id}")
    print(f"   Status: {resp_temporal.status}")
    print(f"   Building Stats:")
    print(f"     Count: {resp_temporal.building_stats.count}")
    print(f"     Total Area: {resp_temporal.building_stats.total_footprint_area:,.0f} m²")
    print(f"\n   Change Stats:")
    print(f"     New Buildings: {resp_temporal.change_stats.new}")
    print(f"     Removed Buildings: {resp_temporal.change_stats.removed}")
    print(f"     Unchanged Buildings: {resp_temporal.change_stats.unchanged}")
    print(f"     Activity Score: {resp_temporal.change_stats.activity_score}/100")
    print(f"\n   Overlay URL: {resp_temporal.overlay_url}")
    
    if resp_temporal.overlay_url:
        overlay_path = Path(resp_temporal.overlay_url)
        if overlay_path.exists():
            print(f"   Temporal overlay created: {overlay_path.name}")
            print(f"   File size: {overlay_path.stat().st_size:,} bytes")
        else:
            print(f"   ERROR: Temporal overlay file not found!")
            return False
    else:
        print("   ERROR: No overlay URL returned for temporal mode!")
        return False
    
    # Verify overlay directory structure
    print("\nVerifying Overlay Directory Structure")
    print("-" * 70)
    overlay_dir = Path("data/overlays/AREA_1")
    if overlay_dir.exists():
        overlay_files = list(overlay_dir.glob("*.png"))
        print(f"Overlay directory exists: {overlay_dir}")
        print(f"   Found {len(overlay_files)} overlay file(s):")
        for f in overlay_files:
            print(f"     - {f.name} ({f.stat().st_size:,} bytes)")
    else:
        print(f"ERROR: Overlay directory not found: {overlay_dir}")
        return False
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("Single-date overlay generation: WORKING")
    print("Temporal change overlay generation: WORKING")
    print("Overlay files saved to data/overlays/")
    print("\nOverlay Color Coding:")
    print("  Red: Removed buildings (temporal) or All buildings (single-date)")
    print("  Green: New buildings (temporal)")
    print("  Yellow: Unchanged buildings (temporal)")
    print("\nSection 6: Overlay Generation - COMPLETE!")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_section6())
    sys.exit(0 if success else 1)
