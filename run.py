#!/usr/bin/env python3
"""
BeeAiRating - Application Startup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import flask
        import numpy
        import pandas
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables and directories"""
    print("🔧 Setting up environment...")
    
    # Create necessary directories
    directories = ['logs', 'models', 'temp', 'uploads']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("⚠️  .env file not found. Creating from template...")
        if Path('env.example').exists():
            with open('env.example', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✅ Created .env file from template")
        else:
            print("❌ env.example not found")
    
    print("✅ Environment setup complete")

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pytest', 'test_app.py', '-v'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def start_application():
    """Start the Flask application"""
    print("🚀 Starting BeeAiRating application...")
    
    try:
        # Import and run the main application
        from app import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🐝 Welcome to BeeAiRating!")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Run tests (optional - can be skipped in production)
    if len(sys.argv) > 1 and sys.argv[1] == '--skip-tests':
        print("⏭️  Skipping tests")
    else:
        if not run_tests():
            print("⚠️  Tests failed, but continuing...")
    
    # Start application
    start_application()

if __name__ == '__main__':
    main() 