#!/usr/bin/env python3
"""
Script for safe Python package cleanup.
Removes locally installed packages (virtual environment) and globally,
without affecting essential operating system packages.

Usage:
    python cleanup_packages.py --help
    python cleanup_packages.py --local
    python cleanup_packages.py --global --confirm
"""

import subprocess
import sys
import argparse
import json
from typing import List, Set, Dict

# Essential packages that should NOT be removed
ESSENTIAL_PACKAGES = {
    'pip', 'setuptools', 'wheel', 'distlib', 'packaging', 'pyobjc-core',
    'certifi', 'urllib3', 'charset-normalizer', 'idna', 'requests',
    'six', 'python-dateutil', 'pytz', 'platformdirs', 'virtualenv'
}

# Function to get macOS packages dynamically
def get_macos_system_packages() -> Set[str]:
    """Gets pyobjc packages installed dynamically."""
    try:
        result = run_command(['pip', 'list', '--format=json'])
        if result and result.returncode == 0:
            packages = json.loads(result.stdout)
            return {
                pkg['name'].lower() for pkg in packages 
                if pkg['name'].lower().startswith('pyobjc-')
            }
    except:
        pass
    return set()

# Function to get all protected packages
def get_protected_packages() -> Set[str]:
    """Combines essential packages with macOS packages."""
    macos_packages = get_macos_system_packages()
    return ESSENTIAL_PACKAGES.union(macos_packages)


