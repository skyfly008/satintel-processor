"""Create mock precomputed masks to test the analysis pipeline"""
import sys
sys.path.insert(0, ".")

from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

def create_mock_mask_from_image(image_path: str, output_path: str):
    """Create a simple mask by thresholding the image (gray pixels = buildings)"""
    img = Image.open(image_path).convert('L')  # Grayscale
    img_array = np.array(img)
    
    # Threshold: buildings are gray (high intensity), vegetation is dark
    mask = (img_array > 120).astype(np.uint8)
    
    # Clean up small noise
    mask = ndimage.binary_opening(mask, iterations=2).astype(np.uint8)
    
    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, mask)
    
    # Count objects
    labeled, num_objects = ndimage.label(mask)
    total_pixels = mask.sum()
    
    return mask, num_objects, total_pixels

print("Creating mock masks for testing the analysis pipeline...\n")

# Process AREA_1 images
images = [
    ("data/imagery/AREA_1/2021-01-01.png", "data/masks/AREA_1/2021-01-01_mask.npy"),
    ("data/imagery/AREA_1/2023-01-01.png", "data/masks/AREA_1/2023-01-01_mask.npy"),
]

for img_path, mask_path in images:
    if not Path(img_path).exists():
        print(f"⚠️ Skipping {img_path} (not found)")
        continue
    
    print(f"Processing: {img_path}")
    mask, num_objects, total_pixels = create_mock_mask_from_image(img_path, mask_path)
    print(f"  ✅ Created: {mask_path}")
    print(f"     Shape: {mask.shape}")
    print(f"     Objects detected: {num_objects}")
    print(f"     Total pixels: {total_pixels}\n")

print("✅ Mock masks created successfully!")
print("\nNote: These are simplified masks based on intensity thresholding.")
print("For production, use SAM-based precompute_sample_masks.py (requires GPU/patience).")
