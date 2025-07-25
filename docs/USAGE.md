# Usage Guide

This document provides detailed usage instructions for the Python Clean Packages toolkit.

## Table of Contents

- [Getting Started](#getting-started)
- [check_packages.sh](#check_packagessh)
- [cleanup_packages.py](#cleanup_packagespy)
- [Workflow Examples](#workflow-examples)
- [Safety Guidelines](#safety-guidelines)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- bash shell (for check_packages.sh)
- Basic understanding of Python virtual environments

### Initial Setup

1. **Make scripts executable:**

   ```bash
   chmod +x scripts/check_packages.sh
   ```

2. **Verify Python version:**

   ```bash
   python --version
   ```

3. **Test the tools:**

   ```bash
   # Check current environment
   ./scripts/check_packages.sh
   
   # Show cleanup info without changes
   python scripts/cleanup_packages.py --info
   ```

## check_packages.sh

### Purpose

Provides a comprehensive overview of your current Python environment, including package listings, environment type detection, and helpful commands.

### Usage

```bash
./scripts/check_packages.sh
```

### What It Shows

1. **Current State:**
   - Python version
   - pip version
   - Virtual environment status

2. **Package Information:**
   - Total package count
   - Package installation location
   - List of main packages with versions

3. **Context-Aware Tips:**
   - Commands to switch between virtual/global environments
   - Useful pip commands for package management

### Example Output

```bash
🔍 PIP PACKAGE CHECKER
=====================

🔧 Current state:
   Python: Python 3.12.6
   Pip: pip 24.2
✅ Virtual environment active: myproject

📦 PACKAGES LOCAL (virtual environment):
   Total: 15 packages
   Location: /path/to/project/venv/lib/python3.12/site-packages
   Main packages:
     • certifi (2024.7.4)
     • charset-normalizer (3.3.2)
     • idna (3.7)
     • pip (24.2)
     • requests (2.32.3)
     • setuptools (75.1.0)
     • urllib3 (2.2.2)
     • wheel (0.44.0)

💡 To see global packages, run:
   deactivate && pip list

📋 Useful commands:
   pip list --outdated    # Outdated packages
   pip show PACKAGE       # Information about a package
   pip freeze             # Generate requirements.txt
   pip list --format=json # List in JSON format
```

## cleanup_packages.py

### **Purpose**

Safely removes non-essential Python packages while protecting system-critical dependencies.

### Basic Syntax

```bash
python scripts/cleanup_packages.py [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--local` | Clean packages from current virtual environment |
| `--global` | Clean packages from global Python installation |
| `--confirm` | Skip confirmation prompts (automatic yes) |
| `--info` | Show environment information only |
| `--dry-run` | Preview changes without executing |
| `--help` | Show help message |

### Usage Modes

#### 1. Information Mode

```bash
python scripts/cleanup_packages.py --info
```

Shows current environment details without making changes.

#### 2. Dry-Run Mode

```bash
python scripts/cleanup_packages.py --local --dry-run
python scripts/cleanup_packages.py --global --dry-run
```

Preview what packages would be removed without actually removing them.

#### 3. Interactive Mode

```bash
python scripts/cleanup_packages.py --local
python scripts/cleanup_packages.py --global
```

Shows packages to be removed and asks for confirmation.

#### 4. Automated Mode

```bash
python scripts/cleanup_packages.py --local --confirm
python scripts/cleanup_packages.py --global --confirm
```

Removes packages without confirmation prompts.

### Protected Packages

The following packages are automatically protected from removal:

**Core Python Tools:**

- `pip`, `setuptools`, `wheel`, `distlib`, `packaging`

**Essential Libraries:**

- `certifi`, `urllib3`, `charset-normalizer`, `idna`, `requests`
- `six`, `python-dateutil`, `pytz`, `platformdirs`, `virtualenv`

**Platform-Specific (macOS):**

- All `pyobjc-*` packages (detected dynamically)

## Workflow Examples

### Daily Development Workflow

1. **Check current environment:**

   ```bash
   ./scripts/check_packages.sh
   ```

2. **Clean virtual environment periodically:**

   ```bash
   # Preview first
   python scripts/cleanup_packages.py --local --dry-run
   
   # Clean if satisfied
   python scripts/cleanup_packages.py --local
   ```

### Project Setup Workflow

1. **Create new virtual environment:**

   ```bash
   python -m venv newproject
   cd newproject
   source bin/activate  # or venv\Scripts\activate on Windows
   ```

2. **Install only needed packages:**

   ```bash
   pip install requests flask
   ```

3. **Check environment:**

   ```bash
   ./scripts/check_packages.sh
   ```

### CI/CD Integration

```bash
#!/bin/bash
# Clean build environment script

# Activate virtual environment
source venv/bin/activate

# Show current state
./scripts/check_packages.sh

# Clean unnecessary packages automatically
python scripts/cleanup_packages.py --local --confirm

# Show final state
./scripts/check_packages.sh
```

### System Maintenance

1. **Check global packages:**

   ```bash
   deactivate  # Exit any virtual environment
   ./scripts/check_packages.sh
   ```

2. **Clean global packages (careful!):**

   ```bash
   # Always dry-run first
   python scripts/cleanup_packages.py --global --dry-run
   
   # Review the list carefully, then:
   python scripts/cleanup_packages.py --global
   ```

## Safety Guidelines

### Before Cleanup

1. **Always check environment first:**

   ```bash
   ./scripts/check_packages.sh
   ```

2. **Use dry-run mode:**

   ```bash
   python scripts/cleanup_packages.py --local --dry-run
   ```

3. **Backup important environments:**

   ```bash
   pip freeze > backup-requirements.txt
   ```

### Environment-Specific Safety

#### Virtual Environments

- ✅ Safe to clean aggressively
- ✅ Easy to recreate if needed
- ✅ Isolated from system

#### Global Environment

- ⚠️ Use extreme caution
- ⚠️ Always use dry-run first
- ⚠️ May affect other projects
- ⚠️ Consider system package manager implications

### Recovery Procedures

#### Restore from Backup

```bash
# If you have a requirements backup
pip install -r backup-requirements.txt
```

#### Recreate Virtual Environment

```bash
# If virtual environment is broken
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Troubleshooting

### Common Issues

#### "Permission Denied" Error

```bash
# Make script executable
chmod +x scripts/check_packages.sh

# For global cleanup, may need elevated permissions
sudo python scripts/cleanup_packages.py --global --confirm
```

#### "Not in Virtual Environment" Warning

```bash
# Activate virtual environment first
source venv/bin/activate

# Or use global mode if intended
python scripts/cleanup_packages.py --global
```

#### "Module Not Found" After Cleanup

```bash
# Reinstall needed package
pip install package-name

# Or restore from backup
pip install -r backup-requirements.txt
```

### Environment Detection Issues

#### Script Shows Wrong Environment

```bash
# Check environment variables
echo $VIRTUAL_ENV
which python
which pip

# Deactivate and reactivate
deactivate
source venv/bin/activate
```

#### Mixed Package Locations

```bash
# Check pip configuration
pip config list

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Performance Issues

#### Slow Package Removal

- Script processes packages in batches of 10
- Some packages may have complex dependencies
- Network issues can slow downloads/verification

#### Large Package Lists

- Use `--dry-run` first to estimate time
- Consider cleaning in smaller batches
- Focus on obvious unused packages first

### Getting Help

1. **Built-in help:**

   ```bash
   python scripts/cleanup_packages.py --help
   ```

2. **Environment information:**

   ```bash
   python scripts/cleanup_packages.py --info
   ./scripts/check_packages.sh
   ```

3. **Debug package issues:**

   ```bash
   pip check  # Check for dependency conflicts
   pip list --outdated  # Show outdated packages
   pip show package-name  # Show package details
   ```
