#!/usr/bin/env python3
"""
Test feature variation for different locations
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

def test_feature_variation():
    """Test that different locations produce different features"""
    print("🧪 Testing Feature Variation Across Locations")
    print("=" * 60)
    
    try:
        from core.earth_engine_integration import AlphaEarthFeatureExtractor
        extractor = AlphaEarthFeatureExtractor(project_id='reboot-468512')
        
        # Test different locations around the world
        test_locations = [
            (39.0372, -121.8036, "California, USA"),
            (7.8845, 39.1553, "Ethiopia"),
            (38.1603, -122.0251, "Northern California"),
            (51.5074, -0.1278, "London, UK"),
            (35.6762, 139.6503, "Tokyo, Japan"),
            (-33.8688, 151.2093, "Sydney, Australia")
        ]
        
        print("Extracting features for different locations:")
        print("-" * 60)
        
        all_features = []
        for lat, lon, name in test_locations:
            features = extractor.extract_agricultural_features(lat, lon, 2024)
            all_features.append((name, features))
            
            print(f"{name:20} | N:{features['nitrogen']:6.1f} P:{features['phosphorus']:6.1f} "
                  f"K:{features['potassium']:6.1f} T:{features['temperature']:6.1f}°C "
                  f"H:{features['humidity']:6.1f}% pH:{features['ph']:5.2f} "
                  f"R:{features['rainfall']:6.1f}mm")
        
        # Check for variation
        print("\n" + "=" * 60)
        print("VARIATION ANALYSIS:")
        print("=" * 60)
        
        # Calculate variation for each feature
        features_by_type = {}
        for name, features in all_features:
            for feature_name, value in features.items():
                if feature_name not in features_by_type:
                    features_by_type[feature_name] = []
                features_by_type[feature_name].append(value)
        
        import numpy as np
        for feature_name, values in features_by_type.items():
            std_dev = np.std(values)
            min_val = min(values)
            max_val = max(values)
            range_val = max_val - min_val
            
            print(f"{feature_name:12} | Range: {range_val:6.1f} | Std Dev: {std_dev:6.2f} | "
                  f"Min: {min_val:6.1f} | Max: {max_val:6.1f}")
        
        # Check if we have good variation
        nitrogen_range = max(features_by_type['nitrogen']) - min(features_by_type['nitrogen'])
        temp_range = max(features_by_type['temperature']) - min(features_by_type['temperature'])
        
        print("\n" + "=" * 60)
        if nitrogen_range > 20 and temp_range > 5:
            print("✅ GOOD VARIATION: Features vary significantly across locations")
            print(f"   Nitrogen range: {nitrogen_range:.1f} (should be > 20)")
            print(f"   Temperature range: {temp_range:.1f} (should be > 5)")
            return True
        else:
            print("❌ POOR VARIATION: Features are too similar across locations")
            print(f"   Nitrogen range: {nitrogen_range:.1f} (should be > 20)")
            print(f"   Temperature range: {temp_range:.1f} (should be > 5)")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_feature_variation()
    if success:
        print("\n🎉 Feature variation test PASSED!")
        print("   Different locations now produce different features")
        print("   This should result in varied crop predictions")
    else:
        print("\n❌ Feature variation test FAILED!")
        print("   Features are still too similar across locations")
        print("   This will continue to produce the same crop predictions")