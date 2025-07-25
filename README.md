# Python Clean Packages

A collection of utilities for managing and cleaning Python packages in virtual environments and global installations.

## Description

This toolkit provides safe and efficient tools for Python package management, helping developers maintain clean environments by removing unnecessary packages while protecting essential system dependencies.

## Features

- **Package Environment Inspector**: Check current Python environment and list installed packages
- **Safe Package Cleanup**: Remove non-essential packages with protection for system dependencies
- **Virtual Environment Detection**: Automatically detects and handles virtual vs global environments
- **Batch Processing**: Efficient removal of packages in batches to avoid dependency conflicts
- **Cross-Platform Support**: Works on macOS, Linux, and Windows
- **Dry-Run Mode**: Preview changes before execution

## Tools Included

### 1. `check_packages.sh`

A bash script that provides detailed information about your current Python environment:

- Lists installed packages with versions
- Shows package locations
- Displays environment type (virtual vs global)
- Provides helpful commands for package management

### 2. `cleanup_packages.py`

A Python script for safe package removal:

- Protects essential packages from removal
- Supports both local (virtual environment) and global cleanup
- Batch processing for efficient removal
- Interactive confirmation prompts
- Comprehensive logging and error handling

## Quick Start

### Check Current Environment

```bash
# Make script executable
chmod +x scripts/check_packages.sh

# Run environment check
./scripts/check_packages.sh
```

### Clean Virtual Environment

```bash
# Activate your virtual environment first
source venv/bin/activate

# Clean packages in current virtual environment
python scripts/cleanup_packages.py --local
```

### Clean Global Packages (Use with Caution)

```bash
# Deactivate virtual environment first
deactivate

# Preview what would be removed
python scripts/cleanup_packages.py --global --dry-run

# Actually clean packages (with confirmation)
python scripts/cleanup_packages.py --global --confirm
```

## Installation

### Prerequisites

- Python 3.8 or higher
- bash (for check_packages.sh)

### Setup

1. Clone or download this repository:

   ```bash
   git clone <repository-url>
   cd pythonCleanPackages
   ```

2. Make scripts executable:

   ```bash
   chmod +x scripts/check_packages.sh
   ```

3. No additional dependencies required - uses only Python standard library!

## Usage Examples

### Basic Environment Check

```bash
./scripts/check_packages.sh
```

### Interactive Package Cleanup

```bash
# In virtual environment
python scripts/cleanup_packages.py --local

# Global environment
python scripts/cleanup_packages.py --global
```

## See more [EXAMPLES](docs/EXAMPLES.md) and [USAGE](docs/USAGE.md)

### Automated Cleanup

```bash
# Skip confirmation prompts
python scripts/cleanup_packages.py --local --confirm
```

### Information Only

```bash
# Show environment info
python scripts/cleanup_packages.py --info

# Preview cleanup without changes
python scripts/cleanup_packages.py --local --dry-run
```

## Safety Features

### Protected Packages

The cleanup script automatically protects essential packages:

- `pip`, `setuptools`, `wheel`
- `certifi`, `urllib3`, `requests`
- Platform-specific packages (like `pyobjc-*` on macOS)
- Core development tools

### Environment Detection

- Prevents accidental global cleanup when in virtual environment
- Warns about environment type before operations
- Provides clear instructions for switching contexts

### Batch Processing

- Removes packages in small batches to avoid dependency conflicts
- Continues processing even if some packages fail to remove
- Comprehensive error reporting

## Command Reference

### check_packages.sh

```bash
./scripts/check_packages.sh
```

No arguments needed - automatically detects and displays current environment.

### cleanup_packages.py

```bash
python scripts/cleanup_packages.py [OPTIONS]

Options:
  --local         Clean packages from current virtual environment
  --global        Clean packages from global Python installation
  --confirm       Skip confirmation prompts
  --info          Show environment information only
  --dry-run       Preview changes without executing
  --help          Show help message
```

## Use Cases

- **Development Environment Maintenance**: Keep virtual environments clean and minimal
- **CI/CD Pipeline Cleanup**: Automated cleanup of build environments
- **System Administration**: Maintain clean global Python installations
- **Project Migration**: Clean up old dependencies when switching projects
- **Storage Management**: Reduce disk usage by removing unused packages

## Best Practices

1. **Always use virtual environments** for project development
2. **Test cleanup in dry-run mode** before actual execution
3. **Backup important environments** before major cleanups
4. **Use --local flag** for virtual environment cleanup
5. **Be extra cautious with --global** flag - it affects system-wide packages

## Troubleshooting

### Permission Errors

- Ensure you have appropriate permissions for the target directory
- On some systems, global cleanup may require `sudo`

### Package Dependencies

- Some packages may fail to remove due to dependencies
- The script continues processing other packages
- Check output for specific error messages

### Virtual Environment Issues

- Ensure virtual environment is properly activated before --local cleanup
- Deactivate virtual environment before --global operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with different environments
5. Submit a pull request

## License

This project is for educational and utility purposes. Use responsibly and always backup important environments before cleanup operations.

## Legal Notices

- This software is provided "as is", without warranties
- Users are responsible for testing in their specific environments
- Always review what packages will be removed before confirming operations
