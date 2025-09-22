#!/usr/bin/env python3
"""
Demo script to showcase Observe logging integration
Run this while the Flask app is running to see structured logs in action

Usage: python3 scripts/demo_observe.py
"""

import requests
import json
import time
import sys
import os

# Add parent directory to path so we can import from the main app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8080"

def demo_observe_logging():
    """Demonstrate various API calls that generate Observe logs"""
    
    print("🔍 Observe Logging Demo - Bird Feeding API")
    print("=" * 50)
    
    # Test 1: Get API info
    print("\n1. 📋 Getting API information...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    
    # Test 2: Add a feeding record
    print("\n2. 🐦 Adding bird feeding record...")
    feeding_data = {
        "bird_type": "Blue Jay",
        "food_type": "Nuts",
        "quantity": 45,
        "location": "Oak tree",
        "notes": "Observe logging demo - Beautiful blue jay!"
    }
    response = requests.post(
        f"{BASE_URL}/api/feedings",
        json=feeding_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"   Created feeding ID: {result['id']}")
    
    # Test 3: Get all feedings
    print("\n3. 📊 Retrieving all feeding records...")
    response = requests.get(f"{BASE_URL}/api/feedings")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        feedings = response.json()
        print(f"   Total records: {len(feedings)}")
    
    # Test 4: Get statistics
    print("\n4. 📈 Getting feeding statistics...")
    response = requests.get(f"{BASE_URL}/api/stats")
    print(f"   Status: {response.status_code}")
    
    # Test 5: Trigger validation error (for error logging)
    print("\n5. ❌ Testing error logging (missing required field)...")
    bad_data = {"bird_type": "Robin"}  # Missing required fields
    response = requests.post(
        f"{BASE_URL}/api/feedings",
        json=bad_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status: {response.status_code} (Expected 400)")
    
    print("\n" + "=" * 50)
    print("✅ Demo complete!")
    print("\n📊 Check your Flask app terminal for structured logs like:")
    print('   📊 OBSERVE: {"event_type": "feeding_created_successfully", ...}')
    print('   📊 OBSERVE: {"event_type": "http_request_end", "duration_ms": 23.45, ...}')
    print("\n💡 In production, these logs would be sent to Observe.inc platform")

if __name__ == "__main__":
    try:
        demo_observe_logging()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Flask app not running!")
        print("   Start the app with: python3 app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
