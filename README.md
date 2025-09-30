# Flask Edge TTS API

This project is a Flask application that serves as an API for text-to-speech functionality using the edge-tts service.

## Project Structure

```
flask-edge-tts-api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── tts.py
│   └── services
│       ├── __init__.py
│       └── edge_tts_service.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-edge-tts-api
   ```

2. **Install dependencies:**
   You can install the required Python packages using pip:
   ```
   pip install -r requirements.txt
   ```

3. **Build the Docker image:**
   ```
   docker build -t flask-edge-tts-api .
   ```

4. **Run the application using Docker Compose:**
   ```
   docker-compose up
   ```

## Usage

Once the application is running, you can access the text-to-speech API at the following endpoint:

```
POST /api/tts
```

### Request Body

```json
{
  "text": "Your text here",
  "voice": "en-US-JennyNeural"
}
```

### Response

The API will return an audio file in response to the text-to-speech request.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.