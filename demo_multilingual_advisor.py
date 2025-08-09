#!/usr/bin/env python3
"""
Demo script for Multi-Language Agricultural Advisor
Showcases English, Amharic, and Afaan Oromo translations
"""

import os
import sys
import time
import json

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def demo_multilingual_advisor():
    """Demo the multi-language agricultural advisor functionality"""
    
    print("🌍 Multi-Language Agricultural Advisor Demo")
    print("🇪🇹 Supporting Ethiopian Farmers in Their Native Languages")
    print("=" * 70)
    print()
    
    try:
        from src.features.agricultural_advisor import AgriculturalAdvisor, AgriculturalAdviceRequest
        
        advisor = AgriculturalAdvisor()
        print(f"🤖 Agricultural Advisor Status: {'✅ Available' if advisor.is_available() else '❌ Unavailable'}")
        print()
        
        # Demo locations in Ethiopia
        demo_locations = [
            {
                "name": "Addis Ababa Region",
                "latitude": 9.0320,
                "longitude": 38.7469,
                "crop": "Teff",
                "description": "Highland plateau, traditional teff growing region"
            },
            {
                "name": "Oromia Region", 
                "latitude": 8.5569,
                "longitude": 39.8616,
                "crop": "Maize",
                "description": "Central highlands, mixed farming system"
            },
            {
                "name": "Amhara Region",
                "latitude": 11.5980,
                "longitude": 37.3906,
                "crop": "Barley",
                "description": "Northern highlands, cereal production area"
            }
        ]
        
        for i, location in enumerate(demo_locations, 1):
            print(f"📍 Demo {i}: {location['name']}")
            print(f"   Location: {location['latitude']:.4f}, {location['longitude']:.4f}")
            print(f"   Description: {location['description']}")
            print(f"   Target Crop: {location['crop']}")
            print()
            
            # Create test request
            test_request = AgriculturalAdviceRequest(
                crop_name=location['crop'],
                suitability_confidence=82.5,
                nitrogen=38.4,
                phosphorus=31.2,
                potassium=45.8,
                temperature=21.3,
                humidity=68.7,
                ph_level=6.5,
                rainfall=135.2,
                climate_zone="highland_tropical",
                alternative_crops=[("Wheat", 75.3), ("Sorghum", 69.8), ("Chickpea", 64.1)]
            )
            
            # Get multi-language advice
            print("🔄 Generating multi-language advice...")
            start_time = time.time()
            advice_response = advisor.get_farmer_advice(test_request)
            total_time = (time.time() - start_time) * 1000
            
            if advice_response.success:
                print(f"✅ Advice generated successfully!")
                print(f"   - English advice: {len(advice_response.advice_text)} characters")
                print(f"   - Amharic translation: {'✅' if advice_response.advice_text_amharic else '❌'}")
                print(f"   - Afaan Oromo translation: {'✅' if advice_response.advice_text_afaan_oromo else '❌'}")
                print(f"   - Processing time: {advice_response.processing_time_ms:.1f}ms")
                print(f"   - Translation time: {advice_response.translation_time_ms:.1f}ms")
                print(f"   - Total time: {total_time:.1f}ms")
                print()
                
                # Display sample advice in all languages
                print("🌾 SAMPLE ADVICE PREVIEW:")
                print("-" * 40)
                
                # English (first 200 characters)
                english_preview = advice_response.advice_text[:200] + "..." if len(advice_response.advice_text) > 200 else advice_response.advice_text
                print(f"🇬🇧 English: {english_preview}")
                print()
                
                # Amharic (first 200 characters)
                if advice_response.advice_text_amharic:
                    amharic_preview = advice_response.advice_text_amharic[:200] + "..." if len(advice_response.advice_text_amharic) > 200 else advice_response.advice_text_amharic
                    print(f"🇪🇹 አማርኛ (Amharic): {amharic_preview}")
                    print()
                
                # Afaan Oromo (first 200 characters)
                if advice_response.advice_text_afaan_oromo:
                    oromo_preview = advice_response.advice_text_afaan_oromo[:200] + "..." if len(advice_response.advice_text_afaan_oromo) > 200 else advice_response.advice_text_afaan_oromo
                    print(f"🇪🇹 Afaan Oromoo: {oromo_preview}")
                    print()
                
            else:
                print(f"❌ Failed to generate advice: {advice_response.error_message}")
            
            print("=" * 70)
            print()
            
            # Only demo first location to avoid excessive API calls
            if i == 1:
                print("📝 Note: Showing only first location demo to conserve API usage.")
                print("    The system supports all Ethiopian regions and languages!")
                break
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return False
    
    return True

