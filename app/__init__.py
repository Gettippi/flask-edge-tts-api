from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .routes import tts
        app.register_blueprint(tts.bp)

    return app