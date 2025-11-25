"""Debug SAM detection with visualization"""
from pathlib import Path
from PIL import Image
import numpy as np

# Check cached image
cache_dir = Path("data/cache")
images = list(cache_dir.glob("*.png"))

if images:
    test_image = images[0]
    print(f"Testing image: {test_image.name}")
    
    # Load and check image
    img = Image.open(test_image)
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
    
    # Convert to array and check
    arr = np.array(img)
    print(f"Array shape: {arr.shape}")
    print(f"Array dtype: {arr.dtype}")
    print(f"Value range: {arr.min()} - {arr.max()}")
    
    # Check if image is all black or has content
    if arr.max() == 0:
        print("\n WARNING: Image is all black!")
    else:
        print(f"\n Image has content (mean pixel value: {arr.mean():.1f})")
    
    # Try SAM with different settings
    print("\n" + "="*60)
    print("Testing SAM with different parameters...")
    print("="*60)
    
    from satinel.object_model import detect_objects
    checkpoint = Path("models/sam_vit_h_4b8939.pth")
    
    # Test 1: Very low thresholds
    print("\nTest 1: Low thresholds")
    try:
        from samgeo import SamGeo
        sam = SamGeo(
            model_type="vit_h",
            checkpoint=str(checkpoint),
            automatic=True,
            sam_kwargs={
                "points_per_side": 16,  # Reduce grid
                "pred_iou_thresh": 0.7,  # Lower threshold
                "stability_score_thresh": 0.7,  # Lower threshold
            }
        )
        
        output = test_image.parent / f"{test_image.stem}_test_mask.tif"
        sam.generate(
            source=str(test_image),
            output=str(output),
            foreground=True,
            batch=False,
        )
        
        print(f" Mask generated: {output.exists()}")
        
        if output.exists():
            import rasterio
            with rasterio.open(output) as src:
                mask = src.read(1)
                print(f"Mask shape: {mask.shape}")
                print(f"Unique values: {np.unique(mask)}")
                print(f"Foreground pixels: {np.sum(mask > 0)}")
            output.unlink()  # Clean up
    
    except Exception as e:
        print(f" Test failed: {e}")
        import traceback
        traceback.print_exc()

else:
    print("No cached images found")
