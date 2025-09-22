#!/usr/bin/env python3
"""
Script to populate Nexus Repository with Maven dependencies
Demonstrates why Java dependencies aren't showing and how to get them there
"""

import requests
import json
import subprocess
import sys
import os

def check_nexus_maven_repos():
    """Check what Maven repositories exist in Nexus"""
    print("🔍 Checking Nexus Maven Repositories...")
    
    try:
        response = requests.get(
            "http://localhost:8081/service/rest/v1/repositories",
            auth=('admin', 'admin123')
        )
        
        if response.status_code == 200:
            repos = response.json()
            maven_repos = [r for r in repos if r['format'] == 'maven2']
            
            print(f"✅ Found {len(maven_repos)} Maven repositories:")
            for repo in maven_repos:
                print(f"   📦 {repo['name']} ({repo['type']})")
            
            return maven_repos
        else:
            print(f"❌ Failed to get repositories: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error checking repositories: {e}")
        return []

def check_maven_artifacts():
    """Check what Maven artifacts are currently in Nexus"""
    print("\n🔍 Checking Maven Artifacts in Nexus...")
    
    maven_repos = ['maven-central', 'maven-public', 'maven-releases', 'maven-snapshots']
    
    for repo in maven_repos:
        try:
            response = requests.get(
                f"http://localhost:8081/service/rest/v1/search?repository={repo}",
                auth=('admin', 'admin123')
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('items', []))
                print(f"   📦 {repo}: {count} artifacts")
                
                if count > 0:
                    # Show first few artifacts
                    for item in data['items'][:3]:
                        print(f"      • {item.get('group', 'unknown')}:{item.get('name', 'unknown')}:{item.get('version', 'unknown')}")
                    if count > 3:
                        print(f"      ... and {count - 3} more")
            else:
                print(f"   ❌ {repo}: Failed to check ({response.status_code})")
                
        except Exception as e:
            print(f"   ❌ {repo}: Error - {e}")

def explain_why_empty():
    """Explain why Maven repositories are empty"""
    print("\n💡 Why Your Nexus Maven Repositories Are Empty:")
    print("=" * 60)
    
    reasons = [
        "🏗️  No Maven builds have run yet",
        "📦 Dependencies are only cached when requested",
        "🔧 Maven needs to be configured to use Nexus",
        "⚡ Nexus proxy repositories start empty until first use",
        "🎯 Your project is Python-focused, so Maven wasn't used"
    ]
    
    for i, reason in enumerate(reasons, 1):
        print(f"{i}. {reason}")

def demonstrate_maven_download():
    """Demonstrate how to populate Nexus with Maven dependencies"""
    print("\n🚀 How to Populate Nexus with Java Dependencies:")
    print("=" * 60)
    
    methods = [
        {
            "name": "Method 1: Maven Build (Recommended)",
            "steps": [
                "Install Maven: brew install maven (macOS) or apt install maven (Linux)",
                "Configure Maven to use Nexus (settings.xml)",
                "Run: mvn dependency:resolve in java/ directory",
                "Dependencies will be downloaded and cached in Nexus"
            ]
        },
        {
            "name": "Method 2: Direct API Upload",
            "steps": [
                "Download JAR files manually",
                "Upload via Nexus REST API",
                "Useful for specific JARs you need"
            ]
        },
        {
            "name": "Method 3: Gradle Build",
            "steps": [
                "Use Gradle instead of Maven",
                "Configure Gradle to use Nexus repositories",
                "Run gradle build to populate cache"
            ]
        }
    ]
    
    for method in methods:
        print(f"\n📋 {method['name']}:")
        for i, step in enumerate(method['steps'], 1):
            print(f"   {i}. {step}")

def simulate_maven_population():
    """Simulate what would happen when Maven runs"""
    print("\n🎭 Simulation: What Happens When Maven Runs")
    print("=" * 50)
    
    dependencies = [
        "com.fasterxml.jackson.core:jackson-databind:2.15.2",
        "com.fasterxml.jackson.core:jackson-core:2.15.2",
        "com.fasterxml.jackson.core:jackson-annotations:2.15.2",
        "junit:junit:4.13.2",
        "org.hamcrest:hamcrest-core:1.3"
    ]
    
    print("📦 Dependencies that would be downloaded to Nexus:")
    for dep in dependencies:
        print(f"   • {dep}")
        
    print("\n🔄 Maven Process:")
    print("   1. Maven reads pom.xml")
    print("   2. Checks local cache (~/.m2/repository)")
    print("   3. If not found, requests from Nexus")
    print("   4. Nexus checks its cache")
    print("   5. If not cached, Nexus downloads from Maven Central")
    print("   6. Nexus caches the artifact")
    print("   7. Nexus serves it to Maven")
    print("   8. Maven caches it locally")

