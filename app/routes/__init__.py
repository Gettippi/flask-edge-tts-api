from flask import Blueprint

bp = Blueprint('routes', __name__)

from . import tts  # Import the tts module to register its routes