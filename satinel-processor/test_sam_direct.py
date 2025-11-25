"""Quick test of SAM detection"""
import sys
sys.path.insert(0, ".")

from pathlib import Path
from samgeo import SamGeo
from PIL import Image

# Test on the simple test image
image_path = "data/cache/test_buildings.png"
checkpoint = "models/sam_vit_h_4b8939.pth"

print(f"Testing SAM directly on: {image_path}")
print(f"Image exists: {Path(image_path).exists()}")

# Check image
img = Image.open(image_path)
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}\n")

# Initialize SAM
print("Initializing SAM...")
sam = SamGeo(
    model_type="vit_h",
    checkpoint=checkpoint,
    automatic=True,
    sam_kwargs={
        "points_per_side": 16,  # Fewer points for faster testing
        "pred_iou_thresh": 0.70,
        "stability_score_thresh": 0.80,
    }
)
print("SAM initialized!\n")

# Generate masks
output_mask = "data/cache/test_output_mask.tif"
print(f"Generating masks to: {output_mask}")

try:
    sam.generate(
        source=image_path,
        output=output_mask,
        foreground=True,
        batch=True,
    )
    print(f"✅ Mask generation complete!")
    
    if Path(output_mask).exists():
        print(f"✅ Output file exists: {Path(output_mask).stat().st_size} bytes")
        
        # Try to read it
        import rasterio
        with rasterio.open(output_mask) as src:
            mask = src.read(1)
            print(f"✅ Mask shape: {mask.shape}")
            print(f"✅ Non-zero pixels: {(mask > 0).sum()}")
            print(f"✅ Unique values: {set(mask.flatten().tolist()[:100])}")
    else:
        print("⚠️ Output file does not exist")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