def run_command(cmd: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
    """Executes command and returns result."""
    try:
        return subprocess.run(
            cmd, 
            capture_output=capture_output, 
            text=True, 
            check=False
        )
    except Exception as e:
        print(f"Error executing command {' '.join(cmd)}: {e}")
        return None


def is_in_virtual_env() -> bool:
    """Checks if running in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )


def get_installed_packages() -> Dict[str, str]:
    """Gets list of installed packages with versions."""
    result = run_command(['pip', 'list', '--format=json'])
    if result and result.returncode == 0:
        try:
            packages = json.loads(result.stdout)
            return {pkg['name'].lower(): pkg['version'] for pkg in packages}
        except json.JSONDecodeError:
            print("Error decoding package list")
            return {}
    return {}


def get_removable_packages(all_packages: Dict[str, str]) -> List[str]:
    """Identifies packages that can be safely removed."""
    removable = []
    protected_packages = get_protected_packages()
    protected_lower = {pkg.lower() for pkg in protected_packages}
    
    for package_name in all_packages.keys():
        if package_name not in protected_lower:
            removable.append(package_name)
    
    return sorted(removable)


def show_package_info(packages: Dict[str, str], removable: List[str]):
    """Shows information about packages."""
    print(f"\n{'='*60}")
    print(f"PACKAGE ANALYSIS")
    print(f"{'='*60}")
    print(f"Total installed packages: {len(packages)}")
    print(f"Protected packages (will not be removed): {len(packages) - len(removable)}")
    print(f"Packages that can be removed: {len(removable)}")
    
    if removable:
        print(f"\n{'Packages to be removed:'}")
        print(f"{'-'*40}")
        for pkg in removable:
            version = packages.get(pkg, 'unknown')
            print(f"  • {pkg} ({version})")
    
    print(f"\n{'Protected packages (kept):'}")
    print(f"{'-'*40}")
    protected_packages = get_protected_packages()
    protected_installed = [
        pkg for pkg in packages.keys() 
        if pkg in {p.lower() for p in protected_packages}
    ]
    for pkg in sorted(protected_installed):
        version = packages.get(pkg, 'unknown')
        print(f"  • {pkg} ({version})")


def remove_packages(packages: List[str], batch_size: int = 10) -> bool:
    """Remove packages in batches to avoid dependency issues."""
    if not packages:
        print("No packages to remove.")
        return True
    
    print(f"\nStarting removal of {len(packages)} packages...")
    
    # Remove in batches
    for i in range(0, len(packages), batch_size):
        batch = packages[i:i + batch_size]
        print(f"\nRemoving batch {i//batch_size + 1}: {', '.join(batch)}")
        
        cmd = ['pip', 'uninstall', '-y'] + batch
        result = run_command(cmd, capture_output=False)
        
        if result and result.returncode != 0:
            print(f"Error removing some packages from batch. Continuing...")
    
    print("\nRemoval completed!")
    return True


def cleanup_local_packages(confirm: bool = False):
    """Remove packages from current virtual environment."""
    if not is_in_virtual_env():
        print("❌ WARNING: You are not in a virtual environment!")
        print("This command should only be used in virtual environments.")
        print("For global cleanup, use --global --confirm")
        return False
    
    print("🔧 Virtual environment cleanup")
    print(f"Environment: {sys.prefix}")
    
    packages = get_installed_packages()
    removable = get_removable_packages(packages)
    
    show_package_info(packages, removable)
    
    if not removable:
        print("\n✅ No non-essential packages found to remove.")
        return True
    
    if not confirm:
        response = input(f"\nDo you want to remove {len(removable)} packages? (y/N): ").lower()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("Operation cancelled.")
            return False
    
    return remove_packages(removable)


def cleanup_global_packages(confirm: bool = False):
    """Remove packages from global Python installation."""
    if is_in_virtual_env():
        print("❌ WARNING: You are in a virtual environment!")
        print("Deactivate the virtual environment first for global cleanup:")
        print("  deactivate")
        return False
    
    print("⚠️  GLOBAL CLEANUP - USE WITH CAUTION!")
    print(f"Python: {sys.executable}")
    print("This will affect all projects that don't use virtual environments.")
    
    packages = get_installed_packages()
    removable = get_removable_packages(packages)
    
    show_package_info(packages, removable)
    
    if not removable:
        print("\n✅ No non-essential packages found to remove.")
        return True
    
    if not confirm:
        print("\n⚠️  WARNING: This operation may affect other projects!")
        print("Make sure you know what you're doing.")
        response = input(f"\nConfirm removal of {len(removable)} packages GLOBALLY? (y/N): ").lower()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("Operation cancelled.")
            return False
    
    return remove_packages(removable)


def show_environment_info():
    """Shows information about the current environment."""
    print(f"{'='*60}")
    print(f"ENVIRONMENT INFORMATION")
    print(f"{'='*60}")
    print(f"Python: {sys.version}")
    print(f"Executable: {sys.executable}")
    print(f"Virtual environment: {'Yes' if is_in_virtual_env() else 'No'}")
    if is_in_virtual_env():
        print(f"Venv path: {sys.prefix}")
    print(f"Pip version: {run_command(['pip', '--version']).stdout.strip()}")
    
    packages = get_installed_packages()
    print(f"Total packages: {len(packages)}")


def main():
    parser = argparse.ArgumentParser(
        description="Safe Python package cleanup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python cleanup_packages.py --info                    # Show information
  python cleanup_packages.py --local                   # Clean virtual environment
  python cleanup_packages.py --global --confirm        # Clean global installation
  python cleanup_packages.py --dry-run                 # See what would be removed
        """
    )
    
    parser.add_argument('--local', action='store_true', 
                       help='Clean packages from current virtual environment')
    parser.add_argument('--global', action='store_true', 
                       help='Clean packages from global installation')
    parser.add_argument('--confirm', action='store_true', 
                       help='Confirm automatically (do not ask for confirmation)')
    parser.add_argument('--info', action='store_true', 
                       help='Show only environment information')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be done without executing')
    
    args = parser.parse_args()
    
    if args.info:
        show_environment_info()
        return
    
    if args.dry_run:
        print("🔍 DRY-RUN MODE - No changes will be made")
        packages = get_installed_packages()
        removable = get_removable_packages(packages)
        show_package_info(packages, removable)
        return
    
    if args.local:
        success = cleanup_local_packages(args.confirm)
    elif getattr(args, 'global'):
        success = cleanup_global_packages(args.confirm)
    else:
        parser.print_help()
        return
    
    if success:
        print("\n✅ Cleanup completed successfully!")
    else:
        print("\n❌ Cleanup failed or was cancelled.")


if __name__ == "__main__":
    main()