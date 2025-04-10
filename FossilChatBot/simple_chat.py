import os
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ollama_client import OllamaClient
from template_manager import TemplateManager

client = OllamaClient()
template_manager = TemplateManager()

def get_chat_response(user_input: str, system_prompt: str = None) -> str:
    """
    Generate a response from the model for web use.
    Handles both JSON and plain text streaming responses.
    """
    print(f"\n[DEBUG] Starting chat response for: {user_input[:50]}...")
    
    try:
        # Prepare prompts
        if system_prompt:
            prompt = user_input
        else:
            formatted = template_manager.format_prompt(user_input)
            prompt = formatted["user"]
            system_prompt = formatted["system"]

        # Get the response stream
        response_stream = client.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            stream=True
        )

        full_response = []
        plain_text_mode = False
        
        for raw_chunk in response_stream:
            # Convert bytes to string if needed
            if isinstance(raw_chunk, bytes):
                try:
                    chunk = raw_chunk.decode('utf-8')
                except UnicodeDecodeError:
                    print("[DEBUG] Skipping non-UTF-8 chunk")
                    continue
            else:
                chunk = str(raw_chunk)

            # Try JSON parsing first
            json_data = None
            if chunk.strip().startswith('{'):
                try:
                    json_data = json.loads(chunk)
                except json.JSONDecodeError:
                    pass

            if json_data:
                # Handle JSON response
                if 'response' in json_data:
                    full_response.append(json_data['response'])
                if json_data.get('done', False):
                    break
            else:
                # Handle plain text response
                plain_text_mode = True
                full_response.append(chunk)

        combined = "".join(full_response).strip()
        
        if plain_text_mode:
            print("[DEBUG] Processed as plain text stream")
        else:
            print("[DEBUG] Processed as JSON stream")

        if not combined:
            print("[WARNING] Empty response received")
            return "I couldn't generate a response. Please try again."
            
        print(f"[SUCCESS] Response length: {len(combined)} characters")
        return combined

    except Exception as e:
        error_msg = f"Error processing your request: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return error_msg