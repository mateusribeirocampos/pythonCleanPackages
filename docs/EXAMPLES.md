# Examples

This document provides practical examples of using the Python Clean Packages toolkit in various scenarios.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Development Scenarios](#development-scenarios)
- [System Administration](#system-administration)
- [CI/CD Integration](#cicd-integration)
- [Automation Scripts](#automation-scripts)
- [Advanced Use Cases](#advanced-use-cases)

## Basic Examples

### Example 1: First-Time Environment Check

```bash
# Navigate to project directory
cd /path/to/your/project

# Check current environment
./scripts/check_packages.sh
```

**Expected Output:**

```bash
🔍 PIP PACKAGE CHECKER
=====================

🔧 Current state:
   Python: Python 3.12.6
   Pip: pip 24.2
❌ No virtual environment active (global mode)

📦 PACKAGES GLOBAL (system):
   Total: 45 packages
   Location: /usr/local/lib/python3.12/site-packages
   Main packages:
     • certifi (2024.7.4)
     • numpy (1.24.3)
     • pandas (2.0.3)
     • requests (2.32.3)
     ... and 37 more packages
```

### Example 2: Simple Virtual Environment Cleanup

```bash
# Activate virtual environment
source venv/bin/activate

# Preview what would be cleaned
python scripts/cleanup_packages.py --local --dry-run
```

**Expected Output:**

```bash
🔍 DRY-RUN MODE - No changes will be made

============================================================
PACKAGE ANALYSIS
============================================================
Total installed packages: 23
Protected packages (will not be removed): 8
Packages that can be removed: 15

Packages to be removed:
----------------------------------------
  • beautifulsoup4 (4.12.2)
  • flask (2.3.3)
  • jinja2 (3.1.2)
  • markupsafe (2.1.3)
  • numpy (1.24.3)
  • pandas (2.0.3)
  • pytest (7.4.2)
  • scipy (1.11.2)
  ... (and 7 more)

Protected packages (kept):
----------------------------------------
  • certifi (2024.7.4)
  • pip (24.2)
  • setuptools (75.1.0)
  • wheel (0.44.0)
  ... (and 4 more)
```

## Development Scenarios

### Scenario 1: New Project Setup

**Situation:** Starting a new Django project with a clean environment.

```bash
# Create new project directory
mkdir my_django_project
cd my_django_project

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Django
pip install django

# Check environment
./scripts/check_packages.sh

# Install development dependencies
pip install pytest black flake8

# Work on project...
# Later, clean up unused packages
python scripts/cleanup_packages.py --local --dry-run
python scripts/cleanup_packages.py --local
```

### Scenario 2: Inheriting a Messy Project

**Situation:** Taking over a project with many unnecessary packages.

```bash
# Activate existing environment
source venv/bin/activate

# Check current state
./scripts/check_packages.sh

# See what can be cleaned
python scripts/cleanup_packages.py --local --dry-run

# Create backup first
pip freeze > backup-requirements.txt

# Clean packages
python scripts/cleanup_packages.py --local

# Test that project still works
python manage.py test  # or your test command

# If something breaks, restore:
# pip install -r backup-requirements.txt
```

### Scenario 3: Multiple Virtual Environments

**Situation:** Managing several project environments.

```bash
# Script to clean all project environments
#!/bin/bash

PROJECTS=(
    "/path/to/project1"
    "/path/to/project2" 
    "/path/to/project3"
)

for project in "${PROJECTS[@]}"; do
    echo "Cleaning $project..."
    cd "$project"
    
    if [ -d "venv" ]; then
        source venv/bin/activate
        python /path/to/scripts/cleanup_packages.py --local --confirm
        deactivate
        echo "✅ Cleaned $project"
    else
        echo "❌ No venv found in $project"
    fi
done
```

## System Administration

### Scenario 4: Global System Cleanup

**Situation:** Cleaning up a development machine with many global packages.

```bash
# First, exit any virtual environments
deactivate

# Check global state
./scripts/check_packages.sh

# VERY IMPORTANT: Dry run first
python scripts/cleanup_packages.py --global --dry-run

# Review the output carefully!
# Look for packages you need globally

# If satisfied, proceed with caution
python scripts/cleanup_packages.py --global

# Verify system still works
python -c "import requests; print('OK')"
```

### Scenario 5: Server Environment Maintenance

**Situation:** Maintaining a production server with Python applications.

```bash
#!/bin/bash
# server-cleanup.sh

echo "🔧 Server Python Environment Maintenance"
echo "========================================"

# Check if any virtual environments are active
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "❌ Virtual environment active. Deactivating..."
    deactivate
fi

# Backup current global packages
pip freeze > /backup/global-packages-$(date +%Y%m%d).txt

# Show current state
./scripts/check_packages.sh

# Dry run global cleanup
echo "📋 Preview of changes:"
python scripts/cleanup_packages.py --global --dry-run

# Wait for manual confirmation
read -p "Proceed with cleanup? (y/N): " confirm
if [ "$confirm" = "y" ]; then
    python scripts/cleanup_packages.py --global --confirm
    echo "✅ Cleanup completed"
else
    echo "❌ Cleanup cancelled"
fi
```

## CI/CD Integration

### Scenario 6: GitHub Actions Workflow

```yaml
# .github/workflows/cleanup.yml
name: Clean Python Environment

on:
  workflow_dispatch:  # Manual trigger
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM

jobs:
  cleanup:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Create virtual environment
      run: |
        python -m venv venv
        source venv/bin/activate
    
    - name: Install dependencies
      run: |
        source venv/bin/activate
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        source venv/bin/activate
        pytest
    
    - name: Clean packages
      run: |
        source venv/bin/activate
        chmod +x scripts/check_packages.sh
        ./scripts/check_packages.sh
        python scripts/cleanup_packages.py --local --confirm
    
    - name: Verify environment
      run: |
        source venv/bin/activate
        ./scripts/check_packages.sh
        python -c "import sys; print(f'Final package count: {len(__import__(\"pkg_resources\").working_set)}')"
```

### Scenario 7: Docker Build Optimization

```dockerfile
# Dockerfile with package cleanup
FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt

# Copy cleanup scripts
COPY scripts/ ./scripts/

# Copy application code
COPY . .

# Clean up packages to reduce image size
RUN chmod +x scripts/check_packages.sh && \
    . venv/bin/activate && \
    ./scripts/check_packages.sh && \
    python scripts/cleanup_packages.py --local --confirm && \
    ./scripts/check_packages.sh

# Set entrypoint
CMD [". venv/bin/activate && python app.py"]
```

## Automation Scripts

### Scenario 8: Daily Development Cleanup

```bash
#!/bin/bash
# daily-cleanup.sh - Add to crontab for daily execution

LOG_FILE="$HOME/cleanup.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Starting daily Python cleanup" >> "$LOG_FILE"

# Find all virtual environments in projects directory
find "$HOME/Projects" -name "venv" -type d | while read venv_path; do
    project_dir=$(dirname "$venv_path")
    project_name=$(basename "$project_dir")
    
    echo "[$DATE] Cleaning $project_name" >> "$LOG_FILE"
    
    cd "$project_dir"
    source venv/bin/activate
    
    # Count packages before
    before=$(pip list | wc -l)
    
    # Clean packages
    python "$HOME/tools/pythonCleanPackages/scripts/cleanup_packages.py" --local --confirm
    
    # Count packages after
    after=$(pip list | wc -l)
    
    echo "[$DATE] $project_name: $before -> $after packages" >> "$LOG_FILE"
    
    deactivate
done

echo "[$DATE] Daily cleanup completed" >> "$LOG_FILE"
```

### Scenario 9: Project Health Check

```python
#!/usr/bin/env python3
"""
project-health.py - Check health of multiple Python projects
"""

import subprocess
import json
import os
from pathlib import Path

def check_project_health(project_path):
    """Check health of a single project."""
    venv_path = project_path / "venv"
    
    if not venv_path.exists():
        return {"status": "no_venv", "packages": 0}
    
    # Activate venv and get package list
    activate_script = venv_path / "bin" / "activate"
    cmd = f"source {activate_script} && pip list --format=json"
    
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        packages = json.loads(result.stdout)
        
        return {
            "status": "healthy",
            "packages": len(packages),
            "package_list": [p["name"] for p in packages]
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def main():
    projects_dir = Path.home() / "Projects"
    results = {}
    
    for project_path in projects_dir.iterdir():
        if project_path.is_dir():
            results[project_path.name] = check_project_health(project_path)
    
    # Generate report
    print("🏥 PROJECT HEALTH REPORT")
    print("=" * 50)
    
    for project, health in results.items():
        status = health["status"]
        if status == "healthy":
            print(f"✅ {project}: {health['packages']} packages")
        elif status == "no_venv":
            print(f"❌ {project}: No virtual environment")
        else:
            print(f"⚠️  {project}: {health.get('error', 'Unknown error')}")
    
    # Suggest cleanups
    print("\n🧹 CLEANUP SUGGESTIONS")
    print("-" * 30)
    
    for project, health in results.items():
        if health["status"] == "healthy" and health["packages"] > 20:
            print(f"📦 {project}: Consider cleanup ({health['packages']} packages)")

if __name__ == "__main__":
    main()
```

## Advanced Use Cases

### Scenario 10: Custom Package Protection

```python
# custom-cleanup.py - Extended cleanup with custom protection rules

import sys
import os

# Add current directory to path to import cleanup_packages
sys.path.insert(0, os.path.dirname(__file__))
from scripts.cleanup_packages import *

# Add custom protected packages for your organization
CUSTOM_PROTECTED = {
    'company-auth-lib',
    'internal-toolkit', 
    'dev-standards',
    'logging-middleware'
}

def get_custom_protected_packages():
    """Override to add custom protected packages."""
    standard_protected = get_protected_packages()
    return standard_protected.union(CUSTOM_PROTECTED)

# Monkey patch the function
get_protected_packages = get_custom_protected_packages

if __name__ == "__main__":
    main()
```

### Scenario 11: Package Usage Analytics

```bash
#!/bin/bash
# package-analytics.sh - Analyze package usage across projects

echo "📊 PACKAGE USAGE ANALYTICS"
echo "=========================="

declare -A package_count
declare -A project_packages

# Scan all projects
for project in "$HOME/Projects"/*; do
    if [ -d "$project/venv" ]; then
        project_name=$(basename "$project")
        
        cd "$project"
        source venv/bin/activate
        
        # Get packages for this project
        packages=$(pip list --format=freeze | cut -d'=' -f1)
        
        for package in $packages; do
            package_count["$package"]=$((${package_count["$package"]} + 1))
            project_packages["$project_name"]+="$package "
        done
        
        deactivate
    fi
done

# Show most common packages
echo "🔝 MOST USED PACKAGES:"
for package in "${!package_count[@]}"; do
    echo "${package_count[$package]} $package"
done | sort -nr | head -10

# Show packages used only once (candidates for cleanup)
echo -e "\n🎯 SINGLE-USE PACKAGES (cleanup candidates):"
for package in "${!package_count[@]}"; do
    if [ "${package_count[$package]}" -eq 1 ]; then
        echo "   $package"
    fi
done | head -20
```

### Scenario 12: Environment Comparison

```python
#!/usr/bin/env python3
"""
env-compare.py - Compare packages between environments
"""

import subprocess
import json
import sys

def get_packages(env_path=None):
    """Get package list from environment."""
    if env_path:
        cmd = f"source {env_path}/bin/activate && pip list --format=json"
    else:
        cmd = "pip list --format=json"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {pkg['name']: pkg['version'] for pkg in json.loads(result.stdout)}

def compare_environments(env1_path, env2_path):
    """Compare two environments."""
    env1_packages = get_packages(env1_path)
    env2_packages = get_packages(env2_path)
    
    env1_only = set(env1_packages.keys()) - set(env2_packages.keys())
    env2_only = set(env2_packages.keys()) - set(env1_packages.keys())
    common = set(env1_packages.keys()) & set(env2_packages.keys())
    
    print(f"📊 ENVIRONMENT COMPARISON")
    print(f"========================")
    print(f"Environment 1: {len(env1_packages)} packages")
    print(f"Environment 2: {len(env2_packages)} packages")
    print(f"Common packages: {len(common)}")
    print(f"Only in env1: {len(env1_only)}")
    print(f"Only in env2: {len(env2_only)}")
    
    if env1_only:
        print(f"\n🔵 Only in Environment 1:")
        for pkg in sorted(env1_only):
            print(f"   • {pkg} ({env1_packages[pkg]})")
    
    if env2_only:
        print(f"\n🔴 Only in Environment 2:")
        for pkg in sorted(env2_only):
            print(f"   • {pkg} ({env2_packages[pkg]})")
    
    # Version differences
    version_diffs = []
    for pkg in common:
        if env1_packages[pkg] != env2_packages[pkg]:
            version_diffs.append((pkg, env1_packages[pkg], env2_packages[pkg]))
    
    if version_diffs:
        print(f"\n⚠️  VERSION DIFFERENCES:")
        for pkg, v1, v2 in version_diffs:
            print(f"   • {pkg}: {v1} vs {v2}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python env-compare.py <env1_path> <env2_path>")
        print("Example: python env-compare.py ./venv1 ./venv2")
        sys.exit(1)
    
    compare_environments(sys.argv[1], sys.argv[2])
```

These examples demonstrate various real-world scenarios where the Python Clean Packages toolkit can be valuable for maintaining clean, efficient Python environments.
