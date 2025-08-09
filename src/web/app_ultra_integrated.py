"""
Ultra-Integrated Flask Application
Seamlessly connects AlphaEarth satellite data with crop recommendation ML model
"""

from flask import Flask, request, render_template, jsonify
import asyncio
import logging
from typing import Dict, List, Any
import time
from concurrent.futures import ThreadPoolExecutor
import json

from core.integration_bridge import UltraIntegrationBridge, CropRecommendationRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the ultra integration bridge
try:
    # Use relative paths that will be resolved by the integration bridge
    bridge = UltraIntegrationBridge(
        model_path='model.pkl',  # Will be resolved to models/model.pkl
        scaler_paths=('minmaxscaler_fixed.pkl', 'standscaler_fixed.pkl'),  # Will be resolved to models/
        earth_engine_credentials=None,  # Will try default auth
        cache_size=1000,
        enable_async=True
    )
    logger.info("Ultra Integration Bridge initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize bridge: {e}")
    bridge = None

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Main page with ultra-integrated interface"""
    return render_template("index_ultra_integrated.html")

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """
    Ultra-fast API endpoint for crop recommendation
    Supports both single and batch requests
    """
    try:
        if bridge is None:
            return jsonify({'error': 'Integration bridge not available'}), 500
        
        data = request.get_json()
        
        # Handle batch requests
        if 'locations' in data:
            return handle_batch_request(data)
        
        # Handle single request
        return handle_single_request(data)
        
    except Exception as e:
        logger.error(f"API recommendation failed: {e}")
        return jsonify({'error': str(e)}), 500

def handle_single_request(data: Dict) -> Dict:
    """Handle single location request"""
    # Create request object
    req = CropRecommendationRequest(
        latitude=float(data['latitude']),
        longitude=float(data['longitude']),
        year=int(data.get('year', 2024)),
        buffer_meters=int(data.get('buffer_meters', 1000)),
        use_cache=bool(data.get('use_cache', True)),
        confidence_threshold=float(data.get('confidence_threshold', 0.7))
    )
    
    # Get recommendation
    response = bridge.get_crop_recommendation(req)
    
    # Convert to JSON-serializable format
    response_data = {
        'success': True,
        'recommendation': {
            'crop': response.recommended_crop,
            'confidence': response.confidence_score,
            'class_id': response.crop_class_id
        },
        'satellite_data': {
            'nitrogen': response.satellite_features.get('nitrogen', 0),
            'phosphorus': response.satellite_features.get('phosphorus', 0),
            'potassium': response.satellite_features.get('potassium', 0),
            'temperature': response.satellite_features.get('temperature', 0),
            'humidity': response.satellite_features.get('humidity', 0),
            'ph': response.satellite_features.get('ph', 0),
            'rainfall': response.satellite_features.get('rainfall', 0)
        },
        'alternative_crops': response.alternative_crops,
        'farmer_advice': {
            'available': response.advice_available,
            'advice_text': response.farmer_advice,
            'advice_text_amharic': response.farmer_advice_amharic,
            'advice_text_afaan_oromo': response.farmer_advice_afaan_oromo,
            'translation_available': response.translation_available
        },
        'metadata': {
            'processing_time_ms': response.processing_time_ms,
            'data_sources': response.data_sources,
            'cache_hit': response.cache_hit,
            'embedding_info': response.embedding_metadata
        }
    }
    
    return jsonify(response_data)

def handle_batch_request(data: Dict) -> Dict:
    """Handle batch location requests"""
    locations = data['locations']
    year = int(data.get('year', 2024))
    
    if len(locations) > 100:  # Limit batch size
        return jsonify({'error': 'Batch size limited to 100 locations'}), 400
    
    # Process batch
    start_time = time.time()
    
    # Create requests
    requests = []
    for loc in locations:
        req = CropRecommendationRequest(
            latitude=float(loc['latitude']),
            longitude=float(loc['longitude']),
            year=year,
            use_cache=True
        )
        requests.append(req)
    
    # Process in parallel using thread pool
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(bridge.get_crop_recommendation, req) for req in requests]
        
        for i, future in enumerate(futures):
            try:
                response = future.result(timeout=30)  # 30 second timeout
                results.append({
                    'location_index': i,
                    'latitude': locations[i]['latitude'],
                    'longitude': locations[i]['longitude'],
                    'crop': response.recommended_crop,
                    'confidence': response.confidence_score,
                    'processing_time_ms': response.processing_time_ms,
                    'cache_hit': response.cache_hit
                })
            except Exception as e:
                logger.error(f"Batch item {i} failed: {e}")
                results.append({
                    'location_index': i,
                    'latitude': locations[i]['latitude'],
                    'longitude': locations[i]['longitude'],
                    'error': str(e)
                })
    
    total_time = (time.time() - start_time) * 1000
    
    return jsonify({
        'success': True,
        'batch_results': results,
        'batch_metadata': {
            'total_locations': len(locations),
            'successful_predictions': len([r for r in results if 'crop' in r]),
            'total_processing_time_ms': total_time,
            'average_time_per_location_ms': total_time / len(locations)
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    if bridge is None:
        return jsonify({
            'status': 'unhealthy',
            'error': 'Integration bridge not available'
        }), 500
    
    health = bridge.health_check()
    status_code = 200 if health['status'] == 'healthy' else 503
    
    return jsonify(health), status_code

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get performance statistics"""
    if bridge is None:
        return jsonify({'error': 'Bridge not available'}), 500
    
    stats = bridge.get_performance_stats()
    return jsonify(stats)

