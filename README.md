# Bird Feeding Python Project

A simple Python project that demonstrates a bird feeding program, configured to use Nexus Repository for PyPI package management.

## Files

- `main.py` - The main Python script containing the Bird Feeding program
- `pip.conf` - Configuration file for using Nexus Repository as PyPI source
- `requirements.txt` - Project dependencies
- `pyproject.toml` - Modern Python project configuration

## Nexus Repository Setup

This project is configured to use a Nexus Repository for PyPI packages. Before running the project, you need to configure your Nexus settings:

### 1. Configure Nexus Repository

Edit the `pip.conf` file and replace the placeholders:
- `YOUR_NEXUS_URL` - Your Nexus repository server URL (e.g., `nexus.company.com`)
- `YOUR_NEXUS_PYPI_REPO` - Your PyPI repository name in Nexus (e.g., `pypi-proxy`)

Example configuration:
```ini
[global]
index-url = https://nexus.company.com/repository/pypi-proxy/simple/
extra-index-url = https://pypi.org/simple/
trusted-host = nexus.company.com
```

### 2. Authentication (if required)

If your Nexus repository requires authentication, you have several options:

#### Option A: Using pip configuration
Create a `~/.netrc` file with your credentials:
```
machine YOUR_NEXUS_URL
login your-username
password your-password
```

#### Option B: Using environment variables
```bash
export PIP_INDEX_URL=https://username:password@YOUR_NEXUS_URL/repository/YOUR_NEXUS_PYPI_REPO/simple/
```

#### Option C: Using pip install with credentials
```bash
pip install --index-url https://username:password@YOUR_NEXUS_URL/repository/YOUR_NEXUS_PYPI_REPO/simple/ package-name
```

### 3. Using the Configuration

#### Global Configuration
Copy `pip.conf` to the appropriate location for global configuration:
- **Linux/macOS**: `~/.pip/pip.conf` or `~/.config/pip/pip.conf`
- **Windows**: `%APPDATA%\pip\pip.ini`

#### Project-specific Configuration
Keep `pip.conf` in the project directory and use:
```bash
pip install --config-settings pip.conf -r requirements.txt
```

Or set the environment variable:
```bash
export PIP_CONFIG_FILE=./pip.conf
pip install -r requirements.txt
```

## How to Run

1. Make sure you have Python 3.8+ installed on your system
2. Configure your Nexus repository settings (see above)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the program:
   ```bash
   python3 main.py
   ```
   or
   ```bash
   python main.py
   ```

## Development Setup

For development with additional tools:
```bash
pip install -e ".[dev]"
```

This installs the project in editable mode with development dependencies like pytest, black, flake8, and mypy.

## Expected Output

```
Welcome to Bird Feeding Station!
Time to feed our feathered friends!
```

## Project Structure

```
bird-feeding/
├── main.py           # Main application
├── pip.conf          # Nexus PyPI configuration
├── requirements.txt  # Production dependencies
├── pyproject.toml    # Modern Python project config
└── README.md         # This file
```

## Requirements

- Python 3.8+
- Access to configured Nexus Repository
- Network connectivity to Nexus server

## Troubleshooting

### Common Issues

1. **SSL Certificate Issues**: Add your Nexus host to `trusted-host` in `pip.conf`
2. **Authentication Failures**: Verify credentials and repository permissions
3. **Network Issues**: Check connectivity to Nexus server
4. **Package Not Found**: Ensure the package exists in your Nexus PyPI repository

### Testing Your Configuration

Test your Nexus configuration:
```bash
pip install --dry-run requests
```

This will show where pip would fetch the `requests` package from without actually installing it.

Enjoy your Python project with Nexus Repository! 🐍
