#!/usr/bin/env python3
"""
Test crop predictions for different locations
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

def test_crop_predictions():
    """Test that different locations produce different crop predictions"""
    print("🧪 Testing Crop Predictions Across Locations")
    print("=" * 60)
    
    try:
        from core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest
        
        bridge = UltraIntegrationBridge()
        print(f"✅ Integration bridge initialized")
        print(f"   Using real AlphaEarth: {bridge.use_real_alphaearth}")
        
        # Test different locations around the world
        test_locations = [
            (39.0372, -121.8036, "California, USA"),
            (7.8845, 39.1553, "Ethiopia"),
            (38.1603, -122.0251, "Northern California"),
            (51.5074, -0.1278, "London, UK"),
            (35.6762, 139.6503, "Tokyo, Japan"),
            (-33.8688, 151.2093, "Sydney, Australia")
        ]
        
        print("\nCrop predictions for different locations:")
        print("-" * 60)
        
        predictions = []
        for lat, lon, name in test_locations:
            request = CropRecommendationRequest(
                latitude=lat,
                longitude=lon,
                year=2024,
                use_cache=False  # Force fresh predictions
            )
            
            response = bridge.get_crop_recommendation(request)
            predictions.append((name, response.recommended_crop))
            
            print(f"{name:20} | {response.recommended_crop:15} | Features: N={response.satellite_features['nitrogen']:5.1f} "
                  f"P={response.satellite_features['phosphorus']:5.1f} K={response.satellite_features['potassium']:5.1f} "
                  f"T={response.satellite_features['temperature']:5.1f}°C")
        
        # Check for crop diversity
        unique_crops = set([crop for _, crop in predictions])
        
        print("\n" + "=" * 60)
        print("CROP DIVERSITY ANALYSIS:")
        print("=" * 60)
        print(f"Total locations tested: {len(predictions)}")
        print(f"Unique crops predicted: {len(unique_crops)}")
        print(f"Crop diversity: {unique_crops}")
        
        if len(unique_crops) >= 3:
            print("\n✅ EXCELLENT DIVERSITY: Multiple different crops predicted!")
            print("   The system is now working correctly with varied predictions")
            return True
        elif len(unique_crops) == 2:
            print("\n⚠️  MODERATE DIVERSITY: Some variation but could be better")
            print("   The system shows improvement but may need more tuning")
            return True
        else:
            print("\n❌ POOR DIVERSITY: Still predicting the same crop everywhere")
            print("   The system needs further adjustment")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_crop_predictions()
    if success:
        print("\n🎉 Crop prediction diversity test PASSED!")
        print("   The system now produces varied crop recommendations")
        print("   Users will see different crops for different locations")
    else:
        print("\n❌ Crop prediction diversity test FAILED!")
        print("   The system still needs adjustment to vary predictions")