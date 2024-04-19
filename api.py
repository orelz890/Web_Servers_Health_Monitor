from flask import Flask, jsonify, request
import config

from models import db
from scheduler import Scheduler
from webserverServices import WebserverService


app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)


# Initialize the scheduler instance
scheduler = Scheduler.get_scheduler(app)


# Later it can load the index page. Now lets test the database connection
@app.route('/')
def test_db_connection():
    
    return jsonify(WebserverService.test_connection())


"""
    Create a new Webserver record.

    This endpoint accepts a JSON payload containing the 'name' and 'http_url' of the new Webserver.
    It creates a new Webserver instance and saves it to the database.

    Returns:
        JSON: Success/Failure indication and the ID of the newly created Webserver.
"""

@app.route('/webservers', methods=['POST'])
def create_webserver():
    
    try:
        data = request.json
        message, status_code = WebserverService.create_new_webserver(data)
        return jsonify(message), status_code
    except Exception as e:
        # Handle exceptions that could be raised while accessing request.json
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


"""
    Retrieve a list of all Webserver records.

    This endpoint returns a JSON array containing details of all Webserver instances in the database,
    including their ID, name, URL, and status.

    Returns:
        JSON: Containing details of all Webserver instances.
"""
@app.route('/webservers', methods=['GET'])
def list_webservers():
    
    message, status_code = WebserverService.get_webservers_list()
    return jsonify(message), status_code


# Get a specific web server
@app.route('/webservers/<int:id>', methods=['GET'])
def get_webserver(id):
    
    message, status_code = WebserverService.get_specific_webserver(id)
    return jsonify(message), status_code


# Get a specific web server history
@app.route('/history/<int:id>', methods=['GET'])
def get_history(id):
    
    message, status_code = WebserverService.get_specific_webserver_hisory(id)
    return jsonify(message), status_code


# Update a Webserver
@app.route('/webservers/<int:id>', methods=['PUT'])
def update_webserver(id):

    try:
        data = request.json
        message, status_code = WebserverService.update_specific_webserver(id, data)
        return jsonify(message), status_code
    except Exception as e:
        # Handle exceptions that could be raised while accessing request.json
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


# Delete a Webserver
@app.route('/webservers/<int:id>', methods=['DELETE'])
def delete_webserver(id):

    message, status_code = WebserverService.delete_specific_webserver(id)

    return jsonify(message), status_code



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Start the scheduler before running the Flask application
    scheduler.start()
    # app.run(debug=True, use_reloader=False, threaded=False)
    app.run(debug=True, use_reloader=False)