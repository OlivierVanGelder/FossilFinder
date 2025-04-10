import sys
import os
import base64
from flask import Blueprint, request, jsonify
from tempfile import NamedTemporaryFile

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from FossilChatBot.simple_chat import get_chat_response
from app.models.classifier import FossilClassifier  # Import your image analysis function

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    image_data = data.get('image')
    analysis = data.get('analysis')

    if not user_message and not image_data:
        return jsonify({'error': 'No message or image provided'}), 400

    try:
        system_prompt = None
        if analysis:
            system_prompt = (
                f"You are analyzing a fossil identified as {analysis['class']} "
                f"with {analysis['confidence']}% confidence. "
                "Provide detailed information about this fossil type."
            )

        # Get the chat response
        response = get_chat_response(
            user_message if user_message else "Tell me about this fossil",
            system_prompt=system_prompt
        )
        
        # Debugging output
        print(f"Final response being returned: {response[:200]}...")
        
        return jsonify({
            'response': response,
            'analysis': analysis
        })
            
    except Exception as e:
        print(f"Route error: {str(e)}")
        return jsonify({'error': str(e)}), 500