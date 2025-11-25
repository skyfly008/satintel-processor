"""Create a test image with simple shapes for SAM testing"""
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path

# Create a test image with buildings-like shapes
img = Image.new("RGB", (512, 512), color=(50, 100, 50))  # Green background (vegetation)
draw = ImageDraw.Draw(img)

# Draw some "buildings" (rectangles)
buildings = [
    ((50, 50), (100, 100)),    # Small building
    ((150, 75), (250, 175)),   # Medium building
    ((300, 100), (450, 250)),  # Large building
    ((100, 300), (180, 380)),  # Another building
    ((250, 350), (350, 450)),  # Bottom building
]

for (x1, y1), (x2, y2) in buildings:
    # Draw building with gray color
    draw.rectangle([x1, y1, x2, y2], fill=(180, 180, 180))
    # Add a darker roof
    draw.rectangle([x1, y1, x2, y1+10], fill=(80, 80, 80))

# Save test image
output_path = Path("data/cache/test_buildings.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
img.save(output_path)
print(f"Created test image: {output_path}")
print(f"Image size: {img.size}")
print(f"Contains {len(buildings)} rectangular buildings")
