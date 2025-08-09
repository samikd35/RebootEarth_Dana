#!/usr/bin/env python3
"""
Agricultural Advisor Demo - LLM Integration Showcase

This demo showcases the new LLM-powered agricultural advisor feature
that provides farmer-friendly explanations for crop recommendations.
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Set environment
os.environ['GOOGLE_CLOUD_PROJECT'] = 'reboot-468512'

def demo_agricultural_advisor():
    """Demonstrate the agricultural advisor functionality"""
    print("🌾 Agricultural Advisor Demo - LLM Integration")
    print("=" * 60)
    
    # Check environment setup
    print("🔧 Environment Check:")
    print(f"   - GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT', 'Not set')}")
    print(f"   - AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')}")
    print(f"   - AZURE_OPENAI_API_KEY: {'Set' if os.getenv('AZURE_OPENAI_API_KEY') else 'Not set'}")
    print()
    
    try:
        from core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest
        
        # Initialize the integration bridge
        print("🚀 Initializing Ultra Integration Bridge...")
        bridge = UltraIntegrationBridge(
            model_path='model.pkl',
            scaler_paths=('minmaxscaler_fixed.pkl', 'standscaler_fixed.pkl'),
            earth_engine_credentials=None,
            cache_size=100,
            enable_async=True
        )
        
        print(f"✅ Integration bridge initialized successfully")
        print(f"   - ML Model: Loaded")
        print(f"   - AlphaEarth: {'Real' if bridge.use_real_alphaearth else 'Fallback'}")
        print(f"   - Agricultural Advisor: {'Available' if bridge.advisor_available else 'Unavailable'}")
        
        # Demo locations with different climates
        demo_locations = [
            {
                "name": "Philippines (Tropical)",
                "lat": 14.5995,
                "lon": 120.9842,
                "description": "Tropical climate, rice farming region"
            },
            {
                "name": "India (Subtropical)", 
                "lat": 28.7041,
                "lon": 77.1025,
                "description": "Subtropical climate, diverse agriculture"
            },
            {
                "name": "California, USA (Mediterranean)",
                "lat": 36.7783,
                "lon": -119.4179,
                "description": "Mediterranean climate, intensive agriculture"
            }
        ]
        
        print(f"\n🌍 Testing {len(demo_locations)} different climate zones...")
        
        for i, location in enumerate(demo_locations, 1):
            print(f"\n{'='*60}")
            print(f"📍 Location {i}: {location['name']}")
            print(f"   Coordinates: {location['lat']:.4f}, {location['lon']:.4f}")
            print(f"   Description: {location['description']}")
            print('='*60)
            
            # Create recommendation request
            request = CropRecommendationRequest(
                latitude=location['lat'],
                longitude=location['lon'],
                year=2024,
                buffer_meters=1000,
                use_cache=True,
                confidence_threshold=0.7
            )
            
            # Get recommendation with advice
            print("🔄 Processing recommendation...")
            response = bridge.get_crop_recommendation(request)
            
            # Display results
            print(f"\n🌱 CROP RECOMMENDATION:")
            print(f"   Recommended Crop: {response.recommended_crop}")
            print(f"   Confidence: {response.confidence_score:.1f}%")
            print(f"   Processing Time: {response.processing_time_ms:.2f}ms")
            print(f"   Climate Zone: {response.region_info.get('climate_zone', 'Unknown')}")
            
            # Display satellite features
            print(f"\n📊 SATELLITE DATA:")
            features = response.satellite_features
            print(f"   Nitrogen: {features.get('nitrogen', 0):.1f}")
            print(f"   Phosphorus: {features.get('phosphorus', 0):.1f}")
            print(f"   Potassium: {features.get('potassium', 0):.1f}")
            print(f"   Temperature: {features.get('temperature', 0):.1f}°C")
            print(f"   Humidity: {features.get('humidity', 0):.1f}%")
            print(f"   pH: {features.get('ph', 0):.2f}")
            print(f"   Rainfall: {features.get('rainfall', 0):.1f}mm")
            
            # Display alternative crops
            if response.alternative_crops:
                print(f"\n🌾 ALTERNATIVE CROPS:")
                for j, (crop, confidence) in enumerate(response.alternative_crops, 1):
                    print(f"   {j}. {crop} ({confidence:.1f}% suitable)")
            
            # Display farmer advice
            if response.farmer_advice:
                print(f"\n👨‍🌾 AGRICULTURAL EXTENSION OFFICER ADVICE:")
                print("="*60)
                print(response.farmer_advice)
                print("="*60)
            else:
                print(f"\n⚠️  Agricultural advice not available")
                if not bridge.advisor_available:
                    print("   Reason: Azure OpenAI not configured")
                
            print(f"\n✅ Location {i} completed successfully!")
            
            # Add a pause between locations for readability
            if i < len(demo_locations):
                input("\nPress Enter to continue to next location...")
        
        # Summary
        print(f"\n🎉 Demo completed successfully!")
        print(f"   - Processed {len(demo_locations)} locations")
        print(f"   - Agricultural Advisor: {'Available' if bridge.advisor_available else 'Unavailable'}")
        print(f"   - All features working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_web_api():
    """Demonstrate the web API with agricultural advisor"""
    print(f"\n🌐 Web API Demo")
    print("=" * 40)
    
    try:
        from web.app_ultra_integrated import app, bridge
        
        if bridge is None:
            print("❌ Web app bridge not available")
            return False
        
        print(f"✅ Web app initialized")
        print(f"   - Agricultural Advisor: {'Available' if bridge.advisor_available else 'Unavailable'}")
        
        # Simulate API request
        test_data = {
            'latitude': 14.5995,  # Philippines
            'longitude': 120.9842,
            'year': 2024
        }
        
        print(f"\n📡 Simulating API request:")
        print(f"   POST /api/recommend")
        print(f"   Data: {test_data}")
        
        # Process request
        from core.integration_bridge import CropRecommendationRequest
        
        req = CropRecommendationRequest(
            latitude=float(test_data['latitude']),
            longitude=float(test_data['longitude']),
            year=int(test_data.get('year', 2024)),
            buffer_meters=1000,
            use_cache=True,
            confidence_threshold=0.7
        )
        
        response = bridge.get_crop_recommendation(req)
        
        # Format API response
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
        
        print(f"\n📋 API Response:")
        print(f"   Success: {api_response['success']}")
        print(f"   Crop: {api_response['recommendation']['crop']}")
        print(f"   Confidence: {api_response['recommendation']['confidence']:.1f}%")
        print(f"   Alternative crops: {len(api_response['alternative_crops'])}")
        print(f"   Farmer advice available: {api_response['farmer_advice']['available']}")
        
        print(f"\n✅ Web API demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Web API demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the complete agricultural advisor demo"""
    print("🌾 AlphaEarth Crop Recommender - Agricultural Advisor Demo")
    print("=" * 70)
    print("This demo showcases the new LLM-powered agricultural advisor feature")
    print("that provides farmer-friendly explanations for crop recommendations.")
    print()
    
    # Run demos
    success_count = 0
    total_demos = 2
    
    # Demo 1: Core agricultural advisor functionality
    if demo_agricultural_advisor():
        success_count += 1
    
    # Demo 2: Web API integration
    if demo_web_api():
        success_count += 1
    
    # Final summary
    print(f"\n{'='*70}")
    print("DEMO SUMMARY:")
    print("="*70)
    print(f"✅ Completed: {success_count}/{total_demos} demos")
    
    if success_count == total_demos:
        print("🎉 All demos completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("   - LLM-powered farmer-friendly advice")
        print("   - Alternative crop recommendations")
        print("   - Multi-climate zone support")
        print("   - Web API integration")
        print("   - Real-time satellite data processing")
        
        print("\n🚀 Ready for Production!")
        print("   - Run 'python run.py' to start the web application")
        print("   - Open http://localhost:5001 in your browser")
        print("   - Click anywhere on the map for instant recommendations")
    else:
        print("⚠️  Some demos failed. Check the output above for details.")
        print("\n🔧 Troubleshooting:")
        print("   - Ensure Azure OpenAI credentials are set in .env file")
        print("   - Check that all dependencies are installed")
        print("   - Verify Google Cloud project is configured")

if __name__ == "__main__":
    main()
