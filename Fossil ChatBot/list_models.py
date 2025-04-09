#!/usr/bin/env python3
"""
Script to list all available models in the Ollama installation.
"""

import sys
import requests
from config import OLLAMA_API_URL


def check_ollama_running():
    """
    Check if Ollama is running.
    
    Returns:
        bool: True if Ollama is running, False otherwise.
    """
    try:
        response = requests.get(f"{OLLAMA_API_URL}/version")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def list_available_models():
    """
    List all available models.
    
    Returns:
        list: A list of available model names.
    """
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        if response.status_code != 200:
            return []
            
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    except requests.exceptions.ConnectionError:
        return []


def main():
    """
    Main entry point.
    """
    # Check if Ollama is running
    if not check_ollama_running():
        print("Fout: Ollama draait niet.")
        print("Start Ollama en probeer het opnieuw.")
        sys.exit(1)
    
    # List available models
    models = list_available_models()
    
    if not models:
        print("Er zijn geen modellen beschikbaar in je Ollama installatie.")
        print("Je kunt modellen downloaden met: ollama pull <model_naam>")
        sys.exit(0)
    
    print("Beschikbare modellen in je Ollama installatie:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    print("\nOm een ander model te gebruiken, werk de MODEL_NAME in config.py bij.")


if __name__ == "__main__":
    main() 