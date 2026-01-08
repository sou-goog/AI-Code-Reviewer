#!/usr/bin/env python3
"""
Quick start script for AI Code Reviewer.
Checks dependencies and helps with initial setup.
"""
import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.9+"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print("✅ Python version OK")
    return True

def check_git():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git installed")
        return True
    except:
        print("❌ Git not found")
        return False

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except:
        print("❌ Failed to install dependencies")
        return False

def check_api_key():
    """Check if API key is set"""
    if os.environ.get("GEMINI_API_KEY"):
        print("✅ GEMINI_API_KEY is set")
        return True
    else:
        print("⚠️  GEMINI_API_KEY not set")
        print("\n💡 To set your API key:")
        print("   Windows: $env:GEMINI_API_KEY='your_key_here'")
        print("   Linux/Mac: export GEMINI_API_KEY='your_key_here'")
        print("\n   Get a free key: https://aistudio.google.com/app/apikey")
        return False

def main():
    print("🤖 AI Code Reviewer - Quick Start\n")
    
    all_ok = True
    all_ok &= check_python_version()
    all_ok &= check_git()
    all_ok &= install_dependencies()
    check_api_key()  # Don't fail on missing API key
    
    print("\n" + "="*50)
    if all_ok:
        print("✅ Setup complete!")
        print("\n📖 Next steps:")
        print("   1. Set GEMINI_API_KEY (if not already set)")
        print("   2. Stage some code: git add <file>")
        print("   3. Run review: python -m src.main review")
        print("   4. Or start dashboard: streamlit run dashboard.py")
    else:
        print("❌ Setup incomplete. Please fix the errors above.")
    
    print("="*50)

if __name__ == "__main__":
    main()
