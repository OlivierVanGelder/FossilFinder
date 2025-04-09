#!/usr/bin/env python3
"""
Simple terminal-based chat interface for the Ollama DeepSeek-v3 model.
"""

import os
import sys
import time
from typing import Dict, List, Optional, Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from ollama_client import OllamaClient
from template_manager import TemplateManager
from config import MODEL_NAME


class BrandweerApp:
    """
    Terminal-based chat interface for firefighting strategy advice.
    """

    def __init__(self):
        """
        Initialize the application.
        """
        # Configure console to handle encoding issues
        self.console = Console(force_terminal=True, color_system="auto")
        self.client = OllamaClient()
        self.template_manager = TemplateManager()
        self.running = True

    def display_welcome(self):
        """
        Display the welcome message.
        """
        self.console.clear()
        self.console.print(
            Panel.fit(
                f"[bold blue]Brandweer Strategie Advies[/bold blue]\n\n"
                f"Gebruikt model: [green]{MODEL_NAME}[/green]\n\n"
                f"Type [bold]/help[/bold] voor beschikbare commando's",
                title="Welkom",
                border_style="blue",
            )
        )
        self.console.print()

    def display_help(self):
        """
        Display the help message.
        """
        help_text = """
        [bold]Beschikbare Commando's:[/bold]
        
        [green]/help[/green] - Toon dit help bericht
        [green]/reset[/green] - Reset het gesprek
        [green]/exit[/green] of [green]/quit[/green] - Verlaat de applicatie
        """
        self.console.print(Panel(Markdown(help_text), title="Help", border_style="green"))
        self.console.print()

    def reset_conversation(self):
        """
        Reset the conversation history.
        """
        self.client.reset_conversation()
        self.console.print("[green]Gesprek gereset[/green]")

    def process_command(self, command: str) -> bool:
        """
        Process a command.
        
        Args:
            command (str): The command to process.
            
        Returns:
            bool: True if the command was processed, False otherwise.
        """
        if command.startswith("/"):
            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()
            
            if cmd in ["/exit", "/quit"]:
                self.running = False
                return True
            elif cmd == "/help":
                self.display_help()
                return True
            elif cmd == "/reset":
                self.reset_conversation()
                return True
            else:
                self.console.print(f"[red]Onbekend commando: {cmd}[/red]")
                self.display_help()
                return True
        
        return False

    def generate_response(self, user_input: str):
        """
        Generate a response from the model.
        
        Args:
            user_input (str): The user input.
        """
        # Format the prompt using the current template
        formatted_template = self.template_manager.format_prompt(user_input)
        
        # Generate the response
        try:
            with self.console.status("[bold blue]Bezig met analyseren...[/bold blue]"):
                response = self.client.generate(
                    prompt=formatted_template["user"],
                    system_prompt=formatted_template["system"],
                )
            
            # Display the response
            self.console.print(Panel(
                Markdown(response),
                title="Advies",
                border_style="green",
            ))
                
        except Exception as e:
            self.console.print(f"[red]Fout: {str(e)}[/red]")

    def run(self):
        """
        Run the application.
        """
        self.display_welcome()
        
        while self.running:
            try:
                user_input = Prompt.ask("\n[bold green]Brandweer[/bold green]")
                
                if not user_input.strip():
                    continue
                
                if not self.process_command(user_input):
                    self.generate_response(user_input)
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Onderbroken. Type /exit om te stoppen.[/yellow]")
            except EOFError:
                self.console.print("\n[green]Tot ziens![/green]")
                break
            except Exception as e:
                self.console.print(f"[red]Fout: {str(e)}[/red]")


def main():
    """
    Main entry point.
    """
    app = BrandweerApp()
    app.run()


if __name__ == "__main__":
    main()
