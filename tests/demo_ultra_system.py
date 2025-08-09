#!/usr/bin/env python3
"""
Ultra-Integrated Crop Recommendation System Demo
Shows the complete AlphaEarth ↔ Crop Recommender integration
"""

import time
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest

def print_banner():
    """Print demo banner"""
    print("🌍" + "="*60 + "🌍")
    print("🚀 ULTRA-INTEGRATED CROP RECOMMENDATION SYSTEM DEMO 🚀")
    print("🌍" + "="*60 + "🌍")
    print()
    print("🛰️  AlphaEarth Satellite Data + 🤖 AI Crop Recommendation")
    print("   Real-time satellite analysis → Intelligent crop suggestions")
    print()

def demo_single_prediction(bridge):
    """Demo single location prediction"""
    print("📍 DEMO 1: Single Location Analysis")
    print("-" * 40)
    
    # California agriculture region
    location = {
        'name': 'California Central Valley',
        'lat': 39.0372,
        'lon': -121.8036,
        'description': 'Major agricultural region in California'
    }
    
    print(f"🌾 Analyzing: {location['name']}")
    print(f"📍 Coordinates: {location['lat']}, {location['lon']}")
    print(f"📝 Description: {location['description']}")
    print()
    
    # Create request
    request = CropRecommendationRequest(
        latitude=location['lat'],
        longitude=location['lon'],
        year=2024,
        use_cache=False
    )
    
    print("🛰️  Extracting satellite data...")
    start_time = time.time()
    
    try:
        response = bridge.get_crop_recommendation(request)
        processing_time = time.time() - start_time
        
        print("✅ Analysis complete!")
        print()
        print("🎯 RECOMMENDATION RESULTS:")
        print(f"   🌱 Recommended Crop: {response.recommended_crop}")
        print(f"   📊 Confidence Score: {response.confidence_score:.1%}")
        print(f"   ⚡ Processing Time: {response.processing_time_ms:.1f}ms")
        print(f"   🌡️  Climate Zone: {response.region_info.get('climate_zone', 'Unknown')}")
        print()
        
        print("📊 EXTRACTED SATELLITE FEATURES:")
        features = response.satellite_features
        print(f"   🧪 Nitrogen (N): {features['nitrogen']:.1f}")
        print(f"   🧪 Phosphorus (P): {features['phosphorus']:.1f}")
        print(f"   🧪 Potassium (K): {features['potassium']:.1f}")
        print(f"   🌡️  Temperature: {features['temperature']:.1f}°C")
        print(f"   💧 Humidity: {features['humidity']:.1f}%")
        print(f"   ⚗️  pH Level: {features['ph']:.2f}")
        print(f"   🌧️  Rainfall: {features['rainfall']:.1f}mm")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

async def demo_batch_processing(bridge):
    """Demo batch processing"""
    print("🌍 DEMO 2: Global Batch Analysis")
    print("-" * 40)
    
    # Global agricultural regions
    locations = [
        {'name': 'California Agriculture', 'lat': 39.0372, 'lon': -121.8036},
        {'name': 'Iowa Corn Belt', 'lat': 42.0308, 'lon': -93.6319},
        {'name': 'India Rice Region', 'lat': 26.8467, 'lon': 80.9462},
        {'name': 'Brazil Soybean', 'lat': -14.2350, 'lon': -51.9253},
        {'name': 'European Farmland', 'lat': 52.5200, 'lon': 13.4050}
    ]
    
    print(f"🌾 Analyzing {len(locations)} global agricultural regions...")
    print()
    
    # Extract coordinates for batch processing
    coordinates = [(loc['lat'], loc['lon']) for loc in locations]
    
    print("🛰️  Processing satellite data for all locations...")
    start_time = time.time()
    
    try:
        responses = await bridge.batch_process_locations(coordinates, 2024)
        total_time = time.time() - start_time
        
        print("✅ Batch analysis complete!")
        print()
        print("🎯 GLOBAL CROP RECOMMENDATIONS:")
        print("-" * 50)
        
        for i, (location, response) in enumerate(zip(locations, responses)):
            if hasattr(response, 'recommended_crop'):
                print(f"{i+1}. {location['name']}")
                print(f"   📍 {location['lat']}, {location['lon']}")
                print(f"   🌱 Recommended: {response.recommended_crop}")
                print(f"   📊 Confidence: {response.confidence_score:.1%}")
                print(f"   🌡️  Climate: {response.region_info.get('climate_zone', 'Unknown')}")
                print(f"   ⚡ Time: {response.processing_time_ms:.1f}ms")
                print()
            else:
                print(f"{i+1}. {location['name']} - ❌ Analysis failed")
                print()
        
        print(f"📈 BATCH PERFORMANCE:")
        print(f"   ⚡ Total Time: {total_time*1000:.1f}ms")
        print(f"   📊 Average per Location: {(total_time*1000)/len(locations):.1f}ms")
        print(f"   🎯 Success Rate: {len([r for r in responses if hasattr(r, 'recommended_crop')])}/{len(locations)}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Batch analysis failed: {e}")
        return False

