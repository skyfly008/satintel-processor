"""
Test Sentinel Hub API Connection
Quick script to verify your Sentinel Hub credentials work before downloading imagery.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SENTINEL_INSTANCE_ID = os.getenv('SENTINEL_INSTANCE_ID')
SENTINEL_CLIENT_ID = os.getenv('SENTINEL_CLIENT_ID')
SENTINEL_CLIENT_SECRET = os.getenv('SENTINEL_CLIENT_SECRET')


def test_sentinelhub_connection():
    """Test if Sentinel Hub API credentials are valid."""
    print("="*60)
    print("Sentinel Hub API Connection Test")
    print("="*60)
    print()
    
    # Check if credentials exist
    print("1. Checking credentials in .env file...")
    if not SENTINEL_INSTANCE_ID:
        print("   ✗ SENTINEL_INSTANCE_ID not found")
        return False
    if not SENTINEL_CLIENT_ID:
        print("   ✗ SENTINEL_CLIENT_ID not found")
        return False
    if not SENTINEL_CLIENT_SECRET:
        print("   ✗ SENTINEL_CLIENT_SECRET not found")
        return False
    
    print(f"   ✓ Instance ID: {SENTINEL_INSTANCE_ID[:8]}...")
    print(f"   ✓ Client ID: {SENTINEL_CLIENT_ID[:8]}...")
    print(f"   ✓ Client Secret: {'*' * 20}")
    print()
    
    # Check if sentinelhub is installed
    print("2. Checking if sentinelhub package is installed...")
    try:
        import sentinelhub
        print(f"   ✓ sentinelhub version: {sentinelhub.__version__}")
    except ImportError:
        print("   ✗ sentinelhub not installed")
        print("   → Install with: pip install sentinelhub")
        return False
    print()
    
    # Try to configure
    print("3. Configuring Sentinel Hub client...")
    try:
        from sentinelhub import SHConfig
        config = SHConfig()
        config.instance_id = SENTINEL_INSTANCE_ID
        config.sh_client_id = SENTINEL_CLIENT_ID
        config.sh_client_secret = SENTINEL_CLIENT_SECRET
        print("   ✓ Configuration successful")
    except Exception as e:
        print(f"   ✗ Configuration failed: {e}")
        return False
    print()
    
    # Try a simple API call
    print("4. Testing API connection with a small request...")
    try:
        from sentinelhub import (
            SentinelHubRequest, 
            MimeType, 
            CRS, 
            BBox, 
            DataCollection
        )
        
        # Small test area (Manhattan)
        bbox = BBox(bbox=[-74.00, 40.75, -73.99, 40.76], crs=CRS.WGS84)
        
        evalscript = """
        //VERSION=3
        function setup() {
            return {
                input: ["B04", "B03", "B02"],
                output: { bands: 3 }
            };
        }
        function evaluatePixel(sample) {
            return [sample.B04 * 2.5, sample.B03 * 2.5, sample.B02 * 2.5];
        }
        """
        
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[{
                'type': DataCollection.SENTINEL2_L2A,
                'dataFilter': {'maxCloudCoverage': 10},
                'time_interval': ('2023-06-01', '2023-06-30')
            }],
            responses=[{
                'identifier': 'default',
                'format': {'type': MimeType.PNG}
            }],
            bbox=bbox,
            size=[64, 64],  # Small test image
            config=config
        )
        
        # Test if we can get data (don't actually download)
        print("   → Sending test request to Sentinel Hub API...")
        data = request.get_data()
        
        if data and len(data) > 0:
            print("   ✓ API connection successful!")
            print(f"   ✓ Retrieved test image: {data[0].shape}")
        else:
            print("   ⚠ API responded but no data found (might be cloud cover)")
            print("   ✓ Connection works, but try different dates if needed")
        
    except Exception as e:
        print(f"   ✗ API request failed: {e}")
        print()
        print("   Common issues:")
        print("   - Invalid credentials")
        print("   - Exceeded API quota (2,500 req/month for free tier)")
        print("   - Network connectivity issues")
        return False
    
    print()
    print("="*60)
    print("✓ All tests passed! Ready to download imagery.")
    print("="*60)
    return True


if __name__ == '__main__':
    success = test_sentinelhub_connection()
    sys.exit(0 if success else 1)
