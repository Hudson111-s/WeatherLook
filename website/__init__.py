import os
from dotenv import load_dotenv
from website.utils import create_geolocator, create_logger, create_valid_pattern
from website.routes import main as main_blueprint
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    key = os.getenv("FLASK_KEY")
    if not key:
        raise ValueError("FLASK_KEY not set in .env")
    app.config["SECRET_KEY"] = key
    # app.config["ENV"] = "production"
    app.config["DEBUG"] = False
    app.config["SESSION_PERMANENT"] = False
    app.register_blueprint(main_blueprint)
    
    # For HTTPS, JavaScript access, and CSRF.
    app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

    app.logger = create_logger()
    app.logger.info("App started.")

    # TODO: Add server-side storage.
    app.limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["100 per minute"],
    )

    # Enable CSRF protection.
    app.csrf = CSRFProtect(app)

    app.geolocator = create_geolocator()
    app.pattern = create_valid_pattern()

    # Error handling for ratelimit and CSRF.
    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning(f"Rate limit exceeded: {request.remote_addr} tried to access {request.path}")
        return "Rate limit exceeded. Try again later.", 429
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        app.logger.warning(f"CSRF token missing or incorrect: {e}")
        return "CSRF validation failed", 400

    return app
