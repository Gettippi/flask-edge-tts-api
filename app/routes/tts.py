from flask import Blueprint, request, jsonify
from app.services.edge_tts_service import EdgeTTSService

tts_bp = Blueprint('tts', __name__)
edge_tts_service = EdgeTTSService()

@tts_bp.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    audio_content = edge_tts_service.convert_text_to_speech(text)
    return jsonify({'audio_content': audio_content}), 200