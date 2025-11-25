"""Test SAM object detection on cached imagery"""
import sys
from pathlib import Path

# Test if SAM checkpoint exists
checkpoint_path = Path("models/sam_vit_h_4b8939.pth")
print(f"Checking SAM checkpoint: {checkpoint_path}")
print(f"Exists: {checkpoint_path.exists()}")
if checkpoint_path.exists():
    size_gb = checkpoint_path.stat().st_size / (1024**3)
    print(f"Size: {size_gb:.2f} GB")

# Test detection on cached image
from satinel.object_model import detect_objects

cache_dir = Path("data/cache")
if cache_dir.exists():
    images = list(cache_dir.glob("*.png"))
    print(f"\nFound {len(images)} cached images")
    
    if images:
        test_image = images[0]
        print(f"\nTesting detection on: {test_image.name}")
        print("Running SAM detection (this may take 1-2 minutes)...")
        
        try:
            detections = detect_objects(
                str(test_image),
                checkpoint=str(checkpoint_path),
                automatic=True,
                min_area=10.0,
            )
            
            print(f"\n Detection complete!")
            print(f"Found {len(detections)} objects")
            
            if detections:
                print("\nFirst 5 detections:")
                for i, det in enumerate(detections[:5]):
                    area = det.get("area", 0)
                    bbox = det.get("bbox", [])
                    print(f"  {i+1}. Area: {area:.1f} pixels, BBox: {bbox}")
                
                total_area = sum(d.get("area", 0) for d in detections)
                print(f"\nTotal detected area: {total_area:.1f} pixels")
        
        except Exception as e:
            print(f"\n Detection failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("No cached images found. Run a dynamic fetch first.")
else:
    print("Cache directory not found.")
