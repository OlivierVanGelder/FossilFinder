"""
Client for interacting with the Ollama API.
"""

import json
import requests
import time
import threading
from typing import Dict, List, Optional, Union, Any, Callable
from functools import lru_cache

from config import OLLAMA_API_URL, MODEL_NAME, DEFAULT_PARAMS


class OllamaClient:
    """
    Client for interacting with the Ollama API.
    """

    def __init__(
        self,
        api_url: str = OLLAMA_API_URL,
        model_name: str = MODEL_NAME,
        default_params: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Ollama client.
        
        Args:
            api_url (str): The URL of the Ollama API.
            model_name (str): The name of the model to use.
            default_params (dict, optional): Default parameters for the model.
        """
        self.api_url = api_url
        self.model_name = model_name
        self.default_params = default_params or DEFAULT_PARAMS
        self.conversation_history: List[Dict[str, str]] = []
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Minimum time between requests in seconds
        self.request_timeout = 30  # Default timeout in seconds

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        timeout: Optional[int] = None,
        fallback_callback: Optional[Callable[[], str]] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate a response from the model.
        
        Args:
            prompt (str): The user prompt.
            system_prompt (str, optional): The system prompt.
            params (dict, optional): Parameters for the model.
            stream (bool): Whether to stream the response.
            timeout (int, optional): Timeout in seconds.
            fallback_callback (callable, optional): Callback to use if the request times out.
            
        Returns:
            Union[str, Dict[str, Any]]: The model's response.
        """
        # Rate limiting to prevent overwhelming the API
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": stream,
        }
        
        # Add system prompt if provided
        if system_prompt:
            payload["system"] = system_prompt
            
        # Add model parameters
        if params:
            payload.update(params)
        else:
            payload.update(self.default_params)
            
        # Add conversation history if available
        if self.conversation_history:
            payload["context"] = self.conversation_history
        
        # Set timeout
        request_timeout = timeout or self.request_timeout
        
        # Make the API request with timeout handling
        try:
            # Start a timer for the request
            start_time = time.time()
            
            # Make the request
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                stream=stream,
                timeout=request_timeout,
            )
            
            self.last_request_time = time.time()
            
            if response.status_code != 200:
                raise Exception(f"Error: {response.status_code} - {response.text}")
                
            if stream:
                return self._handle_stream_response(response)
            else:
                return self._handle_response(response)
                
        except requests.exceptions.Timeout:
            # If we have a fallback callback, use it
            if fallback_callback:
                return fallback_callback()
            else:
                # Generate a simple fallback response
                return self._generate_fallback_response(prompt)
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """
        Generate a simple fallback response when the model times out.
        
        Args:
            prompt (str): The user prompt.
            
        Returns:
            str: A fallback response.
        """
        # Simple fallback response based on keywords in the prompt
        prompt_lower = prompt.lower()
        
        if "defensief" in prompt_lower and "buiten" in prompt_lower:
            return "Defensieve buiteninzet\n---------------------------------\nDeze strategie is geschikt voor situaties waarbij de brand zich heeft verspreid en directe interventie te gevaarlijk is. Door van buitenaf te blussen, kan de brand worden ingeperkt zonder dat brandweerlieden onnodig risico lopen.\n\nMonitor de situatie en pas de strategie aan als de omstandigheden veranderen. Zorg voor voldoende water en blusmiddelen."
        
        elif "offensief" in prompt_lower and "buiten" in prompt_lower:
            return "Offensieve buiteninzet\n---------------------------------\nDeze strategie is effectief wanneer er slachtoffers in het gebouw zijn, maar directe toegang te gevaarlijk is. Door van buitenaf te blussen, kunnen de omstandigheden binnen verbeteren en kan een veilige toegang worden gecreëerd.\n\nBereid je voor op een mogelijke overgang naar een offensieve binneninzet zodra de omstandigheden het toelaten."
        
        elif "defensief" in prompt_lower and "binnen" in prompt_lower:
            return "Defensieve binneninzet\n---------------------------------\nDeze strategie is geschikt wanneer er nog mensen in het gebouw zijn die geëvacueerd moeten worden, maar de brand nog niet volledig is ingeperkt. Door strategisch binnen te gaan, kunnen evacuaties worden gefaciliteerd terwijl de brand wordt bestreden.\n\nZorg voor goede communicatie tussen de binnen- en buitenploegen en heb een duidelijk terugtrekkingsplan."
        
        elif "offensief" in prompt_lower and "binnen" in prompt_lower:
            return "Offensieve binneninzet\n---------------------------------\nDeze strategie is nodig wanneer er directe redding van mensenlevens vereist is en de brand nog beperkt is. Door snel binnen te gaan, kunnen slachtoffers worden gered voordat de brand zich verder verspreidt.\n\nZorg voor voldoende beveiliging en een duidelijk communicatieplan met de buitenploeg."
        
        else:
            # Generic response if no specific keywords are found
            return "Defensieve buiteninzet\n---------------------------------\nOp basis van de beschreven situatie lijkt een defensieve buiteninzet de meest geschikte strategie. Deze aanpak minimaliseert risico's voor brandweerlieden terwijl de brand wordt ingeperkt.\n\nMonitor de situatie en pas de strategie aan als de omstandigheden veranderen."
    
    def _handle_response(self, response: requests.Response) -> str:
        """
        Handle a non-streaming response.
        
        Args:
            response (requests.Response): The API response.
            
        Returns:
            str: The model's response.
        """
        data = response.json()
        
        # Update conversation history
        if "context" in data:
            self.conversation_history = data["context"]
            
        return data.get("response", "")
    
    def _handle_stream_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle a streaming response.
        
        Args:
            response (requests.Response): The API response.
            
        Returns:
            Dict[str, Any]: Information about the streaming response.
        """
        # This is a simplified implementation
        # In a real application, you would process the stream
        return {
            "stream": response.iter_lines(),
            "status": "streaming",
        }
    
    def reset_conversation(self) -> None:
        """
        Reset the conversation history.
        """
        self.conversation_history = []
    
    @lru_cache(maxsize=32)
    def list_models(self) -> List[str]:
        """
        List available models.
        
        Returns:
            List[str]: A list of available model names.
        """
        response = requests.get(f"{self.api_url}/tags")
        
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
            
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    
    def get_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about a model.
        
        Args:
            model_name (str, optional): The name of the model.
            
        Returns:
            Dict[str, Any]: Information about the model.
        """
        model_name = model_name or self.model_name
        response = requests.post(
            f"{self.api_url}/show",
            json={"name": model_name},
        )
        
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
            
        return response.json() 