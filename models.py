#  Importing the SQLAlchemy extension for Flask, which provides integration between Flask and SQLAlchemy,
#  allowing us to work with databases in your Flask application.
from flask_sqlalchemy import SQLAlchemy

# Helps in handling database-related errors.
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


# Initialize db
from database import DatabaseManager


db = DatabaseManager.get_db()




""" ======================== Not Finished ========================
    TODO - Dont forget to handle errors
    ==============================================================
"""



"""
    Database model for storing information about web servers.

    * Inherits from db.Model, which is a base class provided
      by SQLAlchemy for database models in Flask applications.
"""
class Webserver(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    http_url = db.Column(db.String(255), nullable=False, unique=True)
    status = db.Column(db.String(20), default='Unknown')
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)



    """ ======================== Not Finished ========================
        TODO - Add email address?
        TODO - Decide if I want to define a unique constraint on http_url here or in gui.
        
        __table_args__ = (
            UniqueConstraint('http_url', name='')
        )
        ==============================================================
    """
    


    # Save the current Webserver instance to the database.
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        
    # Update the status of the Webserver instance.
    def update_status(self, new_status):
        try:
            self.status = new_status
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise


"""
    Database model for storing request history related to web servers.
"""
class RequestHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    webserver_id = db.Column(db.Integer, db.ForeignKey('webserver.id'), nullable=False)
    response_code = db.Column(db.Integer)
    latency = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    
    # Save the current RequestHistory instance to the database.
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e