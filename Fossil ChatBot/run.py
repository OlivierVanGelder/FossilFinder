#!/usr/bin/env python3
"""
Script to run the Brandweer Strategie Advies application.
"""

import os
import sys
import subprocess


def main():
    """
    Main entry point.
    """
    # Check if Ollama is running and the model is available
    print("Controleren van Ollama setup...")
    
    try:
        # Use subprocess.run with encoding specified to avoid encoding issues
        result = subprocess.run(
            ["python", "check_ollama.py"], 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'  # Replace invalid characters instead of failing
        )
        
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            print("\nDruk op Enter om af te sluiten...")
            input()
            sys.exit(result.returncode)
        
        print(result.stdout)
        print("\nStart Brandweer Strategie Advies...")
        
        # Run the main application
        subprocess.run(["python", "main.py"])
        
    except Exception as e:
        print(f"Fout: {str(e)}")
        print("\nDruk op Enter om af te sluiten...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main() 