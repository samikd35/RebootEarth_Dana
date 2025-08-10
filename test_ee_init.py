#!/usr/bin/env python3
"""
Test Earth Engine initialization
"""

import os
import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set project ID
os.environ['GOOGLE_CLOUD_PROJECT'] = 'reboot-468512'

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_earth_engine_init():
    """Test Earth Engine initialization"""
    print("🧪 Testing Earth Engine Initialization")
    print("=" * 50)
    
    try:
        # Test direct Earth Engine
        import ee
        project_id = 'reboot-468512'
        ee.Initialize(project=project_id)
        print(f"✅ Direct Earth Engine initialization successful with project: {project_id}")
        
        # Test our integration
        from core.earth_engine_integration import AlphaEarthFeatureExtractor
        extractor = AlphaEarthFeatureExtractor(project_id=project_id)
        print(f"✅ AlphaEarthFeatureExtractor initialized successfully")
        
        # Test feature extraction
        features = extractor.extract_agricultural_features(39.0372, -121.8036, 2024)
        print(f"✅ Feature extraction successful:")
        for key, value in features.items():
            print(f"   {key}: {value:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Earth Engine initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_alphaearth_extractor():
    """Test AlphaEarth extractor"""
    print("\n🧪 Testing AlphaEarth Extractor")
    print("=" * 50)
    
    try:
        from alphaearth.alpha_earth_extractor import AlphaEarthExtractor
        extractor = AlphaEarthExtractor(project_id='reboot-468512')
        
        print(f"✅ AlphaEarth extractor initialized")
        print(f"   Using real Earth Engine: {extractor.use_real_ee}")
        
        # Test feature extraction
        features = extractor.extract_agricultural_features(39.0372, -121.8036, 2024)
        print(f"✅ Feature extraction successful:")
        for key, value in features.items():
            print(f"   {key}: {value:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ AlphaEarth extractor failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_bridge():
    """Test integration bridge"""
    print("\n🧪 Testing Integration Bridge")
    print("=" * 50)
    
    try:
        from core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest
        
        bridge = UltraIntegrationBridge()
        print(f"✅ Integration bridge initialized")
        print(f"   Using real AlphaEarth: {bridge.use_real_alphaearth}")
        
        # Test prediction
        request = CropRecommendationRequest(
            latitude=39.0372,
            longitude=-121.8036,
            year=2024
        )
        
        response = bridge.get_crop_recommendation(request)
        print(f"✅ Crop recommendation successful:")
        print(f"   Crop: {response.recommended_crop}")
        print(f"   Features: N={response.satellite_features['nitrogen']:.1f}, "
              f"P={response.satellite_features['phosphorus']:.1f}, "
              f"K={response.satellite_features['potassium']:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration bridge failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Earth Engine Initialization Test")
    print("=" * 60)
    
    # Test each component
    ee_ok = test_earth_engine_init()
    alpha_ok = test_alphaearth_extractor()
    bridge_ok = test_integration_bridge()
    
    print("\n📊 Test Results:")
    print(f"   Earth Engine Direct: {'✅ PASS' if ee_ok else '❌ FAIL'}")
    print(f"   AlphaEarth Extractor: {'✅ PASS' if alpha_ok else '❌ FAIL'}")
    print(f"   Integration Bridge: {'✅ PASS' if bridge_ok else '❌ FAIL'}")
    
    if all([ee_ok, alpha_ok, bridge_ok]):
        print("\n🎉 All tests passed! Earth Engine is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")