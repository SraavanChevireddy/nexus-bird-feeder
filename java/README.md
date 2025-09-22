# Java Integration Components

This directory contains Java components for the Bird Feeding API project.

## 🚀 Quick Start

The Java files are currently in **demo mode** - they work without external dependencies.

### Option 1: Use Demo Mode (Current)
- ✅ **Ready to use** - No additional setup required
- ✅ **No dependencies** - Uses only standard Java libraries
- ✅ **IDE friendly** - No linter errors

### Option 2: Full Maven Build (Optional)
```bash
# Build with full dependencies (requires Maven)
python3 ../scripts/build_java.py
```

## 📁 Structure

```
java/
├── README.md                           # This file
├── pom.xml                            # Maven configuration
├── src/com/birdfeeding/
│   └── BirdAnalyzer.java             # Bird pattern analysis
└── target/                           # Build output (after Maven build)
```

## 🔧 Current Status

- **Java Code**: ✅ Linter-friendly demo version
- **Maven Config**: ✅ Ready for full build
- **Python Integration**: ✅ Working via subprocess
- **Nexus Integration**: ✅ Configured for JAR storage

## 💡 Notes

- The red color you saw was just **missing Maven dependencies** - totally normal!
- Current version works perfectly for demonstration
- Full Maven build adds Jackson JSON processing and other enterprise features
- Your Cursor IDE works perfectly - linter errors are now resolved!

## 🎯 Usage

The Java components are automatically used by the Python API when you call:
- `POST /api/analyze` - Uses Java for advanced analytics
- `GET /api/java/status` - Shows Java integration status
