"""Create realistic sample satellite images for AREA_1 with buildings"""
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path
import random

def create_satellite_image(filename: str, num_buildings: int, add_noise: bool = True):
    """Create a synthetic satellite image with buildings"""
    # 512x512 RGB image
    img = Image.new("RGB", (512, 512), color=(60, 90, 50))  # Green/brown terrain
    draw = ImageDraw.Draw(img)
    
    # Add some terrain variation (roads, vegetation)
    # Main road
    draw.rectangle([200, 0, 220, 512], fill=(120, 120, 120))  # Vertical road
    draw.rectangle([0, 250, 512, 270], fill=(120, 120, 120))  # Horizontal road
    
    # Add vegetation patches
    for _ in range(10):
        x, y = random.randint(0, 450), random.randint(0, 450)
        size = random.randint(20, 60)
        color = (random.randint(40, 80), random.randint(80, 120), random.randint(40, 70))
        draw.ellipse([x, y, x+size, y+size], fill=color)
    
    # Generate random buildings
    for _ in range(num_buildings):
        # Building location (avoid roads)
        quadrant = random.choice(["TL", "TR", "BL", "BR"])
        if quadrant == "TL":
            x1 = random.randint(10, 180)
            y1 = random.randint(10, 230)
        elif quadrant == "TR":
            x1 = random.randint(240, 480)
            y1 = random.randint(10, 230)
        elif quadrant == "BL":
            x1 = random.randint(10, 180)
            y1 = random.randint(290, 480)
        else:  # BR
            x1 = random.randint(240, 480)
            y1 = random.randint(290, 480)
        
        # Building size
        width = random.randint(15, 50)
        height = random.randint(15, 50)
        x2, y2 = x1 + width, y1 + height
        
        # Building color (gray/white concrete)
        gray_val = random.randint(140, 200)
        building_color = (gray_val, gray_val, gray_val + random.randint(-10, 10))
        
        # Draw building
        draw.rectangle([x1, y1, x2, y2], fill=building_color, outline=(100, 100, 100), width=1)
        
        # Add roof shadow
        roof_dark = max(50, gray_val - 30)
        draw.rectangle([x1, y1, x2, y1 + 3], fill=(roof_dark, roof_dark, roof_dark))
    
    # Add noise for realism
    if add_noise:
        pixels = np.array(img)
        noise = np.random.randint(-15, 15, pixels.shape, dtype=np.int16)
        pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(pixels)
    
    # Save
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    
    print(f"✅ Created: {filename}")
    print(f"   Size: {img.size}, Buildings: ~{num_buildings}")
    return img


# Create sample images for AREA_1
print("Creating sample satellite imagery for AREA_1...\n")

# 2021 image - fewer buildings (older development)
img_2021 = create_satellite_image("data/imagery/AREA_1/2021-01-01.png", num_buildings=12)

# 2023 image - more buildings (new development)
img_2023 = create_satellite_image("data/imagery/AREA_1/2023-01-01.png", num_buildings=18)

print("\n✅ Sample imagery created successfully!")
print("\nThese synthetic images simulate:")
print("  - Satellite RGB imagery at ~10m/pixel resolution")
print("  - Buildings as gray/white rectangular structures")
print("  - Roads, vegetation, and terrain features")
print("  - Temporal change (2021: 12 buildings → 2023: 18 buildings)")
