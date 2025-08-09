#!/usr/bin/env python3
"""
Demo runner for AlphaEarth Crop Recommender

This script runs the demo with proper path setup.
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Set environment
os.environ['GOOGLE_CLOUD_PROJECT'] = 'reboot-468512'

def main():
    """Run demo"""
    print("🎮 Running AlphaEarth Crop Recommender Demo")
    print("=" * 50)
    
    try:
        # Import and run demo
        sys.path.insert(0, str(project_root / "tests"))
        
        from demo_ultra_system import main as demo_main
        demo_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Demo error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()