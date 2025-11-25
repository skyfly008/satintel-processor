"""Test with simplified SAM approach - using ViT-B (smaller/faster model)"""
import sys
sys.path.insert(0, ".")

from pathlib import Path
from satinel.object_model import detect_objects

# Test with simple image
test_image = "data/cache/test_buildings.png"

print(f"Testing SAM detection on: {test_image}")
print("Using automatic segmentation...\n")

try:
    # Use detect_objects with automatic mode
    detections = detect_objects(
        test_image,
        prompt="buildings infrastructure",
        model_type="vit_h",  # Use the downloaded model
        checkpoint="models/sam_vit_h_4b8939.pth",
        automatic=True,
        min_area=50.0,
    )
    
    print(f"✅ Detection complete!")
    print(f"Found {len(detections)} objects\n")
    
    if detections:
        print("Detections:")
        for i, det in enumerate(detections[:10]):
            area = det.get("area", 0)
            bbox = det.get("bbox", [])
            if bbox:
                width = bbox[2] - bbox[0]
                height = bbox[3] - bbox[1]
                print(f"  {i+1}. Area: {area:.0f} px, BBox: ({width:.1f}x{height:.1f})")
        
        total_area = sum(d.get("area", 0) for d in detections)
        print(f"\n✅ SUCCESS: {len(detections)} objects detected")
        print(f"   Total area: {total_area:.0f} pixels")
    else:
        print("⚠️ No objects detected")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
