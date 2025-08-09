#!/usr/bin/env python3
"""
Quick verification script for the Ultra-Integrated System
"""

import requests
import json
import time

def test_system():
    """Test all key functionality"""
    base_url = "http://localhost:5001"
    
    print("🧪 Ultra-Integrated System Verification")
    print("=" * 40)
    
    # Test 1: Health Check
    print("1️⃣  Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"   ✅ Health: {health['status']}")
            print(f"   🤖 ML Model: {health['components']['ml_model']}")
            print(f"   🛰️  AlphaEarth: {health['components']['alphaearth']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: API Prediction
    print("\n2️⃣  Testing API prediction...")
    try:
        test_data = {
            "latitude": 39.0372,
            "longitude": -121.8036,
            "year": 2024
        }
        
        response = requests.post(
            f"{base_url}/api/recommend",
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ API prediction successful")
            print(f"   🌱 Crop: {result['recommendation']['crop']}")
            print(f"   📊 Confidence: {result['recommendation']['confidence']:.1%}")
            print(f"   ⚡ Time: {result['metadata']['processing_time_ms']:.1f}ms")
            print(f"   🌍 Region: {result['region_context']['continent']}")
        else:
            print(f"   ❌ API prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API prediction error: {e}")
        return False
    
    # Test 3: Web Form
    print("\n3️⃣  Testing web form...")
    try:
        form_data = {
            "latitude": "42.0308",
            "longitude": "-93.6319",
            "year": "2024"
        }
        
        response = requests.post(
            f"{base_url}/predict_coordinates",
            data=form_data,
            timeout=15
        )
        
        if response.status_code == 200:
            print(f"   ✅ Web form successful")
            print(f"   📄 Response length: {len(response.text)} chars")
            
            # Check if response contains expected content
            if "recommended" in response.text.lower() or "crop" in response.text.lower():
                print(f"   ✅ Contains crop recommendation")
            else:
                print(f"   ⚠️  Response may not contain recommendation")
        else:
            print(f"   ❌ Web form failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Web form error: {e}")
        return False
    
    # Test 4: Batch Processing
    print("\n4️⃣  Testing batch processing...")
    try:
        batch_data = {
            "locations": [
                {"latitude": 39.0372, "longitude": -121.8036},
                {"latitude": 42.0308, "longitude": -93.6319}
            ],
            "year": 2024
        }
        
        response = requests.post(
            f"{base_url}/api/recommend",
            json=batch_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Batch processing successful")
            print(f"   📊 Locations: {result['batch_metadata']['total_locations']}")
            print(f"   ✅ Successful: {result['batch_metadata']['successful_predictions']}")
            print(f"   ⚡ Total time: {result['batch_metadata']['total_processing_time_ms']:.1f}ms")
        else:
            print(f"   ❌ Batch processing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Batch processing error: {e}")
        return False
    
    # Test 5: Performance Stats
    print("\n5️⃣  Testing performance stats...")
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Stats retrieved")
            print(f"   📈 Total requests: {stats['total_requests']}")
            print(f"   ⚡ Avg time: {stats['avg_processing_time']:.1f}ms")
            print(f"   💾 Cache hit rate: {stats.get('cache_hit_rate_percent', 0):.1f}%")
        else:
            print(f"   ❌ Stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Stats error: {e}")
        return False
    
    return True

def main():
    """Main verification function"""
    print("🚀 Starting Ultra-Integrated System Verification")
    print()
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    success = test_system()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ultra-Integrated System is fully operational")
        print()
        print("🌐 Ready to use:")
        print("   • Web Interface: http://localhost:5001")
        print("   • Click anywhere on the world map")
        print("   • Get instant crop recommendations!")
        print()
        print("🔧 API Endpoints working:")
        print("   • POST /api/recommend - Single/batch predictions")
        print("   • GET /api/health - System health")
        print("   • GET /api/stats - Performance statistics")
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Check the server logs for details")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)