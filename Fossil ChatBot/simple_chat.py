#!/usr/bin/env python3
"""
Simple terminal-based chat interface for firefighting strategy advice.
No fancy formatting to avoid encoding issues.
"""

import os
import sys
import time
import requests
import threading
from typing import Dict, List, Optional, Any

from ollama_client import OllamaClient
from template_manager import TemplateManager
from config import MODEL_NAME, OLLAMA_API_URL


def check_ollama_setup():
    """
    Check if Ollama is running and the model is available.
    
    Returns:
        bool: True if everything is set up correctly, False otherwise.
    """
    # Check if Ollama is running
    print("Controleren of Ollama draait...")
    try:
        response = requests.get(f"{OLLAMA_API_URL}/version", timeout=5)
        if response.status_code != 200:
            print("Fout: Ollama draait niet.")
            print("Start Ollama en probeer het opnieuw.")
            return False
        print("OK - Ollama draait.")
    except requests.exceptions.ConnectionError:
        print("Fout: Ollama draait niet.")
        print("Start Ollama en probeer het opnieuw.")
        return False
    except requests.exceptions.Timeout:
        print("Fout: Timeout bij verbinding met Ollama.")
        print("Controleer of Ollama draait en probeer het opnieuw.")
        return False
    
    # Check if the model is available
    print(f"Controleren of model '{MODEL_NAME}' beschikbaar is...")
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags", timeout=5)
        if response.status_code != 200:
            print(f"Fout: Model '{MODEL_NAME}' is niet beschikbaar.")
            return False
            
        data = response.json()
        models = [model["name"] for model in data.get("models", [])]
        if MODEL_NAME not in models:
            print(f"Fout: Model '{MODEL_NAME}' is niet beschikbaar.")
            
            # List available models to help the user
            if models:
                print("\nBeschikbare modellen:")
                for model in models:
                    print(f"  - {model}")
            
            print(f"\nZorg ervoor dat je het model '{MODEL_NAME}' hebt gedownload.")
            print(f"Je kunt het downloaden met: ollama pull {MODEL_NAME}")
            
            # Check if this is a custom model variant
            if "/" in MODEL_NAME:
                print("\nOpmerking: Je gebruikt een aangepaste modelvariant.")
                print("Als je problemen ondervindt, probeer dan het basismodel te gebruiken:")
                base_model = MODEL_NAME.split("/")[-1]
                print(f"  ollama pull {base_model}")
                print("Werk vervolgens de MODEL_NAME in config.py bij.")
            
            return False
        print(f"OK - Model '{MODEL_NAME}' is beschikbaar.")
    except requests.exceptions.ConnectionError:
        print(f"Fout: Model '{MODEL_NAME}' is niet beschikbaar.")
        return False
    except requests.exceptions.Timeout:
        print("Fout: Timeout bij verbinding met Ollama.")
        print("Controleer of Ollama draait en probeer het opnieuw.")
        return False
    
    print("\nAlle controles geslaagd! Je kunt nu chatten met het model.")
    return True


def display_loading_animation():
    """
    Display a simple loading animation.
    """
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while True:
        print(f"\r{animation[i]} Bezig met analyseren...", end="", flush=True)
        time.sleep(0.1)
        i = (i + 1) % len(animation)


def main():
    """
    Main entry point.
    """
    # Check if Ollama is running and the model is available
    if not check_ollama_setup():
        print("\nDruk op Enter om af te sluiten...")
        input()
        sys.exit(1)
    
    # Initialize the client and template manager
    client = OllamaClient()
    template_manager = TemplateManager()
    
    # Display welcome message
    print("\n" + "=" * 50)
    print(f"Brandweer Strategie Advies")
    print(f"Gebruikt model: {MODEL_NAME}")
    print("=" * 50)
    print("Type /help voor beschikbare commando's")
    print("=" * 50 + "\n")
    
    # Main chat loop
    running = True
    while running:
        try:
            # Get user input
            user_input = input("\nBrandweer: ")
            
            # Process commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                
                if cmd in ["/exit", "/quit"]:
                    running = False
                    continue
                elif cmd == "/help":
                    print("\nBeschikbare Commando's:")
                    print("  /help - Toon dit help bericht")
                    print("  /reset - Reset het gesprek")
                    print("  /exit of /quit - Verlaat de applicatie")
                    continue
                elif cmd == "/reset":
                    client.reset_conversation()
                    print("Gesprek gereset")
                    continue
                else:
                    print(f"Onbekend commando: {cmd}")
                    print("Type /help voor beschikbare commando's")
                    continue
            
            # Generate response
            if user_input.strip():
                # Format the prompt using the current template
                formatted_template = template_manager.format_prompt(user_input)
                
                # Generate the response
                try:
                    # Start loading animation in a separate thread
                    loading_thread = threading.Thread(target=display_loading_animation)
                    loading_thread.daemon = True
                    loading_thread.start()
                    
                    # Set a shorter timeout for faster responses
                    timeout = 15  # 15 seconds timeout
                    
                    # Generate response with timeout and fallback
                    response = client.generate(
                        prompt=formatted_template["user"],
                        system_prompt=formatted_template["system"],
                        timeout=timeout,
                    )
                    
                    # Stop loading animation
                    print("\r" + " " * 30 + "\r", end="", flush=True)
                    
                    # Display the response
                    print("\nAdvies:")
                    print("-" * 50)
                    print(response)
                    print("-" * 50)
                        
                except Exception as e:
                    print("\r" + " " * 30 + "\r", end="", flush=True)
                    print(f"Fout: {str(e)}")
        
        except KeyboardInterrupt:
            print("\nOnderbroken. Type /exit om te stoppen.")
        except EOFError:
            print("\nTot ziens!")
            break
        except Exception as e:
            print(f"Fout: {str(e)}")
    
    print("\nTot ziens!")


if __name__ == "__main__":
    main() 