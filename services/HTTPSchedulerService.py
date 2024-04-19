import requests
from services.ProtocolHandler import ProtocolHandler
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime, timedelta
from models.models import db, RequestHistory
from typing import Tuple


class HTTPSchedulerService(ProtocolHandler):
    TIMEOUT_SECONDS = 59
    SUCCESS_STATUS_CODE_RANGE = range(200, 300)
    
    
    """Override the abstract method from ProtocolHandler to perform an HTTP health check."""
    def check_webserver_health(self,item):
        
        if not item.http_url:
            message = f"Webserver URL with ID {item.id} not found in a health check."
                        
            logging.warning(message)
            return message, 404
        

        success, response_code, latency = self.perform_health_check(item.http_url)
        
        # Network error or timeout
        if response_code is None:
            message = f"Network error or timeout occurred while checking {item.http_url}"
            logging.error(message)

            return message, 500
        
        self.update_webserver_status(item, success)
        
        self.log_request_history(item.id, response_code, latency)

        return f"Webserver: {item.id} Health check complete", 200
    
    
    def perform_health_check(self, url) -> Tuple[bool, int, float]:
                
        try:
            response = requests.get(url, timeout=self.TIMEOUT_SECONDS)
            latency = response.elapsed.total_seconds()
            success = response.status_code in self.SUCCESS_STATUS_CODE_RANGE and latency < 60
            return success, response.status_code, latency
        
        except requests.RequestException as e:
            message = f"Exception occurred during health check for {url}: {str(e)}"
            logging.error(message)

            return message, None, None  # None signifies no response code or latency due to exception
    
    
    def update_webserver_status(self, webserver, success):        
                
        new_status = webserver.status
        if success:
            if 0 <= new_status <= 4:
                new_status += 1
            elif new_status < 0:
                new_status = 1
        else:
            if -2 <= new_status <= 0:
                new_status -= 1
            elif new_status > 0:
                new_status = -1

        try:
            webserver.update_data({"status": new_status})
            
                
        # Catch Integrity exception - happens when deleted a webserver and his history but the schduler already queried the database before and then trying to do regular health check on a deleted webserver. It is handled in the update_data function and passed to this higher level function.
        
        except IntegrityError as e:
            logging.error(f"Integrity error updating status for webserver ID {webserver.id}")
        
        # Catch any other exeption related to the database
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy error updating status for webserver ID {webserver.id}: {str(e)}")


    def log_request_history(self, webserver_id, response_code, latency):
        
        try:
            RequestHistory(webserver_id=webserver_id, response_code=response_code, latency=latency).save()
        except SQLAlchemyError as e:
            logging.error(f"Failed to save request history for webserver ID {webserver_id}: {str(e)}")