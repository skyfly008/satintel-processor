"""
Setup script to create required directory structure for ASIP data acquisition.
"""

from pathlib import Path

# Define base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'

# AOI directories
AOIS = [
    'nyc_manhattan',
    'nyc_jfk',
    'nyc_industrial',
    'tehran_central',
    'tehran_airport',
    'tehran_industrial'
]

# Other data directories
OTHER_DIRS = [
    'masks',
    'cache',
    'metadata'
]

def setup_directories():
    """Create all required directories."""
    print("Setting up ASIP directory structure...")
    print()
    
    # Create imagery directories
    print("Creating imagery directories:")
    imagery_dir = DATA_DIR / 'imagery'
    for aoi in AOIS:
        aoi_dir = imagery_dir / aoi
        aoi_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {aoi_dir}")
    
    print()
    
    # Create other data directories
    print("Creating other data directories:")
    for dir_name in OTHER_DIRS:
        dir_path = DATA_DIR / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dir_path}")
    
    print()
    print("✓ Directory structure ready!")
    print()
    print("Next steps:")
    print("1. Run: python scripts\\test_api.py")
    print("2. Run: python scripts\\download_imagery.py")

if __name__ == '__main__':
    setup_directories()
