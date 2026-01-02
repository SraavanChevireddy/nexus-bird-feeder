# 🐦 Bird Feeding API

A hobby project demonstrating enterprise-grade Python development practices with **Nexus Repository management**, **Flask API development**, and **Observe.inc logging integration**.

## 📁 Project Structure

```
bird-feeding/
├── 📄 README.md                    # This file - project overview
├── 🐍 app.py                       # Main Flask application
├── 🔧 observe_logger.py            # Observe.inc logging integration
├── 📋 requirements.txt             # Python dependencies
├── ⚙️ pyproject.toml               # Modern Python project config
├── 🗄️ bird_feedings.db             # SQLite database (auto-created)
├── 📁 config/                      # Configuration files
│   ├── pip.conf                    # Nexus PyPI repository config
│   ├── db_config.json              # Database configuration
│   └── observe_config.json         # Observability settings
├── 📁 docs/                        # Documentation
│   ├── README.md                   # Detailed project documentation
│   ├── TEAM_SETUP.md              # Quick setup guide for team
│   └── .project-memory.md         # Complete project knowledge base
├── 📁 scripts/                     # Utility scripts
│   ├── demo_observe.py            # Observe logging demo
│   └── setup_team.py              # Team setup automation
├── 📁 logs/                        # Log files (created at runtime)
└── 📁 .cursorrules                 # Cursor IDE configuration
```

## 🚀 Quick Start

1. **Prerequisites**: Python 3.8+, Nexus Repository at `http://localhost:8081`
2. **Install dependencies**: `PIP_CONFIG_FILE=config/pip.conf pip3 install -r requirements.txt`
3. **Run application**: `python3 app.py`
4. **Test API**: `curl http://localhost:8080`

## 📚 Documentation

- **📖 [Complete Documentation](docs/README.md)** - Full project details
- **🚀 [Team Setup Guide](docs/TEAM_SETUP.md)** - Quick onboarding
- **🧠 [Project Memory](docs/.project-memory.md)** - Knowledge base

## 🎯 What This Project Demonstrates

### 📦 **Enterprise Package Management**
- Nexus Repository as PyPI proxy
- Dependency caching and security scanning
- Team-consistent package sources

### 🔍 **Observability & Monitoring** 
- Structured JSON logging with Observe.inc
- Request tracing and correlation
- Business event tracking
- Performance metrics collection

### 🏗️ **Modern Python Development**
- Flask REST API with proper structure
- Configuration management (local + remote)
- Type hints and documentation
- Professional project organization

### 🤝 **Team Collaboration**
- Shared configuration via artifact repository
- Comprehensive documentation
- Consistent development environment
- Knowledge preservation system

## 🌐 API Endpoints

### Core Endpoints
- `GET /` - API information
- `POST /api/feedings` - Add bird feeding record
- `GET /api/feedings` - Retrieve feeding records  
- `GET /api/stats` - Get feeding statistics

## 🔧 Configuration

All configuration files are in the `config/` directory:
- **Nexus Repository**: `config/pip.conf`
- **Database**: `config/db_config.json`
- **Observability**: `config/observe_config.json`

## 🛠️ Development

```bash
# Install via Nexus
PIP_CONFIG_FILE=config/pip.conf pip3 install -r requirements.txt

# Run with hot reload
python3 app.py

# Demo features
python3 scripts/demo_observe.py  # Observability
```

## 📊 Technology Stack

- **Backend**: Flask 3.x, SQLite
- **Package Management**: Nexus Repository Manager (PyPI)
- **Observability**: Observe.inc, structlog
- **Development**: Python 3.8+

---

**📖 For detailed information, see [docs/README.md](docs/README.md)**

*This is a learning project demonstrating enterprise patterns in a hobby context.*
