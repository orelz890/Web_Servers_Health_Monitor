# services/ftp_handler.py
from services.ProtocolHandler import ProtocolHandler
import logging

class FTPSchedulerService(ProtocolHandler):
    
    def check_webserver_health(self, url, webserver_id):
        # Placeholder implementation
        message = "FTP health check not implemented yet"
        logging.info(message)
        print(message)
        return message, 404
