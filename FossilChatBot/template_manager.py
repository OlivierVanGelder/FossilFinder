"""
Template manager for the Ollama DeepSeek-v3 project.
"""

from typing import Dict, List, Optional, Any

from templates import get_template


class TemplateManager:
    """
    Manager for handling templates.
    """

    def __init__(self):
        """
        Initialize the template manager.
        """
        self.current_template = "fossil advice"
        self.template_data = get_template(self.current_template)
        self.custom_variables: Dict[str, Any] = {}

    def format_prompt(self, user_input: str) -> Dict[str, str]:
        """
        Format the prompt using the current template.
        
        Args:
            user_input (str): The user input.
            
        Returns:
            Dict[str, str]: The formatted prompt with system and user messages.
        """
        # Create a copy of the template data
        formatted_template = self.template_data.copy()
        
        # Format the user prompt
        formatted_template["user"] = formatted_template["user"].format(
            user_input=user_input,
            **self.custom_variables
        )
        
        return formatted_template 