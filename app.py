from flask import Flask, request, jsonify
from asgiref.wsgi import WsgiToAsgi
import edge_tts
import base64
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

app = Flask(__name__)


@app.route('/tts', methods=['POST'])
async def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice = data.get('voice', 'en-US-AriaNeural')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Create communication instance
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        
        # Stream and collect audio data
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        # Encode audio to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return jsonify({'audio': audio_base64, 'voice': voice, 'text': text})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Convert Flask app to ASGI
asgi_app = WsgiToAsgi(app)


async def main():
    config = Config()
    config.bind = ["localhost:5000"]
    await serve(asgi_app, config)


if __name__ == '__main__':
    asyncio.run(main())