@app.route('/predict_coordinates', methods=['POST'])
def predict_coordinates():
    """Web form endpoint for coordinate-based prediction"""
    try:
        if bridge is None:
            return render_template('index_ultra_integrated.html', 
                                 error="Integration system not available")
        
        # Get form data
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        year = int(request.form.get('year', 2024))
        
        # Create request
        req = CropRecommendationRequest(
            latitude=latitude,
            longitude=longitude,
            year=year,
            use_cache=True
        )
        
        # Get recommendation
        response = bridge.get_crop_recommendation(req)
        
        # Render result
        return render_template('index_ultra_integrated.html',
                             result=response,
                             input_method='coordinates')
        
    except Exception as e:
        logger.error(f"Coordinate prediction failed: {e}")
        return render_template('index_ultra_integrated.html',
                             error=f"Prediction failed: {str(e)}")

@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Manual input endpoint (fallback)"""
    try:
        if bridge is None:
            return render_template('index_ultra_integrated.html',
                                 error="Integration system not available")
        
        # Get manual inputs
        features = {
            'nitrogen': float(request.form['Nitrogen']),
            'phosphorus': float(request.form['Phosphorus']),
            'potassium': float(request.form['Potassium']),
            'temperature': float(request.form['Temperature']),
            'humidity': float(request.form['Humidity']),
            'ph': float(request.form['Ph']),
            'rainfall': float(request.form['Rainfall'])
        }
        
        # Make prediction directly
        prediction = bridge._predict_crop(features)
        
        # Create mock response for template
        class MockResponse:
            def __init__(self):
                self.recommended_crop = prediction['crop_name']
                self.confidence_score = prediction['confidence']
                self.satellite_features = features
                self.processing_time_ms = 0
                self.cache_hit = False
                self.coordinates = {'latitude': 0, 'longitude': 0}
                self.region_info = {'climate_zone': 'Manual Input'}
        
        response = MockResponse()
        
        return render_template('index_ultra_integrated.html',
                             result=response,
                             input_method='manual')
        
    except Exception as e:
        logger.error(f"Manual prediction failed: {e}")
        return render_template('index_ultra_integrated.html',
                             error=f"Manual prediction failed: {str(e)}")

@app.route('/api/test_integration', methods=['GET'])
def test_integration():
    """Test the integration with sample data"""
    try:
        if bridge is None:
            return jsonify({'error': 'Bridge not available'}), 500
        
        # Test locations around the world
        test_locations = [
            {'name': 'California Agriculture', 'lat': 39.0372, 'lon': -121.8036},
            {'name': 'Iowa Corn Belt', 'lat': 42.0308, 'lon': -93.6319},
            {'name': 'India Rice Region', 'lat': 26.8467, 'lon': 80.9462},
            {'name': 'Brazil Soybean', 'lat': -14.2350, 'lon': -51.9253}
        ]
        
        results = []
        for location in test_locations:
            try:
                req = CropRecommendationRequest(
                    latitude=location['lat'],
                    longitude=location['lon'],
                    year=2024,
                    use_cache=False  # Force fresh data for testing
                )
                
                response = bridge.get_crop_recommendation(req)
                
                results.append({
                    'location': location['name'],
                    'coordinates': f"{location['lat']}, {location['lon']}",
                    'recommended_crop': response.recommended_crop,
                    'confidence': f"{response.confidence_score:.2f}",
                    'processing_time_ms': f"{response.processing_time_ms:.1f}",
                    'data_sources': response.data_sources,
                    'climate_zone': response.region_info.get('climate_zone', 'Unknown')
                })
                
            except Exception as e:
                results.append({
                    'location': location['name'],
                    'error': str(e)
                })
        
        return jsonify({
            'integration_test': 'completed',
            'results': results,
            'system_stats': bridge.get_performance_stats()
        })
        
    except Exception as e:
        return jsonify({'error': f'Integration test failed: {e}'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    # Use a different port to avoid conflicts
    port = 5001
    
    print("🚀 Starting Ultra-Integrated Crop Recommendation System")
    print("=" * 60)
    
    if bridge is None:
        print("❌ Warning: Integration bridge failed to initialize")
        print("   The system will run with limited functionality")
    else:
        print("✅ Integration bridge initialized successfully")
        print(f"   - ML Model: Loaded")
        print(f"   - AlphaEarth: {'Real' if bridge.use_real_alphaearth else 'Fallback'}")
        print(f"   - Async Processing: {'Enabled' if bridge.enable_async else 'Disabled'}")
        print(f"   - Cache Size: {bridge.cache_size}")
    
    print(f"\n🌐 Available Endpoints:")
    print(f"   - Main Interface: http://localhost:{port}/")
    print(f"   - API Recommend: POST /api/recommend")
    print(f"   - Health Check: GET /api/health")
    print(f"   - Performance Stats: GET /api/stats")
    print(f"   - Integration Test: GET /api/test_integration")
    
    print(f"\n🎯 Ready for ultra-fast crop recommendations!")
    print(f"   🌐 Open http://localhost:{port} in your browser")
    print(f"   📍 Click anywhere on the world map")
    print(f"   🛰️  Get instant satellite-based crop recommendations!")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port {port} is also in use. Trying port {port+1}...")
            app.run(debug=True, host='0.0.0.0', port=port+1, threaded=True)
        else:
            raise