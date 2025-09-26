#!/usr/bin/env python3
"""
Basic UV Demo Script
Run with: uv run basic_example.py
"""
def main():
    print("Welcome to UV Tutorial!")
    print("Hello from UV - Ultra Fast Python Package Manager!")
    
    # Show Python version and location
    import sys
    print(f"\nPython Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    
    # Show some basic info
    import os
    print(f"\nCurrent working directory: {os.getcwd()}")
    
    print("\n✅ UV is working perfectly!")
    print("Now let's explore more advanced features!")

if __name__ == "__main__":
    main()
