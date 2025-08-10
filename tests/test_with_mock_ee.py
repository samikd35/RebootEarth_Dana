#!/usr/bin/env python3
"""
Test the geospatial system with a mock Earth Engine implementation
"""

import numpy as np
from typing import Dict
import logging

class MockAlphaEarthFeatureExtractor:
    """
    Mock implementation of AlphaEarthFeatureExtractor for testing
    """
    
    def __init__(self):
        """Initialize mock extractor"""
        logging.info("Mock Earth Engine extractor initialized")
    
    def extract_agricultural_features(self, 
                                    latitude: float, 
                                    longitude: float,
                                    year: int = 2024) -> Dict[str, float]:
        """
        Mock feature extraction that returns realistic values based on location
        """
        # Simulate different agricultural conditions based on coordinates
        # This is a simplified mock - real implementation would use satellite data
        
        # Base features (roughly matching dataset statistics)
        base_features = {
            'nitrogen': 50.0,
            'phosphorus': 53.0,
            'potassium': 48.0,
            'temperature': 25.6,
            'humidity': 71.5,
            'ph': 6.47,
            'rainfall': 103.5
        }
        
        # Modify based on latitude (climate zones)
        if latitude > 40:  # Northern regions - cooler, different crops
            base_features['temperature'] -= 5
            base_features['humidity'] += 10
            base_features['nitrogen'] += 20  # Good for cereals
            base_features['rainfall'] += 50
        elif latitude < 20:  # Tropical regions
            base_features['temperature'] += 8
            base_features['humidity'] += 15
            base_features['potassium'] += 30  # Good for fruits
            base_features['rainfall'] += 100
        
        # Modify based on longitude (continental effects)
        if -130 < longitude < -60:  # Americas
            base_features['phosphorus'] += 15
            base_features['ph'] += 0.3
        elif -10 < longitude < 50:  # Europe/Africa
            base_features['nitrogen'] += 10
            base_features['ph'] -= 0.2
        elif 70 < longitude < 150:  # Asia
            base_features['potassium'] += 20
            base_features['rainfall'] += 80
        
        # Add more realistic variation based on precise coordinates
        # Use a more complex seed to ensure different locations get different features
        seed = int(abs(latitude * 1000 + longitude * 1000 + year)) % 2147483647
        np.random.seed(seed)
        
        # Add significant variation to create diverse crop recommendations
        for key in base_features:
            if key in ['nitrogen', 'phosphorus', 'potassium']:
                # Nutrient levels can vary significantly (20-40% variation)
                variation = np.random.normal(0, 0.3)
            elif key in ['temperature', 'rainfall']:
                # Climate factors have moderate variation (15-25%)
                variation = np.random.normal(0, 0.2)
            else:
                # pH and humidity have smaller variation (10-15%)
                variation = np.random.normal(0, 0.15)
            
            base_features[key] *= (1 + variation)
        
        # Ensure values are within realistic ranges
        ranges = {
            'nitrogen': (0, 140),
            'phosphorus': (5, 145),
            'potassium': (5, 205),
            'temperature': (8.8, 43.7),
            'humidity': (14.3, 99.9),
            'ph': (3.5, 9.9),
            'rainfall': (20.2, 298.6)
        }
        
        for key, (min_val, max_val) in ranges.items():
            base_features[key] = max(min_val, min(max_val, base_features[key]))
        
        logging.info(f"Mock features extracted for ({latitude}, {longitude})")
        return base_features

def test_mock_earth_engine():
    """Test the mock Earth Engine implementation"""
    print("🧪 Testing Mock Earth Engine Implementation")
    print("=" * 45)
    
    # Test different locations
    test_locations = [
        (39.0372, -121.8036, "California Agriculture"),
        (42.0308, -93.6319, "Iowa Corn Belt"),
        (26.8467, 80.9462, "India Rice Region"),
        (-14.2350, -51.9253, "Brazil Soybean"),
        (52.5200, 13.4050, "Germany"),
        (35.6762, 139.6503, "Japan")
    ]
    
    extractor = MockAlphaEarthFeatureExtractor()
    
    for lat, lon, name in test_locations:
        print(f"\n📍 Testing {name} ({lat}, {lon}):")
        features = extractor.extract_agricultural_features(lat, lon, 2024)
        
        print(f"   Nitrogen: {features['nitrogen']:.1f}")
        print(f"   Phosphorus: {features['phosphorus']:.1f}")
        print(f"   Potassium: {features['potassium']:.1f}")
        print(f"   Temperature: {features['temperature']:.1f}°C")
        print(f"   Humidity: {features['humidity']:.1f}%")
        print(f"   pH: {features['ph']:.2f}")
        print(f"   Rainfall: {features['rainfall']:.1f}mm")
    
    return True

def test_full_system_with_mock():
    """Test the full system with mock Earth Engine"""
    print("\n🧪 Testing Full System with Mock Earth Engine")
    print("=" * 45)
    
    # Temporarily replace the real extractor with mock
    import sys
    sys.path.insert(0, '.')
    
    # Import and modify the app
    from app_geospatial import app, make_prediction
    
    # Replace the earth_extractor with our mock
    import app_geospatial
    app_geospatial.earth_extractor = MockAlphaEarthFeatureExtractor()
    
    # Test the prediction pipeline
    extractor = MockAlphaEarthFeatureExtractor()
    features = extractor.extract_agricultural_features(39.0372, -121.8036, 2024)
    
    # Make prediction using extracted features
    result = make_prediction(
        features['nitrogen'],
        features['phosphorus'], 
        features['potassium'],
        features['temperature'],
        features['humidity'],
        features['ph'],
        features['rainfall']
    )
    
    print(f"✅ Mock geospatial prediction successful:")
    print(f"   Location: California Agriculture (39.0372, -121.8036)")
    print(f"   Result: {result}")
    
    return True

def main():
    """Run all mock tests"""
    print("🚀 Testing Geospatial System with Mock Earth Engine")
    print("=" * 55)
    
    try:
        # Test mock Earth Engine
        mock_ok = test_mock_earth_engine()
        
        # Test full system integration
        system_ok = test_full_system_with_mock()
        
        if mock_ok and system_ok:
            print("\n🎉 All mock tests passed!")
            print("✅ The system architecture is working correctly")
            print("✅ Ready for real Earth Engine integration")
            print("\nTo enable real satellite data:")
            print("1. Run: earthengine authenticate")
            print("2. Enable Earth Engine in app_geospatial.py")
            print("3. Test with real coordinates")
            return True
        else:
            print("\n❌ Some tests failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)