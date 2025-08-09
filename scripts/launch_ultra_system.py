#!/usr/bin/env python3
"""
Smart launcher for the Ultra-Integrated Crop Recommendation System
Automatically finds an available port and launches the system
"""

import socket
import subprocess
import sys
import time
import webbrowser
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
    print("🚀 Ultra-Integrated Crop Recommendation System Launcher")
    print("=" * 60)
    
    # Find available port
    port = find_free_port()
    if port is None:
        print("❌ Could not find an available port. Please check your system.")
        sys.exit(1)
    
    print(f"✅ Found available port: {port}")
    
    # Prepare the launch command
    launch_cmd = [
        sys.executable, "-c", f"""
import sys
sys.path.append('.')

from app_ultra_integrated import app, bridge

print("🚀 Starting Ultra-Integrated Crop Recommendation System")
print("=" + "=" * 60)

if bridge is None:
    print("❌ Warning: Integration bridge failed to initialize")
    print("   The system will run with limited functionality")
else:
    print("✅ Integration bridge initialized successfully")
    print(f"   - ML Model: Loaded")
    print(f"   - AlphaEarth: {{'Real' if bridge.use_real_alphaearth else 'Fallback'}}")
    print(f"   - Async Processing: {{'Enabled' if bridge.enable_async else 'Disabled'}}")
    print(f"   - Cache Size: {{bridge.cache_size}}")

print(f"\\n🌐 Available Endpoints:")
print(f"   - Main Interface: http://localhost:{port}/")
print(f"   - API Recommend: POST /api/recommend")
print(f"   - Health Check: GET /api/health")
print(f"   - Performance Stats: GET /api/stats")
print(f"   - Integration Test: GET /api/test_integration")

print(f"\\n🎯 Ready for ultra-fast crop recommendations!")
print(f"   🌐 Open http://localhost:{port} in your browser")
print(f"   📍 Click anywhere on the world map")
print(f"   🛰️  Get instant satellite-based crop recommendations!")
print(f"\\n⏹️  Press Ctrl+C to stop the server")

app.run(debug=False, host='0.0.0.0', port={port}, threaded=True)
"""
    ]
    
    # Schedule browser opening
    url = f"http://localhost:{port}"
    open_browser_delayed(url, delay=4)
    
    print(f"🌐 Will open browser at: {url}")
    print(f"⏳ Starting server...")
    print(f"⏹️  Press Ctrl+C to stop")
    print()
    
    try:
        # Launch the application
        subprocess.run(launch_cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()