#!/usr/bin/env python3
"""
Setup script to install pre-commit hooks.

Usage:
    python setup_hooks.py
"""
import os
import shutil
import stat
import sys

def setup_hooks():
    """Install the pre-commit hook."""
    git_hooks_dir = ".git/hooks"
    hook_source = "hooks/pre-commit"
    hook_dest = os.path.join(git_hooks_dir, "pre-commit")
    
    if not os.path.exists(git_hooks_dir):
        print("❌ Error: Not a git repository")
        return 1
    
    if not os.path.exists(hook_source):
        print(f"❌ Error: Hook source not found: {hook_source}")
        return 1
    
    # Copy the hook
    shutil.copy2(hook_source, hook_dest)
    
    # Make it executable
    st = os.stat(hook_dest)
    os.chmod(hook_dest, st.st_mode | stat.S_IEXEC)
    
    print("✅ Pre-commit hook installed successfully!")
    print("\nThe AI code reviewer will now run automatically before each commit.")
    print("To disable, remove: .git/hooks/pre-commit")
    
    return 0

if __name__ == "__main__":
    sys.exit(setup_hooks())
