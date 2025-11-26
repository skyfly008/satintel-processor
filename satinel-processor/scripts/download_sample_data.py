"""
Download Sample Sentinel-2 Imagery for Demo

This script will download sample satellite tiles for New York and Tehran
using the Sentinel Hub API or USGS Earth Explorer API.

Usage:
    python scripts/download_sample_data.py --area new_york --date 2023-01-01
"""

import argparse
from pathlib import Path


def download_sentinel_tile(area_id: str, date: str, output_dir: Path):
    """
    Download Sentinel-2 tile for given area and date.
    
    Args:
        area_id: Area identifier (new_york, tehran)
        date: Date string (YYYY-MM-DD)
        output_dir: Output directory for imagery
    """
    # TODO: Implement Sentinel Hub API download
    # 1. Configure API credentials
    # 2. Define bounding box for area
    # 3. Request imagery
    # 4. Save as PNG/GeoTIFF
    print(f"Downloading {area_id} imagery for {date}...")
    print("TODO: Implement Sentinel Hub integration")


def download_usgs_tile(area_id: str, date: str, output_dir: Path):
    """
    Download USGS/Landsat tile for given area and date.
    
    Args:
        area_id: Area identifier
        date: Date string
        output_dir: Output directory
    """
    # TODO: Implement USGS API download
    print(f"Downloading USGS imagery for {area_id} on {date}...")
    print("TODO: Implement USGS Earth Explorer integration")


def preprocess_imagery(input_path: Path, output_path: Path):
    """
    Preprocess downloaded imagery for model input.
    
    Args:
        input_path: Raw imagery path
        output_path: Processed imagery path
    """
    # TODO: Implement preprocessing
    # 1. Load image
    # 2. Resize to standard tile size
    # 3. Apply normalization
    # 4. Save as PNG
    pass


def main():
    parser = argparse.ArgumentParser(
        description="Download sample satellite imagery"
    )
    parser.add_argument(
        "--area",
        choices=["new_york", "tehran", "all"],
        default="all",
        help="Area to download"
    )
    parser.add_argument(
        "--date",
        default="2023-01-01",
        help="Date for imagery (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--source",
        choices=["sentinel", "usgs"],
        default="sentinel",
        help="Data source"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("ASIP Sample Data Download Script")
    print("=" * 60)
    print(f"Area: {args.area}")
    print(f"Date: {args.date}")
    print(f"Source: {args.source}")
    print("=" * 60)
    
    # TODO: Implement download logic
    print("\nNOTE: This is a placeholder script.")
    print("Implement Sentinel Hub or USGS API integration to download imagery.")
    print("\nFor now, manually download sample imagery and place in:")
    print("  data/imagery/new_york/YYYY-MM-DD.png")
    print("  data/imagery/tehran/YYYY-MM-DD.png")


if __name__ == "__main__":
    main()