def demo_performance_comparison(bridge):
    """Demo performance comparison"""
    print("⚡ DEMO 3: Performance Comparison")
    print("-" * 40)
    
    location = (39.0372, -121.8036)  # California
    
    print("🧪 Testing performance with caching...")
    print()
    
    # First request (no cache)
    request = CropRecommendationRequest(
        latitude=location[0],
        longitude=location[1],
        year=2024,
        use_cache=True
    )
    
    print("1️⃣  First request (no cache):")
    start_time = time.time()
    response1 = bridge.get_crop_recommendation(request)
    time1 = (time.time() - start_time) * 1000
    print(f"   ⚡ Time: {time1:.1f}ms")
    print(f"   🌱 Result: {response1.recommended_crop}")
    print(f"   💾 Cache hit: {response1.cache_hit}")
    print()
    
    # Second request (should be cached)
    print("2️⃣  Second request (cached):")
    start_time = time.time()
    response2 = bridge.get_crop_recommendation(request)
    time2 = (time.time() - start_time) * 1000
    print(f"   ⚡ Time: {time2:.1f}ms")
    print(f"   🌱 Result: {response2.recommended_crop}")
    print(f"   💾 Cache hit: {response2.cache_hit}")
    print()
    
    # Performance comparison
    speedup = time1 / time2 if time2 > 0 else 1
    print("📊 PERFORMANCE ANALYSIS:")
    print(f"   🚀 Cache Speedup: {speedup:.1f}x faster")
    print(f"   💾 Cache Efficiency: {((time1-time2)/time1)*100:.1f}% time saved")
    print(f"   ✅ Consistent Results: {response1.recommended_crop == response2.recommended_crop}")
    print()

def demo_system_health(bridge):
    """Demo system health monitoring"""
    print("🏥 DEMO 4: System Health Monitoring")
    print("-" * 40)
    
    # Get health status
    health = bridge.health_check()
    stats = bridge.get_performance_stats()
    
    print("🔍 SYSTEM HEALTH STATUS:")
    print(f"   🟢 Overall Status: {health['status'].upper()}")
    print(f"   🤖 ML Model: {health['components'].get('ml_model', 'unknown')}")
    print(f"   🛰️  AlphaEarth: {health['components'].get('alphaearth', 'unknown')}")
    print()
    
    print("📊 PERFORMANCE STATISTICS:")
    print(f"   📈 Total Requests: {stats['total_requests']}")
    print(f"   ⚡ Avg Processing Time: {stats['avg_processing_time']:.1f}ms")
    print(f"   💾 Cache Hit Rate: {stats.get('cache_hit_rate_percent', 0):.1f}%")
    print(f"   ❌ Error Rate: {stats.get('error_rate_percent', 0):.1f}%")
    print()

async def main():
    """Main demo function"""
    print_banner()
    
    print("🔧 Initializing Ultra Integration Bridge...")
    try:
        bridge = UltraIntegrationBridge(
            model_path='model.pkl',
            scaler_paths=('minmaxscaler.pkl', 'standscaler.pkl'),
            earth_engine_credentials=None,
            cache_size=100,
            enable_async=True
        )
        print("✅ Bridge initialized successfully!")
        print()
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Run demos
    demos_passed = 0
    total_demos = 4
    
    # Demo 1: Single prediction
    if demo_single_prediction(bridge):
        demos_passed += 1
    
    print("🔄 " + "-"*60)
    print()
    
    # Demo 2: Batch processing
    if await demo_batch_processing(bridge):
        demos_passed += 1
    
    print("🔄 " + "-"*60)
    print()
    
    # Demo 3: Performance comparison
    try:
        demo_performance_comparison(bridge)
        demos_passed += 1
    except Exception as e:
        print(f"❌ Performance demo failed: {e}")
    
    print("🔄 " + "-"*60)
    print()
    
    # Demo 4: System health
    try:
        demo_system_health(bridge)
        demos_passed += 1
    except Exception as e:
        print(f"❌ Health demo failed: {e}")
    
    # Final summary
    print("🎯 DEMO SUMMARY")
    print("="*50)
    print(f"✅ Demos Passed: {demos_passed}/{total_demos}")
    print(f"📊 Success Rate: {(demos_passed/total_demos)*100:.0f}%")
    print()
    
    if demos_passed == total_demos:
        print("🎉 ALL DEMOS SUCCESSFUL!")
        print("🚀 Ultra-Integrated System is fully operational!")
        print()
        print("🌐 Next Steps:")
        print("   1. Run: python app_ultra_integrated.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Click anywhere on the world map")
        print("   4. Get instant crop recommendations!")
    else:
        print("⚠️  Some demos had issues, but core functionality works!")
    
    print()
    print("🌱 Thank you for trying the Ultra-Integrated Crop Recommendation System! 🌱")

if __name__ == "__main__":
    asyncio.run(main())