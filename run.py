#!/usr/bin/env python3
"""
Direct launcher for AlphaEarth Crop Recommender

This launcher runs the application directly without subprocess complications.
"""

import sys
import os
import socket
import webbrowser
from pathlib import Path
from threading import Timer

def find_free_port(start_port=5001, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def open_browser_delayed(url, delay=3):
    """Open browser after a delay"""
    def open_browser():
        print(f"🌐 Opening browser: {url}")
        webbrowser.open(url)
    
    Timer(delay, open_browser).start()

def main():
    """Main launcher function"""
    print("🚀 AlphaEarth Crop Recommender - Direct Launch")
    print("=" * 60)
    
    # Setup paths
    project_root = Path(__file__).parent
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    
    # Set environment
    if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
        os.environ['GOOGLE_CLOUD_PROJECT'] = 'reboot-468512'
        print("✅ Set GOOGLE_CLOUD_PROJECT environment variable")
    
    # Find available port
    port = find_free_port()
    if port is None:
        print("❌ Could not find an available port. Please check your system.")
        sys.exit(1)
    
    print(f"✅ Found available port: {port}")
    
    # Schedule browser opening
    url = f"http://localhost:{port}"
    open_browser_delayed(url, delay=4)
    print(f"🌐 Will open browser at: {url}")
    
    try:
        # Import and run the web app
        from web.app_ultra_integrated import app, bridge
        
        print("🚀 Starting AlphaEarth Crop Recommendation System")
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
        print(f"\n⏹️  Press Ctrl+C to stop the server")
        
        # Run the Flask app
        app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that all files are in the correct locations")
        print("3. Try running: python setup.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()