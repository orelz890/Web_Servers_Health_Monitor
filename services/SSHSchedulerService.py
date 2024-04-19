# services/ftp_handler.py
from services.schedulerProtocolHandler import ProtocolHandler
import logging

class SSHSchedulerService(ProtocolHandler):
    
    def check_webserver_health(self,item):
        # Placeholder implementation
        message = "SSH health check not implemented yet"
        logging.info(message)
        print(message)
        return message, 404
