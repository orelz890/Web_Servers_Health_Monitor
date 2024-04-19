from flask import Flask
from app.config import Config
from models.models import db
import threading

class FlaskAppSingleton:
    _instance = None
    _lock = threading.Lock()

    def setup_routes(self):
        from api.routes import main as main_blueprint
        self.app.register_blueprint(main_blueprint)

    @classmethod
    def get_app(cls):
        # Ensure that the instance exists
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("Creating the Flask app instance")
                    cls._instance = super(FlaskAppSingleton, cls).__new__(cls)
                    cls._instance.app = Flask(__name__)
                    cls._instance.app.config.from_object(Config)
                    db.init_app(cls._instance.app)
                    cls._instance.setup_routes()
        return cls._instance.app
