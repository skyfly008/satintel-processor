"""Precompute SAM masks for sample images in AREA_1"""
import sys
sys.path.insert(0, ".")

from pathlib import Path
from satinel.object_model import precompute_masks

# Sample images
images = [
    ("data/imagery/AREA_1/2021-01-01.png", "data/masks/AREA_1/2021-01-01_mask.npy"),
    ("data/imagery/AREA_1/2023-01-01.png", "data/masks/AREA_1/2023-01-01_mask.npy"),
]

checkpoint = "models/sam_vit_h_4b8939.pth"

print("Precomputing masks for sample imagery...")
print(f"Using checkpoint: {checkpoint}\n")

for img_path, mask_path in images:
    if not Path(img_path).exists():
        print(f"⚠️ Skipping {img_path} (not found)")
        continue
    
    print(f"Processing: {img_path}")
    print(f"  Output: {mask_path}")
    
    try:
        mask = precompute_masks(
            img_path,
            mask_path,
            prompt="buildings infrastructure",
            checkpoint=checkpoint,
            automatic=True,
        )
        
        if mask is not None:
            print(f"  ✅ Mask saved: {mask.shape}, {mask.sum()} pixels detected\n")
        else:
            print(f"  ⚠️ No detections found\n")
    
    except Exception as e:
        print(f"  ❌ Failed: {e}\n")
        import traceback
        traceback.print_exc()

print("\n✅ Precomputation complete!")
