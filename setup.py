#!/usr/bin/env python3
"""
Setup script for AlphaEarth Crop Recommender

This script sets up Earth Engine authentication and system requirements.
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import the setup script
sys.path.insert(0, str(project_root / "scripts"))

if __name__ == "__main__":
    from setup_earth_engine import main
    main()