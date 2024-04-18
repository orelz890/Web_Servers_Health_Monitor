from models import db, Webserver, RequestHistory

from flask import Flask, jsonify, request
import config
from flask_sqlalchemy import SQLAlchemy

import json
from sqlalchemy import text

from scheduler import Scheduler
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)


# Initialize the scheduler instance
scheduler = Scheduler.get_scheduler(app)


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
    new_webserver = Webserver(name=data['name'], http_url=data['http_url'], status=0)
    
    # Save to database
    new_webserver.save()
    
    message = f'Webserver <{new_webserver.name}> created successfully'
    
    return jsonify({'message': message, 'id': new_webserver.id}), 201



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
    
    data = [{"id": ws.id ,"info": ws.get_data_dict()} for ws in webservers]
    
    data_json  = json.dumps(data, indent=4, sort_keys=True)
    
    # Use json.dumps for pretty print
    return jsonify(data_json), 200



""" ======================== Not Finished ========================
    TODO - Handle update, delete, and specific webserver retrieval
           and specific webserver requests history
           
           ERRORs!!!
    ==============================================================
"""

# Get a specific web server
@app.route('/webservers/<int:id>', methods=['GET'])
def get_webserver(id):
    # Retrieve the web server, If don't exist raises 404. 
    webserver = Webserver.query.get_or_404(id)

    # Query the RequestHistory table for the last 10 records with the specified webserver_id
    last_10_requests = RequestHistory.query.filter_by(webserver_id=id).order_by(desc(RequestHistory.timestamp)).limit(10).all()


    # Create a list of dictionaries for the last 10 requests
    history_data = [{f"request_{i}": request.get_data_dict() or {}} for i, request in enumerate(last_10_requests)]


    server_info = webserver.get_data_dict()

    data = {"server_info": server_info, "last_10_requests": history_data}

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
    try:
        # Delete them together so we will not have history for deleted webserver
        message = f'Webserver {webserver.name or ""} and all associated histories deleted successfully'
        
        # Delete the history first cuase webserver_id in the webserver history is a ForeignKey.
        RequestHistory.query.filter_by(webserver_id=id).delete()
        
        db.session.delete(webserver)
        
        # Commit changes to database
        db.session.commit()
    
        return jsonify({'message': message})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Start the scheduler before running the Flask application
    scheduler.start()
    # app.run(debug=True, use_reloader=False, threaded=False)
    app.run(debug=True, use_reloader=False)