def create_maven_settings():
    """Create Maven settings.xml to use Nexus"""
    print("\n⚙️ Creating Maven Configuration for Nexus...")
    
    settings_xml = """<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 
          http://maven.apache.org/xsd/settings-1.0.0.xsd">
    
    <mirrors>
        <mirror>
            <id>nexus</id>
            <mirrorOf>*</mirrorOf>
            <url>http://localhost:8081/repository/maven-public/</url>
        </mirror>
    </mirrors>
    
    <profiles>
        <profile>
            <id>nexus</id>
            <repositories>
                <repository>
                    <id>central</id>
                    <url>http://central</url>
                    <releases><enabled>true</enabled></releases>
                    <snapshots><enabled>true</enabled></snapshots>
                </repository>
            </repositories>
            <pluginRepositories>
                <pluginRepository>
                    <id>central</id>
                    <url>http://central</url>
                    <releases><enabled>true</enabled></releases>
                    <snapshots><enabled>true</enabled></snapshots>
                </pluginRepository>
            </pluginRepositories>
        </profile>
    </profiles>
    
    <activeProfiles>
        <activeProfile>nexus</activeProfile>
    </activeProfiles>
    
    <servers>
        <server>
            <id>nexus</id>
            <username>admin</username>
            <password>admin123</password>
        </server>
    </servers>
</settings>"""
    
    settings_dir = os.path.expanduser("~/.m2")
    os.makedirs(settings_dir, exist_ok=True)
    settings_path = os.path.join(settings_dir, "settings.xml")
    
    try:
        with open(settings_path, 'w') as f:
            f.write(settings_xml)
        print(f"✅ Maven settings created: {settings_path}")
        print("   This configures Maven to use your Nexus repository")
        return True
    except Exception as e:
        print(f"❌ Failed to create settings: {e}")
        return False

def test_maven_availability():
    """Test if Maven is available and working"""
    print("\n🧪 Testing Maven Availability...")
    
    try:
        result = subprocess.run(['mvn', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ Maven available: {version_line}")
            return True
        else:
            print("❌ Maven command failed")
            return False
    except FileNotFoundError:
        print("❌ Maven not installed")
        print("   Install with: brew install maven (macOS) or apt install maven (Linux)")
        return False

def main():
    """Main demonstration function"""
    print("🔍 Nexus Maven Dependencies Investigation")
    print("=" * 70)
    print("Understanding why Java dependencies aren't showing in Nexus\n")
    
    # Check current state
    maven_repos = check_nexus_maven_repos()
    check_maven_artifacts()
    
    # Explain the situation
    explain_why_empty()
    
    # Show how to fix it
    demonstrate_maven_download()
    simulate_maven_population()
    
    # Create Maven configuration
    if create_maven_settings():
        print("\n✅ Maven configuration ready for Nexus")
    
    # Test Maven
    maven_available = test_maven_availability()
    
    print("\n" + "=" * 70)
    print("🎯 SUMMARY: Why Java Dependencies Aren't in Nexus")
    print("=" * 70)
    
    summary_points = [
        "✅ Nexus HAS Maven repositories (maven-central, maven-public, etc.)",
        "❌ No Maven builds have run yet, so repositories are empty",
        "🔧 Maven needs to be installed and configured to use Nexus",
        "📦 Dependencies only appear when actually requested by builds",
        "🎯 Your Python project works fine - this is just for Java enhancement"
    ]
    
    for point in summary_points:
        print(f"• {point}")
    
    print(f"\n🚀 Next Steps:")
    if maven_available:
        print("1. Run: cd java && mvn dependency:resolve")
        print("2. Check Nexus web UI - you'll see Java dependencies appear!")
        print("3. Your Java integration will be fully functional")
    else:
        print("1. Install Maven: brew install maven")
        print("2. Run: cd java && mvn dependency:resolve") 
        print("3. Watch Java dependencies populate in Nexus!")
    
    print(f"\n💡 Remember: This is normal! Nexus repositories start empty.")
    print(f"   They only populate when applications actually request dependencies.")

if __name__ == "__main__":
    main()
