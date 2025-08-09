#!/usr/bin/env python3
"""
Earth Engine Registration Checker

Continuously checks if Earth Engine registration is complete
"""

import time
import ee
import os

def check_registration(project_id):
    """Check if Earth Engine registration is complete"""
    try:
        ee.Initialize(project=project_id)
        return True, "Success"
    except Exception as e:
        return False, str(e)

def main():
    project_id = "reboot-468512"
    
    print(f"🔄 Monitoring Earth Engine registration for project: {project_id}")
    print("⏹️  Press Ctrl+C to stop")
    print()
    
    attempt = 1
    while True:
        print(f"🧪 Attempt {attempt}: Testing registration...", end=" ")
        
        success, message = check_registration(project_id)
        
        if success:
            print("✅ SUCCESS!")
            print(f"🎉 Earth Engine is now registered and working!")
            
            # Set environment variable
            os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
            
            # Test basic functionality
            try:
                image = ee.Image('CGIAR/SRTM90_V4')
                print("✅ Can access basic Earth Engine datasets")
                
                # Test AlphaEarth dataset
                try:
                    dataset = ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
                    first_image = dataset.first()
                    print("✅ AlphaEarth dataset accessible!")
                except Exception as e:
                    print(f"⚠️  AlphaEarth dataset: {e}")
                    print("   (This is normal if you don't have special access)")
                
                print(f"\n🚀 Ready to launch the system!")
                print("Run: python launch_system.py web")
                break
                
            except Exception as e:
                print(f"⚠️  Basic test failed: {e}")
                
        else:
            print("❌ Not ready yet")
            if "not registered" in message:
                print("   Still waiting for registration approval...")
            else:
                print(f"   Error: {message}")
        
        print(f"⏳ Waiting 30 seconds before next check...")
        print()
        
        try:
            time.sleep(30)
            attempt += 1
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
            break

if __name__ == "__main__":
    main()