from models.models import Webserver, RequestHistory, SQLAlchemyError, WebserverAdminEmail, db
from sqlalchemy import text
import json
from sqlalchemy import desc
import logging


class WebserverService:
    
    # Test connection to database
    def test_connection() -> str:
        try:
            result = db.session.execute(text('SELECT 1'))
            row = result.fetchone()
            
            if row and row[0] == 1:
                return 'Created this as a test, the Database connection successful!', 200
            else:
                return 'Database connection failed!', 500
        except Exception as e:
            return f'Error connecting to database: {str(e)}', 500


    # Add a new webserver
    def create_new_webserver(data: json) -> tuple:
        message = 'Missing required fields: name and http_url'
        
        if not data or 'name' not in data or 'http_url' not in data:
            return {'error': message}, 400

        try:
            new_webserver = Webserver(name=data['name'], http_url=data['http_url'], status=0)
            new_webserver.save()
            message = f'Webserver <{new_webserver.name}> created successfully'
            return {'message': message, 'id': new_webserver.id}, 201

        except SQLAlchemyError as e:
            logging.error(f"Database error occurred: {e}")
            return {"error": f"Database error occurred.", "message": f"unable to CREATE webservers. {str(e)}"}, 500
        except ValueError as e:
            return {'error': str(e)}, 500


    # List all the webservers in the database
    def get_webservers_list() -> tuple:
        try:
            # Fetch all webservers from the database
            webservers = Webserver.query.all()
            # Prepare data for response
            data = [{"id": ws.id, "info": ws.get_data_dict()} for ws in webservers]

            return data, 200

        except SQLAlchemyError as e:
            logging.error(f"Database error occurred: {e}")
            return {"error": f"Database error occurred.", "message": f"unable to GET webservers list. {str(e)}"}, 500
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred.", "message": f"Unable to GET webservers list. {str(e)}"}, 500


    # Get a specific webserver by their ID
    def get_specific_webserver(id:int):
        webserver = Webserver.query.get_or_404(id)
        
        if not webserver:
            return {'error': "Webserver not found"}, 404
        
        try:
            # Retrieve the web server; automatically raise 404 if not found

            # Query the RequestHistory table for the last 10 records with the specified webserver_id
            last_10_requests = RequestHistory.query.filter_by(webserver_id=id).order_by(desc(RequestHistory.timestamp)).limit(10).all()

            # Create a list of dictionaries for the last 10 requests
            history_data = [{f"request_{i+1}": request.get_data_dict()} for i, request in enumerate(last_10_requests)]

            server_info = webserver.get_data_dict()
            data = {"server_info": server_info, "last_10_requests": history_data}

            return data, 200
            # data_json = json.dumps(data, indent=4, sort_keys=True)
            # Return the response
            # return data_json, 200

        except SQLAlchemyError as e:
            logging.error(f"Database error occurred while accessing webserver {id}: {e}")
            return {"error": f"Database error occurred.", "message": f"Unable to GET webserver details. {str(e)}"}, 500
        except Exception as e:
            logging.error(f"Unexpected error occurred while accessing webserver {id}: {e}")
            return {"error": "An unexpected error occurred.", "message": f"Unable to GET webserver details. {str(e)}"}, 500


    def get_specific_webserver_hisory(id: int):
        try:
            # Query the RequestHistory table for the last 10 records with the specified webserver_id
            last_10_requests = RequestHistory.query.filter_by(webserver_id=id).order_by(desc(RequestHistory.timestamp)).all()

            # Create a list of dictionaries for the last 10 requests
            history_data = [{f"request_{i+1}": request.get_data_dict()} for i, request in enumerate(last_10_requests)]

            # data = {"history": history_data}
            
            # Return the response
            return history_data, 200


        except SQLAlchemyError as e:
            logging.error(f"Database error occurred while accessing webserver {id}: {e}")
            return {"error": f"Database error occurred.", "message": f"Unable to GET webserver HISTORY details. {str(e)}"}, 500
        except Exception as e:
            logging.error(f"Unexpected error occurred while accessing webserver {id}: {e}")
            return {"error": "An unexpected error occurred.", "message": f"Unable to GET webserver HISTORY details. {str(e)}"}, 500
    
    
    # Update a specific webserver by their ID
    def update_specific_webserver(id: int, data: json):
        
        # Retrieve the web server, If don't exist raises 404. 
        webserver = Webserver.query.get_or_404(id)
        if not webserver:
            return {'error': "Webserver not found"}, 404

        try:
            # Attempt to update the web server with new data
            webserver.update_data(data)

            message = f'Webserver {webserver.name} updated successfully'
            
            return {'message': message}, 201

        except SQLAlchemyError as e:
            # Handle database errors
            logging.error(f"Database error occurred while accessing webserver {id}")
            return {'error': 'Database error', 'message': str(e)}, 500
        except Exception as e:
            # Handle other unforeseen errors
            logging.error(f"Unexpected error occurred while accessing webserver {id}")
            return {'error': 'Unexpected error', 'message': str(e)}, 500


    def delete_specific_webserver(id: int):
        # Retrieve the web server, If don't exist raises 404.
        webserver = Webserver.query.get_or_404(id)
        if not webserver:
            return {'error': "Webserver not found"}, 404

        try:

            # Delete admin emails associated with the webserver first to avoid foreign key constraint errors.
            WebserverAdminEmail.query.filter_by(webserver_id=id).delete()
            
            # Next, delete the history as webserver_id in the webserver history is a ForeignKey.
            RequestHistory.query.filter_by(webserver_id=id).delete()

            # Now, delete the webserver itself.
            db.session.delete(webserver)

            # Commit the changes to the database.
            db.session.commit()
            
            message = f"Webserver {webserver.name or id} and all associated histories and admins deleted successfully"
            
            response = {'message': message}
            
            data_json = json.dumps(response, indent=4, sort_keys=True)
            
            return data_json, 204

        except SQLAlchemyError as e:
            db.session.rollback()
            message = f"Database error occurred while deleting from the database: {str(e)}"
            logging.error(message)
            return {'error': message}, 500
        except Exception as e:
            # Handle other unforeseen errors
            message = f"Unexpected error occurred while deleting from the database {str(e)}"
            logging.error(message)
            return {'error': 'Unexpected error', 'message': message}, 500


    def add_new_admin(data: json):
        
        message = 'Missing required fields: webserver_id or email'
        
        if not data or 'webserver_id' not in data or 'email' not in data:
            return {'error': message}, 400

        try:
            print("starting addition")
            
            new_admin = WebserverAdminEmail(webserver_id=data['webserver_id'], email=data['email'])
                        
            new_admin.save()
                        
            message = f'admin <{new_admin.email}> added successfully to {new_admin.webserver_id} admins list'
            return {'message': message}, 201

        except SQLAlchemyError as e:
            # logging.error(f"Database error occurred: {e}")
            message = f"unable to POST the new admin. {str(e)}"
            return {"error": f"Database error occurred.", "message": message}, 500
        except ValueError as e:
            return {'error': str(e)}, 500
