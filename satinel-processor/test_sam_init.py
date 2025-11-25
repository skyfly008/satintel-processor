#!/usr/bin/env python
"""Test SAM initialization and weight download."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from samgeo import SamGeo

# Try to initialize SAM - this should auto-download weights
print("Initializing SAM...")
try:
    sam = SamGeo(
        model_type="vit_h",
        checkpoint=None,  # Auto-download
        automatic=False
    )
    print("✓ SAM initialized successfully")
    print(f"Model loaded: {sam.checkpoint if hasattr(sam, 'checkpoint') else 'default'}")
except Exception as e:
    print(f"✗ SAM initialization failed: {e}")
    sys.exit(1)
