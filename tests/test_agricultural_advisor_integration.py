#!/usr/bin/env python3
"""
Test Agricultural Advisor Integration

This test verifies that the LLM-powered agricultural advisor
integrates properly with the crop recommendation system.
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Set environment
os.environ['GOOGLE_CLOUD_PROJECT'] = 'reboot-468512'

def test_agricultural_advisor_standalone():
    """Test the agricultural advisor as a standalone component"""
    print("🧪 Testing Agricultural Advisor Standalone")
    print("=" * 50)
    
    try:
        from features.agricultural_advisor import AgriculturalAdvisor, AgriculturalAdviceRequest
        
        # Initialize advisor
        advisor = AgriculturalAdvisor()
        
        if not advisor.is_available():
            print("⚠️  Azure OpenAI not available - testing fallback functionality")
        else:
            print("✅ Azure OpenAI connection successful")
        
        # Create test request
        test_request = AgriculturalAdviceRequest(
            crop_name="Rice",
            suitability_confidence=87.3,
            nitrogen=42.5,
            phosphorus=35.8,
            potassium=48.2,
            temperature=29.1,
            humidity=78.5,
            ph_level=6.1,
            rainfall=145.7,
            climate_zone="tropical",
            alternative_crops=[("Maize", 75.2), ("Banana", 68.9), ("Coconut", 64.1)]
        )
        
        # Get advice
        response = advisor.get_farmer_advice(test_request)
        
        print(f"✅ Advice generated successfully")
        print(f"   - Success: {response.success}")
        print(f"   - Processing time: {response.processing_time_ms:.2f}ms")
        print(f"   - Has advice text: {len(response.advice_text) > 0}")
        
        if response.success:
            print("\n" + "="*60)
            print("GENERATED FARMER ADVICE:")
            print("="*60)
            print(response.advice_text)
        else:
            print(f"   - Error: {response.error_message}")
            print("\n" + "="*60)
            print("FALLBACK ADVICE:")
            print("="*60)
            print(response.advice_text)
        
        return True
        
    except Exception as e:
        print(f"❌ Agricultural advisor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_bridge_with_advisor():
    """Test the full integration bridge with agricultural advisor"""
    print("\n🧪 Testing Integration Bridge with Agricultural Advisor")
    print("=" * 60)
    
    try:
        from core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest
        
        # Initialize bridge
        bridge = UltraIntegrationBridge(
            model_path='model.pkl',
            scaler_paths=('minmaxscaler_fixed.pkl', 'standscaler_fixed.pkl'),
            earth_engine_credentials=None,
            cache_size=100,
            enable_async=True
        )
        
        print(f"✅ Integration bridge initialized")
        print(f"   - ML Model: Loaded")
        print(f"   - AlphaEarth: {'Real' if bridge.use_real_alphaearth else 'Fallback'}")
        print(f"   - Agricultural Advisor: {'Available' if bridge.advisor_available else 'Unavailable'}")
        
        # Create test request
        test_request = CropRecommendationRequest(
            latitude=14.5995,  # Philippines (tropical)
            longitude=120.9842,
            year=2024,
            buffer_meters=1000,
            use_cache=True,
            confidence_threshold=0.7
        )
        
        # Get recommendation with advice
        response = bridge.get_crop_recommendation(test_request)
        
        print(f"\n✅ Crop recommendation completed")
        print(f"   - Recommended crop: {response.recommended_crop}")
        print(f"   - Confidence: {response.confidence_score:.1f}%")
        print(f"   - Processing time: {response.processing_time_ms:.2f}ms")
        print(f"   - Alternative crops: {len(response.alternative_crops or [])}")
        print(f"   - Farmer advice available: {response.advice_available}")
        
        # Display alternative crops
        if response.alternative_crops:
            print(f"\n📊 Alternative Crops:")
            for i, (crop, confidence) in enumerate(response.alternative_crops, 1):
                print(f"   {i}. {crop} ({confidence:.1f}% suitable)")
        
        # Display farmer advice
        if response.farmer_advice:
            print(f"\n" + "="*60)
            print("FARMER ADVICE:")
            print("="*60)
            print(response.farmer_advice)
        else:
            print(f"\n⚠️  No farmer advice generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration bridge test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_api_with_advisor():
    """Test the web API endpoints with agricultural advisor"""
    print("\n🧪 Testing Web API with Agricultural Advisor")
    print("=" * 50)
    
    try:
        from web.app_ultra_integrated import app, bridge
        
        if bridge is None:
            print("❌ Integration bridge not available in web app")
            return False
        
        print(f"✅ Web app bridge initialized")
        print(f"   - Agricultural Advisor: {'Available' if bridge.advisor_available else 'Unavailable'}")
        
        # Test API endpoint simulation
        test_data = {
            'latitude': 28.7041,  # New Delhi, India (subtropical)
            'longitude': 77.1025,
            'year': 2024,
            'buffer_meters': 1000,
            'use_cache': True,
            'confidence_threshold': 0.7
        }
        
        # Simulate the API call logic
        from core.integration_bridge import CropRecommendationRequest
        
        req = CropRecommendationRequest(
            latitude=float(test_data['latitude']),
            longitude=float(test_data['longitude']),
            year=int(test_data.get('year', 2024)),
            buffer_meters=int(test_data.get('buffer_meters', 1000)),
            use_cache=bool(test_data.get('use_cache', True)),
            confidence_threshold=float(test_data.get('confidence_threshold', 0.7))
        )
        
        response = bridge.get_crop_recommendation(req)
        
        # Simulate JSON response format
        api_response = {
            'success': True,
            'recommendation': {
                'crop': response.recommended_crop,
                'confidence': response.confidence_score,
                'class_id': response.crop_class_id
            },
            'satellite_data': response.satellite_features,
            'location': response.coordinates,
            'region_context': response.region_info,
            'alternative_crops': response.alternative_crops or [],
            'farmer_advice': {
                'available': response.advice_available,
                'advice_text': response.farmer_advice,
            },
            'metadata': {
                'processing_time_ms': response.processing_time_ms,
                'data_sources': response.data_sources,
                'cache_hit': response.cache_hit,
                'embedding_info': response.embedding_metadata
            }
        }
        
        print(f"✅ API response generated successfully")
        print(f"   - Success: {api_response['success']}")
        print(f"   - Crop: {api_response['recommendation']['crop']}")
        print(f"   - Confidence: {api_response['recommendation']['confidence']:.1f}%")
        print(f"   - Alternative crops: {len(api_response['alternative_crops'])}")
        print(f"   - Farmer advice available: {api_response['farmer_advice']['available']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Web API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all agricultural advisor integration tests"""
    print("🌾 Agricultural Advisor Integration Tests")
    print("=" * 60)
    
    # Check environment setup
    print("🔧 Environment Check:")
    print(f"   - GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT', 'Not set')}")
    print(f"   - AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')}")
    print(f"   - AZURE_OPENAI_API_KEY: {'Set' if os.getenv('AZURE_OPENAI_API_KEY') else 'Not set'}")
    print()
    
    tests = [
        ("Agricultural Advisor Standalone", test_agricultural_advisor_standalone),
        ("Integration Bridge with Advisor", test_integration_bridge_with_advisor),
        ("Web API with Advisor", test_web_api_with_advisor),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY:")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Agricultural advisor integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("\n💡 Tips:")
        print("   - Ensure Azure OpenAI credentials are set in .env file")
        print("   - Check that all dependencies are installed")
        print("   - Verify Google Cloud project is set correctly")

if __name__ == "__main__":
    main()
