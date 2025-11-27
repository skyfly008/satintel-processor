"""
Data Acquisition Script for ASIP
Predownload satellite imagery from Sentinel-2 and USGS Landsat for specified AOIs.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SENTINEL_INSTANCE_ID = os.getenv('SENTINEL_INSTANCE_ID')
SENTINEL_CLIENT_ID = os.getenv('SENTINEL_CLIENT_ID')
SENTINEL_CLIENT_SECRET = os.getenv('SENTINEL_CLIENT_SECRET')
USGS_USERNAME = os.getenv('USGS_USERNAME', '')  # Optional
USGS_PASSWORD = os.getenv('USGS_PASSWORD', '')  # Optional

DATA_DIR = Path(os.getenv('DATA_DIR', 'data'))
IMAGERY_DIR = DATA_DIR / 'imagery'
METADATA_DIR = DATA_DIR / 'metadata'

# Areas of Interest (AOIs)
AOIS = {
    'nyc_manhattan': {
        'name': 'Manhattan Urban Core',
        'bbox': [-74.02, 40.70, -73.92, 40.85],  # [lon_min, lat_min, lon_max, lat_max]
        'description': 'Dense urban buildings',
        'mgrs': '18TWL'
    },
    'nyc_jfk': {
        'name': 'JFK Airport',
        'bbox': [-73.82, 40.62, -73.76, 40.66],
        'description': 'Airport infrastructure',
        'mgrs': '18TWL'
    },
    'nyc_industrial': {
        'name': 'Industrial Brooklyn',
        'bbox': [-73.95, 40.65, -73.90, 40.70],
        'description': 'Warehouses and factories',
        'mgrs': '18TWL'
    },
    'tehran_central': {
        'name': 'Tehran Central Urban',
        'bbox': [51.35, 35.68, 51.45, 35.75],
        'description': 'Dense residential/commercial',
        'mgrs': '40SUC'
    },
    'tehran_airport': {
        'name': 'Tehran International Airport',
        'bbox': [51.10, 35.40, 51.20, 35.45],
        'description': 'Airfield infrastructure',
        'mgrs': '40SUC'
    },
    'tehran_industrial': {
        'name': 'Tehran Industrial Outskirts',
        'bbox': [51.25, 35.65, 51.35, 35.70],
        'description': 'Factories and expansion areas',
        'mgrs': '40SUC'
    }
}

# Date ranges for imagery
DATE_RANGES = [
    ('2023-01-01', '2023-01-31'),
    ('2023-06-01', '2023-06-30')
]

# Image configuration
IMAGE_SIZE = [512, 512]  # Width, Height
MAX_CLOUD_COVER = 10  # Percentage


def setup_directories():
    """Create directory structure for storing imagery."""
    print("Setting up directory structure...")
    
    for aoi_id in AOIS.keys():
        aoi_dir = IMAGERY_DIR / aoi_id
        aoi_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {aoi_dir}")
    
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  Created: {METADATA_DIR}")
    print()


def download_sentinel2_imagery():
    """Download Sentinel-2 imagery for all AOIs."""
    try:
        from sentinelhub import SHConfig, SentinelHubRequest, MimeType, CRS, BBox, DataCollection
        from PIL import Image
        import numpy as np
    except ImportError:
        print("ERROR: sentinelhub or PIL not installed.")
        print("Please install: pip install sentinelhub Pillow")
        return False
    
    print("Configuring Sentinel Hub API...")
    config = SHConfig()
    
    if not SENTINEL_INSTANCE_ID or not SENTINEL_CLIENT_ID or not SENTINEL_CLIENT_SECRET:
        print("ERROR: Sentinel Hub credentials not found in .env file")
        print("Please set SENTINEL_INSTANCE_ID, SENTINEL_CLIENT_ID, SENTINEL_CLIENT_SECRET")
        return False
    
    config.instance_id = SENTINEL_INSTANCE_ID
    config.sh_client_id = SENTINEL_CLIENT_ID
    config.sh_client_secret = SENTINEL_CLIENT_SECRET
    
    # Evalscript for true color RGB with enhancement
    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: ["B02", "B03", "B04", "SCL"],
            output: { bands: 3, sampleType: "AUTO" }
        };
    }

    function evaluatePixel(sample) {
        // Enhanced true color
        return [sample.B04 * 2.5, sample.B03 * 2.5, sample.B02 * 2.5];
    }
    """
    
    metadata = []
    
    for aoi_id, aoi_data in AOIS.items():
        print(f"\nProcessing AOI: {aoi_id} ({aoi_data['name']})")
        
        bbox = BBox(bbox=aoi_data['bbox'], crs=CRS.WGS84)
        
        for date_start, date_end in DATE_RANGES:
            print(f"  Date range: {date_start} to {date_end}")
            
            try:
                request = SentinelHubRequest(
                    evalscript=evalscript,
                    input_data=[{
                        'type': DataCollection.SENTINEL2_L2A,
                        'dataFilter': {
                            'maxCloudCoverage': MAX_CLOUD_COVER
                        },
                        'time_interval': (date_start, date_end)
                    }],
                    responses=[{
                        'identifier': 'default',
                        'format': {'type': MimeType.PNG}
                    }],
                    bbox=bbox,
                    size=IMAGE_SIZE,
                    config=config
                )
                
                # Get data
                images = request.get_data()
                
                if images and len(images) > 0:
                    # Save the first (most recent) cloud-free image
                    image_array = images[0]
                    
                    # Convert to PIL Image
                    if image_array.dtype == np.float32 or image_array.dtype == np.float64:
                        image_array = (np.clip(image_array, 0, 1) * 255).astype(np.uint8)
                    
                    img = Image.fromarray(image_array)
                    
                    # Save with date in filename
                    filename = f"{date_start}.png"
                    output_path = IMAGERY_DIR / aoi_id / filename
                    img.save(output_path)
                    
                    print(f"    ✓ Downloaded: {output_path}")
                    
                    # Store metadata
                    metadata.append({
                        'aoi_id': aoi_id,
                        'aoi_name': aoi_data['name'],
                        'bbox': aoi_data['bbox'],
                        'date_range': [date_start, date_end],
                        'filename': filename,
                        'path': str(output_path),
                        'source': 'Sentinel-2',
                        'resolution': '10m',
                        'downloaded_at': datetime.now().isoformat()
                    })
                else:
                    print(f"    ✗ No cloud-free images found")
                    
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                continue
    
    # Save metadata
    if metadata:
        metadata_file = METADATA_DIR / 'imagery_metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"\n✓ Metadata saved to: {metadata_file}")
    
    return True


