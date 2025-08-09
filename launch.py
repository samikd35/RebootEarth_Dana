#!/usr/bin/env python3
"""
AlphaEarth Crop Recommender - Main Launcher

This is the main entry point for the AlphaEarth crop recommendation system.
It handles the structured folder imports and launches the web application.
"""

import sys
import os
import socket
import subprocess
import webbrowser
from pathlib import Path
from threading import Timer

# Add the src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

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
    print("🚀 AlphaEarth Crop Recommender - Structured Launch")
    print("=" * 60)
    
    # Find available port
    port = find_free_port()
    if port is None:
        print("❌ Could not find an available port. Please check your system.")
        sys.exit(1)
    
    print(f"✅ Found available port: {port}")
    
    # Set environment variable for Google Cloud
    if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
        os.environ['GOOGLE_CLOUD_PROJECT'] = 'reboot-468512'
        print("✅ Set GOOGLE_CLOUD_PROJECT environment variable")
    
    # Create a temporary launcher script
    launcher_script = f"""
import sys
import os
from pathlib import Path

# Add src to path
project_root = Path.cwd()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Set environment
os.environ['GOOGLE_CLOUD_PROJECT'] = 'reboot-468512'

# Import and run the web app
try:
    from web.app_ultra_integrated import app, bridge
    
    print("🚀 Starting AlphaEarth Crop Recommendation System")
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
    
except ImportError as e:
    print(f"❌ Import error: {{e}}")
    import traceback
    traceback.print_exc()
    print("Make sure all dependencies are installed and paths are correct")
    sys.exit(1)
except Exception as e:
    print(f"❌ Startup error: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
    
    # Write the launcher script to a temporary file
    temp_launcher = project_root / "temp_launcher.py"
    with open(temp_launcher, 'w') as f:
        f.write(launcher_script)
    
    # Prepare the launch command
    launch_cmd = [sys.executable, str(temp_launcher)]
    
    # Schedule browser opening
    url = f"http://localhost:{port}"
    open_browser_delayed(url, delay=4)
    
    print(f"🌐 Will open browser at: {url}")
    print(f"⏳ Starting server...")
    print(f"⏹️  Press Ctrl+C to stop")
    print()
    
    try:
        # Launch the application
        subprocess.run(launch_cmd, check=True, cwd=project_root)
    except KeyboardInterrupt:
        print("\\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\\n❌ Server failed to start: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary launcher
        temp_launcher = project_root / "temp_launcher.py"
        if temp_launcher.exists():
            temp_launcher.unlink()

if __name__ == "__main__":
    main()