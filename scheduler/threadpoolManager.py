from concurrent.futures import ThreadPoolExecutor

from models.models import Webserver
from services.protocolServiceFactory import ProtocolHandlerFactory

# This is the threadpool [MANAGER class]
class ThreadPoolManager:
    def __init__(self, app, max_workers=10):
        self.app = app
        self.max_workers = max_workers

    # The result is not interesting cuase it is performed every 45 seconds
    # And saved in the history. It will be extremely hard to understand 
    # the logs of this func
    def execute_tasks(self, items: list):
        def task_wrapper(item: Webserver):
            try:
                with self.app.app_context():
                    # Get the specific handler for this type from factory
                    scheduler_handler = ProtocolHandlerFactory.get_protocol_handler(item.protocol)
                    
                    if scheduler_handler:
                        return scheduler_handler.check_webserver_health(item.http_url, item.id)
                    else:
                        message = f"No handler available for protocol: {item.protocol}"
                        return message, None, None

            except Exception as e:
                error_message = f"Error processing webserver {item.id}: {str(e)}"
                return error_message, None, None

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            
            for item in items:
                if item and item.id:
                                        
                    # Exctute the task of the specific handler we got from factory for this webserver protocol type
                    executor.submit(task_wrapper, item)