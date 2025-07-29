#!/usr/bin/env python3
"""
CTX Installation Script for Development Environment
Installs ctx-tools in development mode with proper dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} - Success")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Main installation process"""
    print("🚀 CTX Tools Development Installation")
    print("=" * 50)
    
    # Verify we're in the right directory
    if not Path("setup.py").exists() or not Path("ctx").exists():
        print("❌ Error: Must run from ctx-tools project root directory")
        sys.exit(1)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7+ required")
        sys.exit(1)
    
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Install in development mode
    success = True
    
    # Uninstall existing installation
    if run_command("pip uninstall ctx-manager -y", "Uninstalling existing ctx-manager"):
        pass  # Continue even if nothing to uninstall
    
    # Install development dependencies
    success &= run_command("pip install -e .[dev]", "Installing ctx-tools in development mode")
    
    if success:
        # Verify installation
        success &= run_command("ctx --version", "Verifying ctx installation")
        
        if success:
            print("\n🎉 Installation Complete!")
            print("\nQuick test commands:")
            print("  ctx --version")
            print("  ctx create test-context")
            print("  ctx status")
            print("\nFor VS Code integration:")
            print("  Use Ctrl+Shift+P -> 'Tasks: Run Task' -> 'ctx: Show Status'")
        else:
            print("\n❌ Installation verification failed")
            sys.exit(1)
    else:
        print("\n❌ Installation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()