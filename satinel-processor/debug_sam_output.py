"""Debug SAM mask generation"""
from pathlib import Path
from samgeo import SamGeo
import numpy as np

test_image = Path("data/cache/test_buildings.png")
checkpoint = Path("models/sam_vit_h_4b8939.pth")
output_mask = Path("data/cache/test_mask_debug.tif")

print("Initializing SAM...")
sam = SamGeo(
    model_type="vit_h",
    checkpoint=str(checkpoint),
    automatic=True,
    sam_kwargs={
        "points_per_side": 16,
        "pred_iou_thresh": 0.7,
        "stability_score_thresh": 0.7,
    }
)

print("Generating masks...")
sam.generate(
    source=str(test_image),
    output=str(output_mask),
    foreground=True,
    batch=False,
)

print(f"\nChecking output: {output_mask.exists()}")

if output_mask.exists():
    import rasterio
    with rasterio.open(output_mask) as src:
        print(f"Bands: {src.count}")
        print(f"Shape: {src.shape}")
        print(f"Dtype: {src.dtypes}")
        
        mask = src.read(1)
        print(f"\nMask array shape: {mask.shape}")
        print(f"Mask dtype: {mask.dtype}")
        print(f"Unique values: {np.unique(mask)}")
        print(f"Non-zero pixels: {np.sum(mask != 0)}")
        print(f"Value counts:")
        unique, counts = np.unique(mask, return_counts=True)
        for val, count in zip(unique, counts):
            print(f"  {val}: {count} pixels")
    
    # Check what samgeo internal state has
    print(f"\nSAM object attributes:")
    if hasattr(sam, 'masks'):
        print(f"  masks: {type(sam.masks)}, length: {len(sam.masks) if sam.masks else 0}")
    if hasattr(sam, 'prediction'):
        print(f"  prediction: {sam.prediction is not None}")
    
else:
    print("Mask file not generated!")
