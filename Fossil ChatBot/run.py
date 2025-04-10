#!/usr/bin/env python3
"""
Script to run the FossilFinder chatbot application.
"""

import os
import sys
import subprocess


def main():
    """
    Main entry point.
    """
    # Check if Ollama is running and the model is available
    print("Checking Ollama setup...")
    
    try:
        # Use subprocess.run with encoding specified to avoid encoding issues
        result = subprocess.run(
            ["python", "Fossil Chatbot/check_ollama.py"], 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'  # Replace invalid characters instead of failing
        )
        
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            print("\nPress enter to exit...")
            input()
            sys.exit(result.returncode)
        
        print(result.stdout)
        print("\nStarting FossilFinder advice...")
        
        # Run the main application
        subprocess.run(["python", "Fossil ChatBot/main.py"])
        
    except Exception as e:
        print(f"Fout: {str(e)}")
        print("\nPress enter to exit ...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main() 