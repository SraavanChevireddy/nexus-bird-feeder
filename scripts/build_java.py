#!/usr/bin/env python3
"""
Java Build and Integration Script
Builds JAR files and integrates them with Nexus Repository
"""

import os
import subprocess
import sys
import json
import requests
from pathlib import Path

def check_prerequisites():
    """Check if Java and Maven are available"""
    print("🔍 Checking prerequisites...")
    
    # Check Java
    try:
        java_result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if java_result.returncode == 0:
            print("✅ Java is available")
            java_version = java_result.stderr.split('\n')[0]
            print(f"   Version: {java_version}")
        else:
            print("❌ Java not found")
            return False
    except FileNotFoundError:
        print("❌ Java not found")
        return False
    
    # Check Maven
    try:
        maven_result = subprocess.run(['mvn', '-version'], capture_output=True, text=True)
        if maven_result.returncode == 0:
            print("✅ Maven is available")
            maven_version = maven_result.stdout.split('\n')[0]
            print(f"   Version: {maven_version}")
        else:
            print("❌ Maven not found")
            return False
    except FileNotFoundError:
        print("❌ Maven not found - please install Apache Maven")
        return False
    
    return True

def build_java_project():
    """Build the Java project using Maven"""
    print("\n🔨 Building Java project...")
    
    java_dir = Path("java")
    if not java_dir.exists():
        print("❌ Java directory not found")
        return False
    
    try:
        # Change to Java directory and run Maven build
        original_dir = os.getcwd()
        os.chdir(java_dir)
        
        # Clean and package
        result = subprocess.run([
            'mvn', 'clean', 'package', '-DskipTests'
        ], capture_output=True, text=True)
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print("✅ Java project built successfully")
            
            # Check if JAR was created
            jar_path = java_dir / "target" / "bird-analyzer-1.0.0.jar"
            if jar_path.exists():
                print(f"✅ JAR created: {jar_path}")
                
                # Copy JAR to java directory for easy access
                import shutil
                shutil.copy2(jar_path, java_dir / "bird-analyzer.jar")
                print("✅ JAR copied to java/bird-analyzer.jar")
                
                return True
            else:
                print("❌ JAR file not found after build")
                return False
        else:
            print("❌ Maven build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def test_java_integration():
    """Test the Java integration"""
    print("\n🧪 Testing Java integration...")
    
    try:
        # Create sample data
        sample_data = [
            {"bird_type": "Robin", "food_type": "Seeds", "quantity": 25},
            {"bird_type": "Cardinal", "food_type": "Nuts", "quantity": 30},
            {"bird_type": "Robin", "food_type": "Berries", "quantity": 15}
        ]
        
        # Test with subprocess (simulating standalone Java execution)
        jar_path = Path("java/bird-analyzer.jar")
        if jar_path.exists():
            # Create temp JSON file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(sample_data, f)
                temp_file = f.name
            
            try:
                result = subprocess.run([
                    'java', '-jar', str(jar_path), temp_file
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print("✅ Java analyzer executed successfully")
                    print("📊 Sample output:")
                    output = json.loads(result.stdout)
                    print(f"   Most common bird: {output.get('patterns', {}).get('most_common_bird')}")
                    print(f"   Analysis engine: {output.get('analysis_engine')}")
                    return True
                else:
                    print("❌ Java execution failed:")
                    print(result.stderr)
                    return False
                    
            finally:
                os.unlink(temp_file)
        else:
            print("❌ JAR file not found")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def upload_to_nexus():
    """Upload JAR to Nexus Repository"""
    print("\n📦 Uploading to Nexus Repository...")
    
    jar_path = Path("java/bird-analyzer.jar")
    if not jar_path.exists():
        print("❌ JAR file not found")
        return False
    
    try:
        # Upload to Nexus Maven repository
        nexus_url = "http://localhost:8081/repository/maven-releases/"
        group_id = "com.birdfeeding"
        artifact_id = "bird-analyzer"
        version = "1.0.0"
        
        # Use Maven deploy plugin
        java_dir = Path("java")
        original_dir = os.getcwd()
        os.chdir(java_dir)
        
        result = subprocess.run([
            'mvn', 'deploy',
            f'-DaltDeploymentRepository=nexus-releases::default::{nexus_url}',
            '-DskipTests'
        ], capture_output=True, text=True)
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print("✅ JAR uploaded to Nexus successfully")
            print(f"📍 Available at: {nexus_url}{group_id.replace('.', '/')}/{artifact_id}/{version}/")
            return True
        else:
            print("❌ Nexus upload failed:")
            print(result.stderr)
            
            # Try alternative upload method
            print("🔄 Trying alternative upload...")
            return upload_jar_directly()
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def upload_jar_directly():
    """Direct JAR upload to Nexus using REST API"""
    try:
        jar_path = Path("java/bird-analyzer.jar")
        
        # Upload to raw repository for now
        upload_url = "http://localhost:8081/repository/test-raw/bird-analyzer.jar"
        
        with open(jar_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                auth=('admin', 'admin123'),
                headers={'Content-Type': 'application/java-archive'}
            )
        
        if response.status_code in [200, 201]:
            print("✅ JAR uploaded to Nexus (raw repository)")
            print(f"📍 Available at: {upload_url}")
            return True
        else:
            print(f"❌ Direct upload failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Direct upload error: {e}")
        return False

def install_jpype():
    """Install JPype1 for Java-Python integration"""
    print("\n🐍 Installing JPype1 for Java integration...")
    
    try:
        env = os.environ.copy()
        env['PIP_CONFIG_FILE'] = 'config/pip.conf'
        
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'JPype1>=1.4.0'
        ], env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ JPype1 installed successfully")
            return True
        else:
            print("❌ JPype1 installation failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ JPype1 installation error: {e}")
        return False

def main():
    """Main build and integration process"""
    print("🚀 Java Integration Setup for Bird Feeding Project")
    print("=" * 60)
    
    steps = [
        ("Prerequisites Check", check_prerequisites),
        ("Install JPype1", install_jpype),
        ("Build Java Project", build_java_project),
        ("Test Integration", test_java_integration),
        ("Upload to Nexus", upload_to_nexus)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_func():
            print(f"\n❌ Build process failed at: {step_name}")
            print("Please resolve the issue and try again")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Java integration setup completed successfully!")
    print("\n📝 What's been accomplished:")
    print("✅ Java project built and packaged")
    print("✅ JAR file uploaded to Nexus Repository")
    print("✅ Python-Java bridge (JPype1) installed")
    print("✅ Integration tested and verified")
    
    print("\n🚀 Next steps:")
    print("1. Test the new endpoints: /api/analyze, /api/report")
    print("2. Check Java status: GET /api/java/status")
    print("3. Use advanced analytics in your bird feeding API")
    
    print("\n💡 Java integration features now available:")
    print("• Advanced pattern analysis using Java algorithms")
    print("• PDF report generation with Java libraries")
    print("• Maven artifact management through Nexus")
    print("• Polyglot development (Python + Java)")

if __name__ == "__main__":
    main()
