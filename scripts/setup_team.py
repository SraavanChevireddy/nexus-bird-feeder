#!/usr/bin/env python3
"""
Team setup automation script
Helps new team members get up and running quickly
"""

import os
import subprocess
import sys
import requests
import json

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_nexus_connection():
    """Check if Nexus Repository is accessible"""
    try:
        response = requests.get("http://localhost:8081", timeout=5)
        if response.status_code == 200:
            print("✅ Nexus Repository accessible at http://localhost:8081")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("❌ Nexus Repository not accessible at http://localhost:8081")
    print("   Please ensure Nexus is running before continuing")
    return False

def install_dependencies():
    """Install Python dependencies via Nexus"""
    print("📦 Installing dependencies via Nexus...")
    try:
        env = os.environ.copy()
        env['PIP_CONFIG_FILE'] = 'config/pip.conf'
        
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_application():
    """Test if the application can start"""
    print("🧪 Testing application startup...")
    try:
        # Import the main app to test for import errors
        sys.path.append('.')
        from app import app
        
        print("✅ Application imports successfully")
        return True
    except Exception as e:
        print(f"❌ Application import failed: {e}")
        return False

def main():
    """Main setup process"""
    print("🚀 Bird Feeding Project - Team Setup")
    print("=" * 50)
    
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    checks = [
        ("Python Version", check_python_version),
        ("Nexus Connection", check_nexus_connection),
        ("Install Dependencies", install_dependencies),
        ("Test Application", test_application)
    ]
    
    for name, check_func in checks:
        print(f"\n🔍 {name}...")
        if not check_func():
            print(f"\n❌ Setup failed at: {name}")
            print("Please resolve the issue and try again")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Read the documentation: docs/README.md")
    print("2. Start the application: python3 app.py")
    print("3. Test the API: curl http://localhost:8080")
    print("4. Run the demo: python3 scripts/demo_observe.py")
    print("\n💡 For troubleshooting, see: docs/TEAM_SETUP.md")

if __name__ == "__main__":
    main()
