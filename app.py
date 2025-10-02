from flask import Flask, request, jsonify
from asgiref.wsgi import WsgiToAsgi
import edge_tts
import base64
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
import os
from dotenv import load_dotenv
from functools import wraps

# Load environment variables with explicit path
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

# Get API key from environment with debugging
API_KEY = os.getenv('API_KEY')

# Debug print to check if .env is loaded
print(f"Current directory: {os.getcwd()}")
print(f"Script directory: {os.path.dirname(__file__)}")
print(f"API_KEY loaded: {'Yes' if API_KEY else 'No'}")
print(f"Environment variables: {[k for k in os.environ.keys() if 'API' in k]}")

if not API_KEY:
    raise ValueError("API_KEY must be set in .env file. Make sure .env file is in the same directory as app.py")


def require_api_key(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        
        if not provided_key or provided_key != API_KEY:
            return jsonify({'error': 'Invalid or missing API key'}), 401
            
        return await f(*args, **kwargs)
    return decorated_function


@app.route('/tts', methods=['POST'])
@require_api_key
async def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice = data.get('voice', 'en-US-AriaNeural')
        rate = data.get('rate', '+0%')  # Default: normal speed
        pitch = data.get('pitch', '+0Hz')  # Default: normal pitch
        volume = data.get('volume', '+0%')  # Default: normal volume
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Validate rate format
        if not isinstance(rate, str) or not (rate.startswith('+') or rate.startswith('-')) or not rate.endswith('%'):
            rate = '+0%'
        
        # Validate pitch format
        if not isinstance(pitch, str) or not (pitch.startswith('+') or pitch.startswith('-')) or not pitch.endswith('Hz'):
            pitch = '+0Hz'
        
        # Validate volume format
        if not isinstance(volume, str) or not (volume.startswith('+') or volume.startswith('-')) or not volume.endswith('%'):
            volume = '+0%'
        
        # Create communication instance with rate, pitch, and volume
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
        audio_data = b""
        
        # Stream and collect audio data
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        # Encode audio to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return jsonify({
            'audio': audio_base64, 
            'voice': voice, 
            'text': text,
            'rate': rate,
            'pitch': pitch,
            'volume': volume
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Convert Flask app to ASGI
asgi_app = WsgiToAsgi(app)


async def main():
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    await serve(asgi_app, config)


if __name__ == '__main__':
    asyncio.run(main())