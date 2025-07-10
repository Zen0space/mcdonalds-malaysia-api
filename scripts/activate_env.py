#!/usr/bin/env python3
"""
Environment activation helper script
Ensures virtual environment is properly activated and isolated
"""
import os
import sys
import subprocess
from pathlib import Path

def check_virtual_env():
    """Check if virtual environment is properly activated"""
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment is activated")
        print(f"  Python path: {sys.prefix}")
        return True
    else:
        print("✗ Virtual environment is NOT activated")
        return False

def check_project_packages():
    """Check if required packages are installed in the virtual environment"""
    # Map package names to their import names
    package_imports = {
        'playwright': 'playwright',
        'beautifulsoup4': 'bs4',
        'requests': 'requests',
        'libsql-client': 'libsql_client',
        'pandas': 'pandas',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    return missing_packages

def main():
    """Main function to check environment setup"""
    print("🔍 Checking Python environment setup...")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print()
    
    # Check virtual environment
    if not check_virtual_env():
        print("\n❌ Please activate the virtual environment first:")
        print("   venv\\Scripts\\activate")
        return False
    
    print()
    
    # Check packages
    print("🔍 Checking required packages...")
    missing = check_project_packages()
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r backend/requirements.txt")
        return False
    
    print("\n✅ Environment setup is correct!")
    print("   You can now run the scraper or other project commands.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 