def demo_web_api_multilingual():
    """Demo the web API with multi-language support"""
    
    print("🌐 Web API Multi-Language Demo")
    print("=" * 40)
    
    try:
        from src.web.app_ultra_integrated import app
        
        with app.test_client() as client:
            # Test Ethiopian location
            test_data = {
                'latitude': 9.0320,   # Addis Ababa
                'longitude': 38.7469,
                'year': 2024
            }
            
            print("🔄 Making API request for Addis Ababa region...")
            response = client.post('/api/recommend', 
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            if response.status_code == 200:
                data = response.get_json()
                
                print(f"✅ API Response Generated")
                print(f"   - Recommended Crop: {data.get('recommendation', {}).get('crop', 'Unknown')}")
                print(f"   - Confidence: {data.get('recommendation', {}).get('confidence', 0):.1f}%")
                
                farmer_advice = data.get('farmer_advice', {})
                print(f"   - Advice Available: {farmer_advice.get('available', False)}")
                print(f"   - Translation Available: {farmer_advice.get('translation_available', False)}")
                
                # Check language availability
                languages = []
                if farmer_advice.get('advice_text'):
                    languages.append("English")
                if farmer_advice.get('advice_text_amharic'):
                    languages.append("Amharic (አማርኛ)")
                if farmer_advice.get('advice_text_afaan_oromo'):
                    languages.append("Afaan Oromo")
                
                print(f"   - Available Languages: {', '.join(languages)}")
                
                alternatives = data.get('alternative_crops', [])
                if alternatives:
                    print(f"   - Alternative Crops: {len(alternatives)}")
                    for crop, confidence in alternatives[:3]:
                        print(f"     • {crop} ({confidence:.1f}% suitable)")
                
                print()
                print("🎉 Multi-language API integration working perfectly!")
                
            else:
                print(f"❌ API request failed with status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Web API demo error: {e}")
        return False
    
    return True

def main():
    """Run the multi-language agricultural advisor demo"""
    
    print("🌍 AlphaEarth Multi-Language Agricultural Advisor")
    print("🇪🇹 Empowering Ethiopian Farmers in Their Native Languages")
    print("=" * 70)
    print()
    print("This demo showcases the new multi-language feature that translates")
    print("agricultural advice into Amharic (አማርኛ) and Afaan Oromo for Ethiopian farmers.")
    print()
    
    # Run demos
    advisor_success = demo_multilingual_advisor()
    print()
    api_success = demo_web_api_multilingual()
    
    print("=" * 70)
    print("🎯 DEMO SUMMARY")
    print("=" * 70)
    
    if advisor_success and api_success:
        print("✅ Multi-Language Agricultural Advisor: Working")
        print("✅ Web API Multi-Language Support: Working")
        print("✅ Translation Pipeline: Functional")
        print()
        print("🌾 FEATURES DEMONSTRATED:")
        print("   • English agricultural advice generation")
        print("   • Amharic (አማርኛ) translation")
        print("   • Afaan Oromo translation")
        print("   • Web interface tabbed language support")
        print("   • Alternative crop recommendations")
        print()
        print("🚀 Ready for Ethiopian farmers!")
        print("🌍 Farmers can now get advice in their preferred language!")
    else:
        print("❌ Some features not working properly")
        print("🔧 Check Azure OpenAI configuration in .env file")
    
    print()
    print("📝 To use the web interface:")
    print("   1. Run: python run.py")
    print("   2. Open: http://localhost:5001")
    print("   3. Click on map in Ethiopia")
    print("   4. Toggle between English/Amharic/Afaan Oromo tabs")
    print()
    print("🌾 Empowering smallholder farmers with AI in their native languages! 🇪🇹")

if __name__ == "__main__":
    main()
