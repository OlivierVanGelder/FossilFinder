from flask import Blueprint, render_template, request, jsonify
from app.models.classifier import FossilClassifier
from app.routes.chat import chat_bp

main_bp = Blueprint('main', __name__)
classifier = FossilClassifier()

main_bp.register_blueprint(chat_bp)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    try:
        result = classifier.predict(file)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
