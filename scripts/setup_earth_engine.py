#!/usr/bin/env python3
"""
Earth Engine Setup Script

This script helps set up Google Earth Engine authentication and project configuration
for the AlphaEarth crop recommendation system.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_earth_engine_cli():
    """Check if Earth Engine CLI is installed"""
    success, stdout, stderr = run_command("earthengine --help")
    return success

def authenticate_earth_engine():
    """Run Earth Engine authentication"""
    print("🔐 Starting Earth Engine authentication...")
    print("This will open a web browser for authentication.")
    
    success, stdout, stderr = run_command("earthengine authenticate", capture_output=False)
    
    if success:
        print("✅ Earth Engine authentication successful!")
        return True
    else:
        print(f"❌ Authentication failed: {stderr}")
        return False

def test_earth_engine_connection(project_id=None):
    """Test Earth Engine connection"""
    print("🧪 Testing Earth Engine connection...")
    
    try:
        # Try to import Earth Engine directly
        import ee
        
        # Try different initialization methods
        if project_id:
            ee.Initialize(project=project_id)
            print(f'✅ Earth Engine initialized with project: {project_id}')
        else:
            # Try without project first
            try:
                ee.Initialize()
                print('✅ Earth Engine initialized without explicit project')
            except Exception as e1:
                print(f'⚠️  Failed without project: {e1}')
                # Try with earthengine-legacy
                try:
                    ee.Initialize(project='earthengine-legacy')
                    print('✅ Earth Engine initialized with earthengine-legacy')
                except Exception as e2:
                    print(f'❌ All initialization methods failed: {e1}, {e2}')
                    return False
        
        # Test basic functionality
        image = ee.Image('CGIAR/SRTM90_V4')
        print('✅ Can access basic Earth Engine datasets')
        
        # Test AlphaEarth dataset access
        try:
            dataset = ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
            print('✅ AlphaEarth dataset accessible!')
            
            # Try to get basic info
            first_image = dataset.first()
            info = first_image.getInfo()
            print('✅ Can query AlphaEarth embeddings successfully!')
            
        except Exception as e:
            print(f'⚠️  AlphaEarth dataset access issue: {e}')
            print('   This might be normal if you don\'t have access to the dataset')
        
        print('🎉 Earth Engine connection test completed!')
        return True
        
    except ImportError:
        print("❌ Earth Engine API not installed!")
        print("Install with: pip install earthengine-api")
        return False
    except Exception as e:
        print(f'❌ Earth Engine test failed: {e}')
        return False

def create_project_config(project_id):
    """Create a project configuration file"""
    config_dir = Path.home() / '.config' / 'earthengine'
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / 'project_config.json'
    config = {
        'project_id': project_id,
        'created_at': str(time.time()),
        'notes': 'Created by AlphaEarth setup script'
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Project configuration saved to {config_file}")

def main():
    """Main setup process"""
    print("🌍 AlphaEarth Earth Engine Setup")
    print("=" * 40)
    
    # Check if Earth Engine CLI is available
    if not check_earth_engine_cli():
        print("❌ Earth Engine CLI not found!")
        print("Please install it with: pip install earthengine-api")
        sys.exit(1)
    
    print("✅ Earth Engine CLI found")
    
    # Get project ID from user
    project_id = input("\n🏗️  Enter your Google Cloud Project ID (or press Enter to skip): ").strip()
    
    if not project_id:
        print("⚠️  No project ID provided. Will try default authentication.")
        project_id = None
    
    # Authenticate
    if not authenticate_earth_engine():
        print("❌ Authentication failed. Please try again.")
        sys.exit(1)
    
    # Test connection
    if test_earth_engine_connection(project_id):
        print("🎉 Setup completed successfully!")
        
        if project_id:
            create_project_config(project_id)
            
        print("\n📋 Next steps:")
        print("1. Run: python demo_ultra_system.py")
        print("2. Or run: python launch_ultra_system.py")
        print("3. Test with: python test_ultra_integration.py")
        
    else:
        print("❌ Setup failed. Please check your Google Cloud project permissions.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have a Google Cloud project")
        print("2. Enable the Earth Engine API in your project")
        print("3. Make sure you have the necessary permissions")
        print("4. Visit: https://console.cloud.google.com/apis/library/earthengine.googleapis.com")

if __name__ == "__main__":
    main()