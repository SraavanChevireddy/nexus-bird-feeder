#!/usr/bin/env python3
"""
Demo script for Java integration features
Tests the Java-enhanced bird feeding API endpoints
"""

import requests
import json
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8080"

def test_java_status():
    """Test Java integration status"""
    print("🔍 Testing Java integration status...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/java/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Java status retrieved successfully")
            print(f"   Java available: {data['java_runtime']['available']}")
            print(f"   JAR files: {data['jar_files']}")
            print(f"   Integration ready: {data['integration_ready']}")
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False

def add_sample_data():
    """Add sample bird feeding data for analysis"""
    print("\n📊 Adding sample data for Java analysis...")
    
    sample_feedings = [
        {"bird_type": "Robin", "food_type": "Seeds", "quantity": 25, "location": "Front yard"},
        {"bird_type": "Cardinal", "food_type": "Nuts", "quantity": 30, "location": "Back yard"},
        {"bird_type": "Blue Jay", "food_type": "Nuts", "quantity": 35, "location": "Oak tree"},
        {"bird_type": "Robin", "food_type": "Berries", "quantity": 15, "location": "Garden"},
        {"bird_type": "Sparrow", "food_type": "Seeds", "quantity": 20, "location": "Feeder 1"},
        {"bird_type": "Cardinal", "food_type": "Seeds", "quantity": 25, "location": "Feeder 2"},
        {"bird_type": "Blue Jay", "food_type": "Peanuts", "quantity": 40, "location": "Platform feeder"}
    ]
    
    added_count = 0
    for feeding in sample_feedings:
        try:
            response = requests.post(
                f"{BASE_URL}/api/feedings",
                headers={'Content-Type': 'application/json'},
                json=feeding
            )
            if response.status_code == 201:
                added_count += 1
            time.sleep(0.1)  # Small delay between requests
        except Exception as e:
            print(f"❌ Failed to add feeding: {e}")
    
    print(f"✅ Added {added_count} sample feedings")
    return added_count > 0

def test_java_analysis():
    """Test Java-powered analysis"""
    print("\n🔬 Testing Java-powered analysis...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/analyze")
        if response.status_code == 200:
            data = response.json()
            print("✅ Java analysis completed successfully")
            print(f"   Analysis engine: {data.get('analysis_engine', 'Unknown')}")
            print(f"   Processed by: {data.get('processed_by', 'Unknown')}")
            
            patterns = data.get('patterns', {})
            print("\n📊 Analysis Results:")
            print(f"   Most common bird: {patterns.get('most_common_bird')}")
            print(f"   Preferred food: {patterns.get('preferred_food')}")
            print(f"   Average quantity: {patterns.get('average_quantity')}")
            print(f"   Total feedings: {patterns.get('total_feedings')}")
            print(f"   Bird diversity: {patterns.get('bird_diversity')}")
            
            recommendations = data.get('recommendations', [])
            if recommendations:
                print("\n💡 Recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"   {i}. {rec}")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_report_generation():
    """Test Java-powered report generation"""
    print("\n📄 Testing Java-powered report generation...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/report",
            headers={'Content-Type': 'application/json'},
            json={"type": "detailed"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Report generation completed successfully")
            print(f"   Report path: {data.get('path')}")
            print(f"   Report type: {data.get('type')}")
            
            # Check if report file exists
            report_path = data.get('path', '').replace('.pdf', '.txt')
            if os.path.exists(report_path):
                print(f"✅ Report file created: {report_path}")
                
                # Show first few lines of the report
                with open(report_path, 'r') as f:
                    lines = f.readlines()[:10]
                    print("\n📋 Report preview:")
                    for line in lines:
                        print(f"   {line.rstrip()}")
                    if len(lines) == 10:
                        print("   ...")
            
            return True
        else:
            print(f"❌ Report generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Report generation error: {e}")
        return False

def test_enhanced_api_info():
    """Test enhanced API info with Java integration"""
    print("\n🌐 Testing enhanced API info...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced API info retrieved")
            
            java_info = data.get('java_integration', {})
            print(f"   Java features: {java_info.get('features', [])}")
            print(f"   Java available: {java_info.get('available', {}).get('available', False)}")
            
            return True
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API info error: {e}")
        return False

def demo_complete_workflow():
    """Demonstrate complete Java-enhanced workflow"""
    print("\n🚀 Complete Java Integration Demo")
    print("=" * 50)
    
    tests = [
        ("Java Status Check", test_java_status),
        ("Enhanced API Info", test_enhanced_api_info),
        ("Add Sample Data", add_sample_data),
        ("Java Analysis", test_java_analysis),
        ("Report Generation", test_report_generation)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"⚠️  {test_name} failed, but continuing...")
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"🎯 Demo Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All Java integration features working perfectly!")
    elif passed >= len(tests) // 2:
        print("✅ Java integration mostly working - some features may need setup")
    else:
        print("⚠️  Java integration needs attention - check setup and dependencies")
    
    print("\n💡 Java Integration Features Demonstrated:")
    print("• Advanced analytics using Java algorithms")
    print("• Report generation with Java libraries")
    print("• Python-Java interoperability with JPype")
    print("• Maven artifact management through Nexus")
    print("• Polyglot development patterns")

def main():
    """Main demo function"""
    print("🔬 Java Integration Demo - Bird Feeding API")
    print("This demo showcases Java JAR integration with your Python project")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Bird Feeding API is not responding")
            print("Please start the server with: python3 app.py")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Bird Feeding API")
        print("Please ensure the server is running at http://localhost:8080")
        sys.exit(1)
    
    print("✅ Bird Feeding API is running")
    
    # Run the complete demo
    demo_complete_workflow()

if __name__ == "__main__":
    main()
