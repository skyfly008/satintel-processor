"""Download SAM model weights"""
import urllib.request
from pathlib import Path
import sys

# SAM ViT-H model (largest, most accurate)
MODEL_URL = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
MODEL_PATH = Path("models/sam_vit_h_4b8939.pth")

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

if MODEL_PATH.exists():
    print(f"Model already exists at: {MODEL_PATH}")
    print(f"Size: {MODEL_PATH.stat().st_size / (1024**3):.2f} GB")
    sys.exit(0)

print(f"Downloading SAM model from: {MODEL_URL}")
print(f"Target: {MODEL_PATH}")
print("This will download ~2.4 GB and may take several minutes...")
print()

def progress_callback(block_num, block_size, total_size):
    downloaded = block_num * block_size
    percent = min(100, downloaded * 100 / total_size)
    mb_downloaded = downloaded / (1024 ** 2)
    mb_total = total_size / (1024 ** 2)
    sys.stdout.write(f"\rProgress: {percent:.1f}% ({mb_downloaded:.1f} MB / {mb_total:.1f} MB)")
    sys.stdout.flush()

try:
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH, progress_callback)
    print(f"\n\n✅ Download complete!")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"File size: {MODEL_PATH.stat().st_size / (1024**3):.2f} GB")
except Exception as e:
    print(f"\n\n❌ Download failed: {e}")
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    sys.exit(1)
