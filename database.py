from threading import Lock
from flask_sqlalchemy import SQLAlchemy


"""
    A singleton class responsible for managing the SQLAlchemy database instance.
"""
class DatabaseManager:
    _db = None
    _lock = Lock()  # Lock for thread safety

    # Can be called on the class itself, not on instances of the class
    @classmethod
    def get_db(cls):
        if cls._db is None:
            with cls._lock:  # Acquire the lock to ensure thread safety
                if cls._db is None:  # Double-checking for race conditions
                    cls._db = SQLAlchemy()
        return cls._db
