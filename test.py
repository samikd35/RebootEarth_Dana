#!/usr/bin/env python3
"""
Test runner for AlphaEarth Crop Recommender

This script runs the main integration tests with proper path setup.
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
    """Run tests"""
    print("🧪 Running AlphaEarth Crop Recommender Tests")
    print("=" * 50)
    
    try:
        # Import and run tests
        sys.path.insert(0, str(project_root / "tests"))
        
        # Run integration tests
        from test_ultra_integration import main as test_main
        test_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()