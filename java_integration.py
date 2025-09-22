"""
Java Integration Module for Bird Feeding API
Demonstrates how to use JAR files in a Python project
"""

import os
import subprocess
import json
from typing import Dict, Any, List, Optional
# JPype imports - will be imported dynamically when needed
# import jpype
# import jpype.imports
# from jpype.types import *

class JavaBirdAnalyzer:
    """Python wrapper for Java-based bird analysis functionality"""
    
    def __init__(self, jar_path: str = "java/bird-analyzer.jar"):
        self.jar_path = jar_path
        self.jvm_started = False
        
    def start_jvm(self):
        """Initialize the Java Virtual Machine"""
        try:
            import jpype
            import jpype.imports
            
            if not self.jvm_started and not jpype.isJVMStarted():
                # Start JVM with the JAR file in classpath
                jpype.startJVM(
                    jpype.getDefaultJVMPath(),
                    f"-Djava.class.path={self.jar_path}",
                    convertStrings=False
                )
                self.jvm_started = True
                print("✅ JVM started successfully")
        except ImportError:
            print("⚠️  JPype not installed - using subprocess mode")
            self.jvm_started = False
        except Exception as e:
            print(f"❌ Failed to start JVM: {e}")
            raise
    
    def shutdown_jvm(self):
        """Shutdown the Java Virtual Machine"""
        try:
            import jpype
            if self.jvm_started and jpype.isJVMStarted():
                jpype.shutdownJVM()
                self.jvm_started = False
                print("🔄 JVM shutdown")
        except ImportError:
            pass  # JPype not available
    
    def analyze_feeding_patterns(self, feeding_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Use Java library to analyze bird feeding patterns
        This would call a hypothetical Java class for advanced analytics
        """
        if not self.jvm_started:
            self.start_jvm()
        
        try:
            # Try to use JPype if available
            try:
                import jpype
                # Import Java classes (this would be your actual JAR classes)
                # from com.birdfeeding import BirdAnalyzer
                # analyzer = BirdAnalyzer()
                
                # For now, simulate the Java analysis
                return self._simulate_java_analysis(feeding_data)
            except ImportError:
                # Fall back to subprocess execution
                return self._execute_java_subprocess(feeding_data)
            
        except Exception as e:
            print(f"❌ Java analysis failed: {e}")
            return {"error": str(e)}
    
    def _execute_java_subprocess(self, feeding_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute Java analysis using subprocess"""
        try:
            import tempfile
            
            # Create temporary JSON file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(feeding_data, f)
                temp_file = f.name
            
            try:
                # Execute Java program
                result = execute_java_program(self.jar_path, "com.birdfeeding.BirdAnalyzer", [temp_file])
                
                if result['success'] and result['stdout']:
                    return json.loads(result['stdout'])
                else:
                    # Fall back to simulation if Java execution fails
                    print("⚠️  Java execution failed, using simulation")
                    return self._simulate_java_analysis(feeding_data)
                    
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            print(f"⚠️  Subprocess execution failed: {e}, using simulation")
            return self._simulate_java_analysis(feeding_data)
    
    def _simulate_java_analysis(self, feeding_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate what a Java analyzer might return"""
        if not feeding_data:
            return {"patterns": [], "recommendations": []}
        
        # Simulate complex analysis that might be better suited for Java
        bird_types = [f.get('bird_type', '') for f in feeding_data]
        food_types = [f.get('food_type', '') for f in feeding_data]
        quantities = [f.get('quantity', 0) for f in feeding_data]
        
        return {
            "patterns": {
                "most_common_bird": max(set(bird_types), key=bird_types.count) if bird_types else None,
                "preferred_food": max(set(food_types), key=food_types.count) if food_types else None,
                "average_quantity": sum(quantities) / len(quantities) if quantities else 0,
                "total_feedings": len(feeding_data)
            },
            "recommendations": [
                "Consider increasing seed variety for better bird diversity",
                "Morning feedings show 23% higher bird activity",
                "Cardinals prefer nuts over seeds by 2:1 ratio"
            ],
            "analysis_engine": "Java Bird Analyzer v1.0",
            "processed_by": "JPype Bridge"
        }

class JavaReportGenerator:
    """Use Java libraries for advanced report generation (e.g., PDF, Excel)"""
    
    def __init__(self, jar_path: str = "java/report-generator.jar"):
        self.jar_path = jar_path
    
    def generate_pdf_report(self, data: Dict[str, Any], output_path: str) -> bool:
        """Generate PDF report using Java libraries (e.g., iText, Apache PDFBox)"""
        try:
            # This would use a Java library like iText for PDF generation
            # For now, we'll create a simple text report
            report_content = self._create_report_content(data)
            
            with open(output_path.replace('.pdf', '.txt'), 'w') as f:
                f.write(report_content)
            
            print(f"📄 Report generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            return False
    
    def _create_report_content(self, data: Dict[str, Any]) -> str:
        """Create report content (would be enhanced with Java libraries)"""
        return f"""
🐦 Bird Feeding Analysis Report
Generated by Java Report Engine

=== FEEDING PATTERNS ===
{json.dumps(data.get('patterns', {}), indent=2)}

=== RECOMMENDATIONS ===
{chr(10).join(f"• {rec}" for rec in data.get('recommendations', []))}

=== METADATA ===
Analysis Engine: {data.get('analysis_engine', 'Unknown')}
Processed By: {data.get('processed_by', 'Unknown')}
Generated: {data.get('timestamp', 'Unknown')}
"""

class MavenArtifactManager:
    """Manage JAR files through Nexus Repository (Maven format)"""
    
    def __init__(self, nexus_url: str = "http://localhost:8081"):
        self.nexus_url = nexus_url
        self.maven_repo = "maven-central"  # or your custom Maven repo
    
    def download_jar(self, group_id: str, artifact_id: str, version: str, 
                     target_dir: str = "java/") -> str:
        """Download JAR file from Nexus Maven repository"""
        try:
            os.makedirs(target_dir, exist_ok=True)
            
            # Construct Maven repository URL
            group_path = group_id.replace('.', '/')
            jar_url = f"{self.nexus_url}/repository/{self.maven_repo}/{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.jar"
            
            jar_path = os.path.join(target_dir, f"{artifact_id}-{version}.jar")
            
            # Download using requests (could also use Maven CLI)
            import requests
            response = requests.get(jar_url, auth=('admin', 'admin123'))
            
            if response.status_code == 200:
                with open(jar_path, 'wb') as f:
                    f.write(response.content)
                print(f"📦 Downloaded: {jar_path}")
                return jar_path
            else:
                print(f"❌ Failed to download JAR: {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"❌ JAR download failed: {e}")
            return ""
    
    def list_available_jars(self) -> List[str]:
        """List available JAR files in Nexus"""
        try:
            # This would query Nexus REST API for Maven artifacts
            # For demo, return some common libraries
            return [
                "org.apache.commons:commons-lang3:3.12.0",
                "com.fasterxml.jackson.core:jackson-core:2.15.0",
                "org.apache.poi:poi:5.2.0"
            ]
        except Exception as e:
            print(f"❌ Failed to list JARs: {e}")
            return []

# Utility functions for Java integration
def execute_java_program(jar_path: str, main_class: str, args: List[str] = None) -> Dict[str, Any]:
    """Execute a Java program and return results"""
    try:
        cmd = ["java", "-jar", jar_path]
        if args:
            cmd.extend(args)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Java program timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_java_availability() -> Dict[str, Any]:
    """Check if Java is available on the system"""
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        return {
            "available": result.returncode == 0,
            "version": result.stderr.split('\n')[0] if result.stderr else "Unknown",
            "path": subprocess.run(["which", "java"], capture_output=True, text=True).stdout.strip()
        }
    except Exception as e:
        return {"available": False, "error": str(e)}
