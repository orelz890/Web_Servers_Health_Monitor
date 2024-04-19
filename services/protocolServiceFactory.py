from services.HTTPSchedulerService import HTTPSchedulerService
from services.FTPSchedulerService import FTPSchedulerService
from services.SSHSchedulerService import SSHSchedulerService
from services.ProtocolHandler import ProtocolHandler

import threading
import logging


class ProtocolHandlerFactory:
    """
    Factory class to create instances of protocol handlers based on the protocol type.
    Uses the Singleton pattern to ensure only one instance of each handler is created.
    """
    _lock = threading.Lock()
    
    _handlers = {
        'HTTP': HTTPSchedulerService,
        'FTP': FTPSchedulerService,
        'SSH': SSHSchedulerService,
    }
    
    _instances = {}


    @classmethod
    def get_protocol_handler(cls, protocol) -> ProtocolHandler:
        """
        Returns a singleton instance of ProtocolHandler based on the specified protocol type.
        
        :param protocol: String, the protocol type of the webserver.
        :return: A singleton instance of a class that extends ProtocolHandler.
        """
        
        with cls._lock:
            protocol = protocol.upper()
            if protocol not in cls._instances:
                handler_class = cls._handlers.get(protocol)
                if handler_class is None:
                    message = f"No handler available for protocol: {protocol}"
                    logging.error(message)
                    
                    print(message)
                    
                    return None
                
                cls._instances[protocol] = handler_class()
            return cls._instances[protocol]