def download_landsat_imagery():
    """Download USGS Landsat imagery for all AOIs (optional fallback)."""
    try:
        from landsatxplore.api import API
        from landsatxplore.earthexplorer import EarthExplorer
    except ImportError:
        print("\nNOTE: landsatxplore not installed (optional).")
        print("Skipping Landsat download. Install with: pip install landsatxplore")
        return False
    
    if not USGS_USERNAME or not USGS_PASSWORD:
        print("\nNOTE: USGS credentials not found in .env file")
        print("Skipping Landsat download. Set USGS_USERNAME and USGS_PASSWORD if needed")
        return False
    
    print("\n" + "="*60)
    print("Downloading Landsat Imagery (optional fallback)")
    print("="*60)
    
    # Implementation for Landsat download would go here
    # Skipping for now as Sentinel-2 is primary source
    
    return True


def generate_summary():
    """Generate a summary of downloaded imagery."""
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    
    total_images = 0
    total_size = 0
    
    for aoi_id in AOIS.keys():
        aoi_dir = IMAGERY_DIR / aoi_id
        if aoi_dir.exists():
            images = list(aoi_dir.glob('*.png')) + list(aoi_dir.glob('*.jpg'))
            count = len(images)
            size = sum(img.stat().st_size for img in images)
            total_images += count
            total_size += size
            
            print(f"{aoi_id:20s} : {count:2d} images ({size/1024/1024:.2f} MB)")
    
    print("-"*60)
    print(f"{'TOTAL':20s} : {total_images:2d} images ({total_size/1024/1024:.2f} MB)")
    print("="*60)


def main():
    """Main execution function."""
    print("="*60)
    print("ASIP Data Acquisition Script")
    print("="*60)
    print()
    
    # Setup directories
    setup_directories()
    
    # Download Sentinel-2 imagery
    print("="*60)
    print("Downloading Sentinel-2 Imagery")
    print("="*60)
    success = download_sentinel2_imagery()
    
    if not success:
        print("\n⚠️  Sentinel-2 download failed. Please check credentials and installation.")
        return 1
    
    # Optional: Download Landsat imagery
    download_landsat_imagery()
    
    # Generate summary
    generate_summary()
    
    print("\n✓ Data acquisition complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
