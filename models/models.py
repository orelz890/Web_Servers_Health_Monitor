
# Helps in handling database-related errors.
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime
import json

# Initialize db
from models.database import DatabaseManager

# Database indexing
from sqlalchemy import Index


db = DatabaseManager.get_db()

health_statuses = {5: "Healthy", -3: "Unhealthy"}



"""
    Database model for storing information about web servers.

    * Inherits from db.Model, which is a base class provided
      by SQLAlchemy for database models in Flask applications.
"""
class Webserver(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    http_url = db.Column(db.String(255), nullable=False, unique=True)
    protocol = db.Column(db.String(20), default='HTTP')
    status = db.Column(db.Integer, default=0, nullable=False)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)



    """ ======================== Not Finished ========================
        TODO - Add email address?
        TODO - Decide if I want to define a unique constraint on http_url here or in gui.
        
        __table_args__ = (
            UniqueConstraint('http_url', name='')
        )
        ==============================================================
    """

    # Update the current Webserver.
    def update_data(self, data: json = {}):
        try:
            if 'name' in data: 
                self.name = data.get('name')
            if 'http_url' in data:
                self.http_url = data.get('http_url')
            if 'status' in data:
                print(data)
                self.status = data.get('status')
                print(f"new status is: {self.status}")
            if 'protocol' in data:
                self.protocol = data.get("protocol")
            
            print("im about to commit")
            db.session.commit()
                
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"error {str(e)}")
            raise e
        

    # Save the current Webserver instance to the database.
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def get_health(self):
        return health_statuses.get(self.status) or "Unstable"



    def get_data_dict(self):
        
        data = {
            'name': self.name,
            'http_url': self.http_url,
            'status': self.status,
            'health': self.get_health(),
            'protocol': self.protocol
        }
        
        return data


"""
    Database model for storing request history related to web servers.
"""
class RequestHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    webserver_id = db.Column(db.Integer, db.ForeignKey('webserver.id'), nullable=False, index=True)
    response_code = db.Column(db.Integer)
    latency = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)


    # Combines webserver_id and timestamp. useful when frequently running queries that filter or sort based on both of these columns.
    __table_args__ = (
        Index('ix_webserver_id_timestamp', 'webserver_id', 'timestamp'),
    )
    
    # Save the current RequestHistory instance to the database.
    def save(self):
                
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    
    def get_data_dict(self):
        
        data = {
            'webserver_id': self.webserver_id,
            'response_code': self.response_code,
            'latency': self.latency,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else 'Unknown'
        }
        
        return data


class WebserverAdminEmail(db.Model):
    """
    Database model for storing admin emails associated with webservers.

    Each record represents an admin email that receives notifications about its webserver's status.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    webserver_id = db.Column(db.Integer, db.ForeignKey('webserver.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    # Relationship back to the Webserver model
    webserver = db.relationship('Webserver', backref=db.backref('admin_emails', lazy=True))

    def __repr__(self):
        return f'<WebserverAdminEmail {self.email}>'

    # Save the current admin instance to the database.
    def save(self):

        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    # Method to serialize data for easy JSONify
    def get_data_dict(self):
        return {
            'id': self.id,
            'webserver_id': self.webserver_id,
            'email': self.email
        }