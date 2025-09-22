# 🚀 Team Setup Guide - Bird Feeding Project

## 📋 Prerequisites
- Python 3.8+ installed
- Access to Nexus Repository at `http://localhost:8081`
- Git repository access

## 🔧 Quick Setup (5 minutes)

### 1. Clone & Navigate
```bash
git clone <repository-url>
cd bird-feeding
```

### 2. Read Project Memory
```bash
# Essential reading for context
cat .project-memory.md
```

### 3. Verify Nexus Connection
```bash
# Test Nexus is running
curl -I http://localhost:8081
# Should return: HTTP/1.1 200 OK
```

### 4. Install Dependencies via Nexus
```bash
# Use our Nexus repository configuration
PIP_CONFIG_FILE=pip.conf pip3 install -r requirements.txt
```

### 5. Run the Application
```bash
python3 app.py
```

### 6. Test API
```bash
# In another terminal
curl http://localhost:8080/
```

## 🎯 Success Criteria
✅ Nexus repository responds on port 8081  
✅ Flask app starts on port 8080  
✅ API returns JSON response  
✅ Packages installed via Nexus (check terminal output)  

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'urllib3'"
```bash
PIP_CONFIG_FILE=pip.conf pip3 install --force-reinstall urllib3
```

### "Address already in use" (Port 5000)
This is expected - app runs on port 8080 instead.

### Nexus connection fails
- Verify Nexus is running: `curl http://localhost:8081`
- Check credentials in `pip.conf` are correct
- Try accessing Nexus web interface

### Package not found in Nexus
The app will fall back to PyPI.org automatically.

## 📚 Understanding the Project

### What You're Learning
- Enterprise package management with Nexus
- Configuration management patterns
- API development with Flask
- Security considerations for dependency management

### Key Files to Understand
1. `pip.conf` - Routes pip to use Nexus
2. `app.py` - Main application with config loading and Observe logging
3. `observe_logger.py` - Custom Observe.inc integration
4. `observe_config.json` - Observability configuration
5. `db_config.json` - Database configuration stored in Nexus
6. `.project-memory.md` - Complete project context

## 🤝 Team Workflow

### Adding New Dependencies
```bash
# Add to requirements.txt first
echo "new-package>=1.0.0" >> requirements.txt

# Install via Nexus
PIP_CONFIG_FILE=pip.conf pip3 install new-package

# Verify it's cached in Nexus
curl -s http://localhost:8081/repository/bird-feeder/simple/ | grep new-package
```

### Making Configuration Changes
1. Update `db_config.json` locally
2. Test changes
3. Upload to Nexus for team sharing:
```bash
curl -u admin:admin123 -X PUT \
  "http://localhost:8081/repository/test-raw/db_config.json" \
  --data-binary @db_config.json \
  -H "Content-Type: application/json"
```

### Code Changes
1. Make changes to `app.py`
2. Test locally
3. Update `.project-memory.md` if architecture changes
4. Commit and push

## 🔍 Verification Commands

```bash
# Check what packages are in Nexus
curl -s http://localhost:8081/repository/bird-feeder/simple/ | grep -i flask

# Test API endpoints (watch for structured logs in terminal)
curl http://localhost:8080/
curl -X POST http://localhost:8080/api/feedings \
  -H "Content-Type: application/json" \
  -d '{"bird_type":"Robin","food_type":"Seeds","quantity":25}'

# Check database
ls -la *.db

# View structured logs (you'll see JSON logs in the terminal running the app)
# Look for entries like:
# 📊 OBSERVE: {"event_type": "feeding_created_successfully", ...}
```

## 💡 Pro Tips
- Always read `.project-memory.md` first for context
- Use `PIP_CONFIG_FILE=pip.conf` for all pip commands
- Check Nexus web interface to see cached packages
- This is a learning project - experiment freely!

---
*Need help? Check `.project-memory.md` or ask the team!*
