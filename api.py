from models import db, Webserver, RequestHistory

from flask import Flask, jsonify, request
import config
from flask_sqlalchemy import SQLAlchemy

import json
from sqlalchemy import text

from scheduler import Scheduler


app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)


# Initialize the scheduler instance
scheduler = Scheduler(app)


@app.route('/')
def test_db_connection():
    try:
        # Explicitly declare the SQL expression as a text object
        result = db.session.execute(text('SELECT 1'))

        # Fetch the first row to confirm the query executed successfully
        row = result.fetchone()
        if row and row[0] == 1:
            return 'Database connection successful!'
        else:
            return 'Database connection failed!'
    except Exception as e:
        return f'Error connecting to database: {str(e)}'


"""
    Create a new Webserver record.

    This endpoint accepts a JSON payload containing the 'name' and 'http_url' of the new Webserver.
    It creates a new Webserver instance and saves it to the database.

    Returns:
        JSON: Success/Failure indication and the ID of the newly created Webserver.
"""
@app.route('/webservers', methods=['POST'])
def create_webserver():
    data = request.json
    new_webserver = Webserver(name=data['name'], http_url=data['http_url'])
    
    # Save to database
    new_webserver.save()
    
    return jsonify({'message': f'Webserver <{new_webserver.name}> created successfully', 'id': new_webserver.id}), 201



"""
    Retrieve a list of all Webserver records.

    This endpoint returns a JSON array containing details of all Webserver instances in the database,
    including their IDs, names, HTTP URLs, and statuses.

    Returns:
        JSON: Containing details of all Webserver instances.
"""
@app.route('/webservers', methods=['GET'])
def list_webservers():
    webservers = Webserver.query.all()
    
    data = [ws.get_data_dict() for ws in webservers]
    
    # Use json.dumps for pretty print
    return jsonify(json.dumps(data, indent=4, sort_keys=True)), 200



""" ======================== Not Finished ========================
    TODO - Handle update, delete, and specific webserver retrieval
           and specific webserver requests history
    ==============================================================
"""

# Get a specific web server
@app.route('/webservers/<int:id>', methods=['GET'])
def get_webserver(id):
    # Retrieve the web server, If don't exist raises 404. 
    webserver = Webserver.query.get_or_404(id)
    
    """ ======================== Not finished ========================
        TODO - Add last 10 requests.
        ==============================================================
    """

    data = webserver.get_data_dict()
    
    # Use json.dumps for pretty print
    return jsonify(json.dumps(data, indent=4, sort_keys=True)), 200


# Update a Webserver
@app.route('/webservers/<int:id>', methods=['PUT'])
def update_webserver(id):
    
    print(f"im in update_webserver!! data = {request.json}")
    
    # Retrieve the web server, If don't exist raises 404. 
    webserver = Webserver.query.get_or_404(id)
    data = request.json
    webserver.update_data(data)
    
    db.session.commit()
    
    return jsonify({'message': f'Webserver {webserver.name} updated successfully'})

# Delete a Webserver
@app.route('/webservers/<int:id>', methods=['DELETE'])
def delete_webserver(id):
    
    # Retrieve the web server, If don't exist raises 404.
    webserver = Webserver.query.get_or_404(id)
    db.session.delete(webserver)
    db.session.commit()
    
    
    """ ======================== Not finished ========================
        TODO - Delete the history too.
        ==============================================================
    """
    
    
    return jsonify({'message': 'Webserver deleted successfully'})





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Start the scheduler before running the Flask application
    scheduler.start()
    app.run(debug=True)