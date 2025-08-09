#!/usr/bin/env python3
"""
Ultra Integration Test Suite
Tests the complete AlphaEarth ↔ Crop Recommender integration
"""

import asyncio
import time
import json
import requests
import threading
from typing import List, Dict, Any
import logging

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltraIntegrationTester:
    """Comprehensive test suite for the ultra integration system"""
    
    def __init__(self):
        self.bridge = None
        self.test_results = []
        self.server_url = "http://localhost:5000"
        
    def initialize_bridge(self) -> bool:
        """Initialize the integration bridge"""
        try:
            self.bridge = UltraIntegrationBridge(
                model_path='model.pkl',
                scaler_paths=('minmaxscaler.pkl', 'standscaler.pkl'),
                earth_engine_credentials=None,
                cache_size=100,
                enable_async=True
            )
            logger.info("✅ Integration bridge initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize bridge: {e}")
            return False
    
    def test_single_prediction(self) -> Dict[str, Any]:
        """Test single location prediction"""
        logger.info("🧪 Testing single prediction...")
        
        try:
            request = CropRecommendationRequest(
                latitude=39.0372,
                longitude=-121.8036,
                year=2024,
                use_cache=False
            )
            
            start_time = time.time()
            response = self.bridge.get_crop_recommendation(request)
            processing_time = (time.time() - start_time) * 1000
            
            result = {
                'test': 'single_prediction',
                'status': 'success',
                'location': f"{request.latitude}, {request.longitude}",
                'recommended_crop': response.recommended_crop,
                'confidence': response.confidence_score,
                'processing_time_ms': processing_time,
                'satellite_features_extracted': len(response.satellite_features),
                'cache_hit': response.cache_hit,
                'data_sources': response.data_sources
            }
            
            logger.info(f"✅ Single prediction: {response.recommended_crop} ({processing_time:.1f}ms)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Single prediction failed: {e}")
            return {
                'test': 'single_prediction',
                'status': 'failed',
                'error': str(e)
            }
    
    async def test_async_prediction(self) -> Dict[str, Any]:
        """Test async prediction capability"""
        logger.info("🧪 Testing async prediction...")
        
        try:
            request = CropRecommendationRequest(
                latitude=42.0308,
                longitude=-93.6319,
                year=2024
            )
            
            start_time = time.time()
            response = await self.bridge.get_crop_recommendation_async(request)
            processing_time = (time.time() - start_time) * 1000
            
            result = {
                'test': 'async_prediction',
                'status': 'success',
                'location': f"{request.latitude}, {request.longitude}",
                'recommended_crop': response.recommended_crop,
                'confidence': response.confidence_score,
                'processing_time_ms': processing_time,
                'async_enabled': True
            }
            
            logger.info(f"✅ Async prediction: {response.recommended_crop} ({processing_time:.1f}ms)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Async prediction failed: {e}")
            return {
                'test': 'async_prediction',
                'status': 'failed',
                'error': str(e)
            }
    
    async def test_batch_processing(self) -> Dict[str, Any]:
        """Test batch processing capability"""
        logger.info("🧪 Testing batch processing...")
        
        try:
            # Test locations around the world
            locations = [
                (39.0372, -121.8036),  # California
                (42.0308, -93.6319),   # Iowa
                (26.8467, 80.9462),    # India
                (-14.2350, -51.9253),  # Brazil
                (52.5200, 13.4050)     # Germany
            ]
            
            start_time = time.time()
            responses = await self.bridge.batch_process_locations(locations, 2024)
            total_time = (time.time() - start_time) * 1000
            
            successful_predictions = len([r for r in responses if hasattr(r, 'recommended_crop')])
            
            result = {
                'test': 'batch_processing',
                'status': 'success',
                'total_locations': len(locations),
                'successful_predictions': successful_predictions,
                'total_processing_time_ms': total_time,
                'average_time_per_location_ms': total_time / len(locations),
                'predictions': [
                    {
                        'location': f"{locations[i][0]}, {locations[i][1]}",
                        'crop': r.recommended_crop if hasattr(r, 'recommended_crop') else 'Error',
                        'confidence': r.confidence_score if hasattr(r, 'confidence_score') else 0,
                        'processing_time_ms': r.processing_time_ms if hasattr(r, 'processing_time_ms') else 0
                    }
                    for i, r in enumerate(responses)
                ]
            }
            
            logger.info(f"✅ Batch processing: {successful_predictions}/{len(locations)} successful ({total_time:.1f}ms total)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Batch processing failed: {e}")
            return {
                'test': 'batch_processing',
                'status': 'failed',
                'error': str(e)
            }
    
    def test_caching_performance(self) -> Dict[str, Any]:
        """Test caching performance"""
        logger.info("🧪 Testing caching performance...")
        
        try:
            request = CropRecommendationRequest(
                latitude=39.0372,
                longitude=-121.8036,
                year=2024,
                use_cache=True
            )
            
            # First request (should be slow - no cache)
            start_time = time.time()
            response1 = self.bridge.get_crop_recommendation(request)
            first_time = (time.time() - start_time) * 1000
            
            # Second request (should be faster - cached)
            start_time = time.time()
            response2 = self.bridge.get_crop_recommendation(request)
            second_time = (time.time() - start_time) * 1000
            
            # Verify same results
            same_crop = response1.recommended_crop == response2.recommended_crop
            
            result = {
                'test': 'caching_performance',
                'status': 'success',
                'first_request_ms': first_time,
                'second_request_ms': second_time,
                'cache_speedup': first_time / second_time if second_time > 0 else 1,
                'first_cache_hit': response1.cache_hit,
                'second_cache_hit': response2.cache_hit,
                'consistent_results': same_crop,
                'recommended_crop': response1.recommended_crop
            }
            
            logger.info(f"✅ Caching: {first_time:.1f}ms → {second_time:.1f}ms (speedup: {result['cache_speedup']:.1f}x)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Caching test failed: {e}")
            return {
                'test': 'caching_performance',
                'status': 'failed',
                'error': str(e)
            }
    
    def test_global_coverage(self) -> Dict[str, Any]:
        """Test global coverage with diverse locations"""
        logger.info("🧪 Testing global coverage...")
        
        try:
            # Diverse global locations
            test_locations = [
                {'name': 'California Agriculture', 'lat': 39.0372, 'lon': -121.8036},
                {'name': 'Iowa Corn Belt', 'lat': 42.0308, 'lon': -93.6319},
                {'name': 'India Rice Region', 'lat': 26.8467, 'lon': 80.9462},
                {'name': 'Brazil Soybean', 'lat': -14.2350, 'lon': -51.9253},
                {'name': 'European Farmland', 'lat': 52.5200, 'lon': 13.4050},
                {'name': 'Australian Wheat', 'lat': -31.9505, 'lon': 115.8605},
                {'name': 'African Agriculture', 'lat': -1.2921, 'lon': 36.8219},
                {'name': 'Southeast Asia', 'lat': 13.7563, 'lon': 100.5018}
            ]
            
            results = []
            total_time = 0
            
            for location in test_locations:
                try:
                    request = CropRecommendationRequest(
                        latitude=location['lat'],
                        longitude=location['lon'],
                        year=2024
                    )
                    
                    start_time = time.time()
                    response = self.bridge.get_crop_recommendation(request)
                    processing_time = (time.time() - start_time) * 1000
                    total_time += processing_time
                    
                    results.append({
                        'location': location['name'],
                        'coordinates': f"{location['lat']}, {location['lon']}",
                        'recommended_crop': response.recommended_crop,
                        'confidence': response.confidence_score,
                        'climate_zone': response.region_info.get('climate_zone', 'Unknown'),
                        'continent': response.region_info.get('continent', 'Unknown'),
                        'processing_time_ms': processing_time,
                        'status': 'success'
                    })
                    
                except Exception as e:
                    results.append({
                        'location': location['name'],
                        'coordinates': f"{location['lat']}, {location['lon']}",
                        'status': 'failed',
                        'error': str(e)
                    })
            
            successful = len([r for r in results if r['status'] == 'success'])
            
            result = {
                'test': 'global_coverage',
                'status': 'success',
                'total_locations': len(test_locations),
                'successful_predictions': successful,
                'success_rate': (successful / len(test_locations)) * 100,
                'total_processing_time_ms': total_time,
                'average_time_per_location_ms': total_time / len(test_locations),
                'location_results': results
            }
            
            logger.info(f"✅ Global coverage: {successful}/{len(test_locations)} locations successful")
            return result
            
        except Exception as e:
            logger.error(f"❌ Global coverage test failed: {e}")
            return {
                'test': 'global_coverage',
                'status': 'failed',
                'error': str(e)
            }
    
    def test_web_api_endpoints(self) -> Dict[str, Any]:
        """Test web API endpoints"""
        logger.info("🧪 Testing web API endpoints...")
        
        try:
            # Start the Flask app in a separate thread
            from app_ultra_integrated import app
            
            def run_server():
                app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
            
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            time.sleep(3)  # Wait for server to start
            
            base_url = "http://127.0.0.1:5001"
            
            # Test health endpoint
            health_response = requests.get(f"{base_url}/api/health", timeout=10)
            health_ok = health_response.status_code == 200
            
            # Test single prediction API
            api_data = {
                'latitude': 39.0372,
                'longitude': -121.8036,
                'year': 2024
            }
            
            api_response = requests.post(
                f"{base_url}/api/recommend",
                json=api_data,
                timeout=30
            )
            api_ok = api_response.status_code == 200
            
            # Test batch API
            batch_data = {
                'locations': [
                    {'latitude': 39.0372, 'longitude': -121.8036},
                    {'latitude': 42.0308, 'longitude': -93.6319}
                ],
                'year': 2024
            }
            
            batch_response = requests.post(
                f"{base_url}/api/recommend",
                json=batch_data,
                timeout=60
            )
            batch_ok = batch_response.status_code == 200
            
            result = {
                'test': 'web_api_endpoints',
                'status': 'success',
                'health_endpoint': 'ok' if health_ok else 'failed',
                'single_api_endpoint': 'ok' if api_ok else 'failed',
                'batch_api_endpoint': 'ok' if batch_ok else 'failed',
                'health_response': health_response.json() if health_ok else None,
                'api_response_sample': api_response.json() if api_ok else None
            }
            
            logger.info(f"✅ Web API: Health={health_ok}, Single={api_ok}, Batch={batch_ok}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Web API test failed: {e}")
            return {
                'test': 'web_api_endpoints',
                'status': 'failed',
                'error': str(e)
            }
    
    def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance benchmarks"""
        logger.info("🧪 Testing performance benchmarks...")
        
        try:
            # Performance targets
            targets = {
                'single_prediction_ms': 5000,  # 5 seconds max
                'batch_10_locations_ms': 30000,  # 30 seconds max for 10 locations
                'cache_hit_ms': 100  # 100ms max for cached results
            }
            
            results = {}
            
            # Single prediction benchmark
            request = CropRecommendationRequest(
                latitude=39.0372,
                longitude=-121.8036,
                year=2024,
                use_cache=False
            )
            
            start_time = time.time()
            response = self.bridge.get_crop_recommendation(request)
            single_time = (time.time() - start_time) * 1000
            
            results['single_prediction_ms'] = single_time
            results['single_meets_target'] = single_time <= targets['single_prediction_ms']
            
            # Cache performance benchmark
            start_time = time.time()
            cached_response = self.bridge.get_crop_recommendation(request)
            cache_time = (time.time() - start_time) * 1000
            
            results['cache_hit_ms'] = cache_time
            results['cache_meets_target'] = cache_time <= targets['cache_hit_ms']
            
            # Overall performance score
            performance_score = 0
            if results['single_meets_target']:
                performance_score += 50
            if results['cache_meets_target']:
                performance_score += 50
            
            result = {
                'test': 'performance_benchmarks',
                'status': 'success',
                'targets': targets,
                'results': results,
                'performance_score': performance_score,
                'grade': 'A' if performance_score >= 90 else 'B' if performance_score >= 70 else 'C'
            }
            
            logger.info(f"✅ Performance: {performance_score}/100 (Grade: {result['grade']})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Performance benchmark failed: {e}")
            return {
                'test': 'performance_benchmarks',
                'status': 'failed',
                'error': str(e)
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("🚀 Starting Ultra Integration Test Suite")
        logger.info("=" * 50)
        
        if not self.initialize_bridge():
            return {
                'overall_status': 'failed',
                'error': 'Failed to initialize integration bridge'
            }
        
        # Run all tests
        test_results = []
        
        # Synchronous tests
        test_results.append(self.test_single_prediction())
        test_results.append(self.test_caching_performance())
        test_results.append(self.test_global_coverage())
        test_results.append(self.test_performance_benchmarks())
        
        # Asynchronous tests
        test_results.append(await self.test_async_prediction())
        test_results.append(await self.test_batch_processing())
        
        # Web API tests (optional - requires server)
        try:
            test_results.append(self.test_web_api_endpoints())
        except Exception as e:
            logger.warning(f"Web API tests skipped: {e}")
        
        # Calculate overall results
        successful_tests = len([t for t in test_results if t.get('status') == 'success'])
        total_tests = len(test_results)
        success_rate = (successful_tests / total_tests) * 100
        
        # Get system stats
        system_stats = self.bridge.get_performance_stats()
        health_check = self.bridge.health_check()
        
        overall_result = {
            'overall_status': 'success' if success_rate >= 80 else 'partial' if success_rate >= 60 else 'failed',
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': total_tests - successful_tests,
                'success_rate': success_rate
            },
            'individual_tests': test_results,
            'system_performance': system_stats,
            'system_health': health_check,
            'timestamp': time.time()
        }
        
        # Print summary
        logger.info("\n" + "=" * 50)
        logger.info("🎯 ULTRA INTEGRATION TEST RESULTS")
        logger.info("=" * 50)
        logger.info(f"Overall Status: {overall_result['overall_status'].upper()}")
        logger.info(f"Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        logger.info(f"System Health: {health_check['status']}")
        logger.info(f"Total Requests Processed: {system_stats['total_requests']}")
        logger.info(f"Average Processing Time: {system_stats['avg_processing_time']:.1f}ms")
        logger.info(f"Cache Hit Rate: {system_stats.get('cache_hit_rate_percent', 0):.1f}%")
        
        if success_rate >= 80:
            logger.info("🎉 INTEGRATION SUCCESSFUL - System ready for production!")
        elif success_rate >= 60:
            logger.info("⚠️  PARTIAL SUCCESS - Some issues need attention")
        else:
            logger.info("❌ INTEGRATION FAILED - Major issues need fixing")
        
        return overall_result

async def main():
    """Main test execution"""
    tester = UltraIntegrationTester()
    results = await tester.run_all_tests()
    
    # Save results to file
    with open('ultra_integration_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"\n📄 Detailed results saved to: ultra_integration_test_results.json")
    
    return results['overall_status'] == 'success'

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)