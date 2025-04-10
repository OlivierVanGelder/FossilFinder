"""
Configuration settings for the Ollama DeepSeek-v3 project.
"""

# Ollama API settings
OLLAMA_API_URL = "http://localhost:11434/api"
MODEL_NAME = "nezahatkorkmaz/deepseek-v3:latest"

# Model parameters
DEFAULT_PARAMS = {
    "temperature": 0.7,  # Higher temperature for more creative responses
    "top_p": 0.9,       # Higher top_p for more diverse outputs
    "top_k": 40,        # Higher top_k for better quality
    "num_ctx": 2048,    # Balanced context window
    "repeat_penalty": 1.1,
    "seed": 42,
    "num_thread": 4,    # Balanced thread count
    "num_gpu": 1,       # Use GPU if available
    "num_batch": 8,     # Balanced batch size
}

# Application settings
MAX_HISTORY = 5  # Balanced history size 