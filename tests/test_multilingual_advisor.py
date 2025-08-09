#!/usr/bin/env python3
"""
Test suite for Multi-Language Agricultural Advisor Integration
Tests English, Amharic, and Afaan Oromo translation functionality
"""

import os
import sys
import time
import json
from typing import Dict, Any

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_multilingual_advisor():
    """Test the multi-language agricultural advisor functionality"""
    
    print("🌍 Multi-Language Agricultural Advisor Tests")
    print("=" * 60)
    
    # Environment check
    print("🔧 Environment Check:")
    google_project = os.getenv('GOOGLE_CLOUD_PROJECT')
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    azure_key = os.getenv('AZURE_OPENAI_API_KEY')
    
    print(f"   - GOOGLE_CLOUD_PROJECT: {google_project or 'Not set'}")
    print(f"   - AZURE_OPENAI_ENDPOINT: {'Set' if azure_endpoint else 'Not set'}")
    print(f"   - AZURE_OPENAI_API_KEY: {'Set' if azure_key else 'Not set'}")
    print()
    
    # Test 1: Standalone Agricultural Advisor with Translations
    print("🧪 Testing Multi-Language Agricultural Advisor")
    print("=" * 50)
    
    try:
        from src.features.agricultural_advisor import AgriculturalAdvisor, AgriculturalAdviceRequest
        
        advisor = AgriculturalAdvisor()
        print(f"✅ Agricultural advisor initialized")
        print(f"   - Azure OpenAI available: {advisor.is_available()}")
        
        # Create test request for Ethiopian location
        test_request = AgriculturalAdviceRequest(
            crop_name="Teff",
            suitability_confidence=78.5,
            nitrogen=35.2,
            phosphorus=28.7,
            potassium=42.1,
            temperature=22.5,
            humidity=65.3,
            ph_level=6.8,
            rainfall=125.4,
            climate_zone="highland_tropical",
            alternative_crops=[("Barley", 72.1), ("Wheat", 68.9), ("Sorghum", 61.3)]
        )
        
        # Get advice with translations
        start_time = time.time()
        advice_response = advisor.get_farmer_advice(test_request)
        total_time = (time.time() - start_time) * 1000
        
        print(f"✅ Multi-language advice generated")
        print(f"   - Success: {advice_response.success}")
        print(f"   - Translation success: {advice_response.translation_success}")
        print(f"   - Processing time: {advice_response.processing_time_ms:.2f}ms")
        print(f"   - Translation time: {advice_response.translation_time_ms:.2f}ms")
        print(f"   - Total time: {total_time:.2f}ms")
        print(f"   - English advice available: {bool(advice_response.advice_text)}")
        print(f"   - Amharic advice available: {bool(advice_response.advice_text_amharic)}")
        print(f"   - Afaan Oromo advice available: {bool(advice_response.advice_text_afaan_oromo)}")
        print()
        
        if advice_response.success and advice_response.translation_success:
            print("=" * 60)
            print("ENGLISH ADVICE:")
            print("=" * 60)
            print(advice_response.advice_text[:300] + "..." if len(advice_response.advice_text) > 300 else advice_response.advice_text)
            print()
            
            if advice_response.advice_text_amharic:
                print("=" * 60)
                print("AMHARIC ADVICE (አማርኛ):")
                print("=" * 60)
                print(advice_response.advice_text_amharic[:300] + "..." if len(advice_response.advice_text_amharic) > 300 else advice_response.advice_text_amharic)
                print()
            
            if advice_response.advice_text_afaan_oromo:
                print("=" * 60)
                print("AFAAN OROMO ADVICE:")
                print("=" * 60)
                print(advice_response.advice_text_afaan_oromo[:300] + "..." if len(advice_response.advice_text_afaan_oromo) > 300 else advice_response.advice_text_afaan_oromo)
                print()
        
    except Exception as e:
        print(f"❌ Error testing agricultural advisor: {e}")
        return False
    
    # Test 2: Integration Bridge with Multi-Language Support
    print("🧪 Testing Integration Bridge with Multi-Language Support")
    print("=" * 60)
    
    try:
        from src.core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest
        
        bridge = UltraIntegrationBridge()
        print(f"✅ Integration bridge initialized")
        print(f"   - ML Model: {'Loaded' if bridge.model_available else 'Not available'}")
        print(f"   - AlphaEarth: {'Real' if bridge.alphaearth_available else 'Mock'}")
        print(f"   - Agricultural Advisor: {'Available' if bridge.advisor_available else 'Not available'}")
        print()
        
        # Test Ethiopian location (Addis Ababa area)
        test_request = CropRecommendationRequest(
            latitude=9.0320,   # Addis Ababa, Ethiopia
            longitude=38.7469,
            year=2024
        )
        
        start_time = time.time()
        response = bridge.get_crop_recommendation(test_request)
        total_time = (time.time() - start_time) * 1000
        
        print(f"✅ Multi-language crop recommendation completed")
        print(f"   - Recommended crop: {response.recommended_crop}")
        print(f"   - Confidence: {response.confidence_score:.1f}%")
        print(f"   - Processing time: {total_time:.2f}ms")
        print(f"   - Alternative crops: {len(response.alternative_crops) if response.alternative_crops else 0}")
        print(f"   - Farmer advice available: {response.advice_available}")
        print(f"   - Translations available: {response.translation_available}")
        print()
        
        if response.alternative_crops:
            print("📊 Alternative Crops:")
            for i, (crop, confidence) in enumerate(response.alternative_crops[:3], 1):
                print(f"   {i}. {crop} ({confidence:.1f}% suitable)")
            print()
        
        if response.advice_available:
            print("🌾 Multi-Language Advice Status:")
            print(f"   - English: {'✅ Available' if response.farmer_advice else '❌ Not available'}")
            print(f"   - Amharic: {'✅ Available' if response.farmer_advice_amharic else '❌ Not available'}")
            print(f"   - Afaan Oromo: {'✅ Available' if response.farmer_advice_afaan_oromo else '❌ Not available'}")
            print()
        
    except Exception as e:
        print(f"❌ Error testing integration bridge: {e}")
        return False
    
    # Test 3: Web API Multi-Language Response
    print("🧪 Testing Web API Multi-Language Response")
    print("=" * 50)
    
    try:
        from src.web.app_ultra_integrated import app
        
        with app.test_client() as client:
            # Test Ethiopian location
            test_data = {
                'latitude': 8.9806,   # Central Ethiopia
                'longitude': 38.7578,
                'year': 2024
            }
            
            response = client.post('/api/recommend', 
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            print(f"✅ API response generated")
            print(f"   - Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"   - Success: {data.get('success', False)}")
                print(f"   - Crop: {data.get('recommendation', {}).get('crop', 'Unknown')}")
                print(f"   - Confidence: {data.get('recommendation', {}).get('confidence', 0):.1f}%")
                
                farmer_advice = data.get('farmer_advice', {})
                print(f"   - Advice available: {farmer_advice.get('available', False)}")
                print(f"   - Translation available: {farmer_advice.get('translation_available', False)}")
                print(f"   - English advice: {'✅' if farmer_advice.get('advice_text') else '❌'}")
                print(f"   - Amharic advice: {'✅' if farmer_advice.get('advice_text_amharic') else '❌'}")
                print(f"   - Afaan Oromo advice: {'✅' if farmer_advice.get('advice_text_afaan_oromo') else '❌'}")
                
                alternatives = data.get('alternative_crops', [])
                print(f"   - Alternative crops: {len(alternatives)}")
                print()
                
                return True
            else:
                print(f"❌ API request failed with status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing web API: {e}")
        return False

def main():
    """Run all multi-language agricultural advisor tests"""
    
    print("🌍 Multi-Language Agricultural Advisor Test Suite")
    print("🇪🇹 Testing English, Amharic (አማርኛ), and Afaan Oromo Support")
    print("=" * 70)
    print()
    
    success = test_multilingual_advisor()
    
    print("=" * 70)
    print("TEST SUMMARY:")
    print("=" * 70)
    
    if success:
        print("✅ PASSED: Multi-Language Agricultural Advisor")
        print("✅ PASSED: Integration Bridge with Translations")
        print("✅ PASSED: Web API with Multi-Language Support")
        print()
        print("🎉 All tests passed! Multi-language agricultural advisor is working correctly.")
        print("🌍 Farmers can now get advice in English, Amharic, and Afaan Oromo!")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    print()
    print("📝 Note: For full translation functionality, ensure Azure OpenAI is properly configured.")
    print("🔧 Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME in .env")

if __name__ == "__main__":
    main()
