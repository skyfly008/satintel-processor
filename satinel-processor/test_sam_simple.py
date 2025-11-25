"""Test SAM on synthetic test image"""
from pathlib import Path
from satinel.object_model import detect_objects

test_image = Path("data/cache/test_buildings.png")
checkpoint = Path("models/sam_vit_h_4b8939.pth")

print(f"Testing SAM on: {test_image.name}")
print("Running detection (may take 1-2 minutes)...\n")

try:
    detections = detect_objects(
        str(test_image),
        checkpoint=str(checkpoint),
        automatic=True,
        min_area=50.0,  # Filter very small detections
    )
    
    print(f" Detection complete!")
    print(f"Found {len(detections)} objects\n")
    
    if detections:
        print("Detections:")
        for i, det in enumerate(detections[:10]):
            area = det.get("area", 0)
            bbox = det.get("bbox", [])
            if bbox:
                width = bbox[2] - bbox[0]
                height = bbox[3] - bbox[1]
                print(f"  {i+1}. Area: {area:.0f} px, Size: {width:.0f}x{height:.0f}")
            else:
                print(f"  {i+1}. Area: {area:.0f} px")
        
        total_area = sum(d.get("area", 0) for d in detections)
        print(f"\nTotal: {total_area:.0f} pixels across {len(detections)} objects")
    else:
        print("No objects detected. SAM may need parameter tuning.")

except Exception as e:
    print(f" Detection failed: {e}")
    import traceback
    traceback.print_exc()
