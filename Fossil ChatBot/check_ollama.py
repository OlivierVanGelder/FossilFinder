#!/usr/bin/env python3
"""
Script to check if Ollama is running and the model is available.
"""

import sys
import requests
from rich.console import Console

from config import OLLAMA_API_URL, MODEL_NAME


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


def check_model_available():
    """
    Check if the model is available.
    
    Returns:
        bool: True if the model is available, False otherwise.
    """
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        if response.status_code != 200:
            return False
            
        data = response.json()
        models = [model["name"] for model in data.get("models", [])]
        return MODEL_NAME in models
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
    console = Console()
    
    # Check if Ollama is running
    console.print("Controleren of Ollama draait...")
    if not check_ollama_running():
        console.print("[red]Fout: Ollama draait niet.[/red]")
        console.print("Start Ollama en probeer het opnieuw.")
        sys.exit(1)
    console.print("[green]OK - Ollama draait.[/green]")
    
    # Check if the model is available
    console.print(f"Controleren of model '{MODEL_NAME}' beschikbaar is...")
    if not check_model_available():
        console.print(f"[red]Fout: Model '{MODEL_NAME}' is niet beschikbaar.[/red]")
        
        # List available models to help the user
        available_models = list_available_models()
        if available_models:
            console.print("\nBeschikbare modellen:")
            for model in available_models:
                console.print(f"  - {model}")
        
        console.print(f"\nZorg ervoor dat je het model '{MODEL_NAME}' hebt gedownload.")
        console.print(f"Je kunt het downloaden met: ollama pull {MODEL_NAME}")
        
        # Check if this is a custom model variant
        if "/" in MODEL_NAME:
            console.print("\n[bold]Opmerking:[/bold] Je gebruikt een aangepaste modelvariant.")
            console.print("Als je problemen ondervindt, probeer dan het basismodel te gebruiken:")
            base_model = MODEL_NAME.split("/")[-1]
            console.print(f"  ollama pull {base_model}")
            console.print("Werk vervolgens de MODEL_NAME in config.py bij.")
        
        sys.exit(1)
    console.print(f"[green]OK - Model '{MODEL_NAME}' is beschikbaar.[/green]")
    
    console.print("\n[bold green]Alle controles geslaagd! Je kunt nu de applicatie starten.[/bold green]")


if __name__ == "__main__":
    main() 