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


class FossilBot:
    """
    Terminal-based chat interface for fossil advice.
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
                f"[bold blue]FossilFinder Chatbot[/bold blue]\n\n"
                f"Using model: [green]{MODEL_NAME}[/green]\n\n"
                f"Type [bold]/help[/bold] for available commando's",
                title="Welcome",
                border_style="blue",
            )
        )
        self.console.print()

    def display_help(self):
        """
        Display the help message.
        """
        help_text = """
        [bold]Available Commando's:[/bold]
        
        [green]/help[/green] - Show this help message
        [green]/reset[/green] - Reset the conversation
        [green]/exit[/green] of [green]/quit[/green] - Exit the application
        """
        self.console.print(Panel(Markdown(help_text), title="Help", border_style="green"))
        self.console.print()

    def reset_conversation(self):
        """
        Reset the conversation history.
        """
        self.client.reset_conversation()
        self.console.print("[green]Conversation reset[/green]")

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
                self.console.print(f"[red]Unknown commando: {cmd}[/red]")
                self.display_help()
                return True
        
        return False

    def generate_response(self, user_input: str):
        """
        Generate a streamed response from the model.
        
        Args:
            user_input (str): The user input.
        """
        # Format the prompt using the current template
        formatted_template = self.template_manager.format_prompt(user_input)

        try:
            # Start streaming from the model
            response_stream = self.client.generate(
                prompt=formatted_template["user"],
                system_prompt=formatted_template["system"],
                stream=True  # << Enable streaming here
            )

            self.console.print(Panel.fit("💬 [bold green]Model is thinking...[/bold green]", border_style="blue"))

            full_response = ""

            print("[debug] Starting to read stream...")

            for chunk in response_stream:
                if not isinstance(chunk, dict):
                    continue

                if chunk.get("done"):
                    break

                text = chunk.get("response", "")
                if text:
                    print(text, end="", flush=True)

            print()
            self.console.print(Panel(Markdown(full_response), title="Advice", border_style="green"))

        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def run(self):
        """
        Run the application.
        """
        self.display_welcome()
        
        while self.running:
            try:
                user_input = Prompt.ask("\n[bold green]User[/bold green]")
                
                if not user_input.strip():
                    continue
                
                if not self.process_command(user_input):
                    self.generate_response(user_input)
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interupted. Type /exit om to exit.[/yellow]")
            except EOFError:
                self.console.print("\n[green]Goodbye![/green]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """
    Main entry point.
    """
    app = FossilBot()
    app.run()


if __name__ == "__main__":
    main()
