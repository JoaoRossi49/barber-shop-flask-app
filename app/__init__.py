from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import os

app = Flask(__name__)

# Configurações da aplicação
# app.config.from_object('config.Config')

# Inicializa CORS
CORS(app)

# Inicializa o Limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

# A configuração pode ser importada da pasta instance/config.py
from .auth import authenticate_google_api

from .routes import register_routes

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
