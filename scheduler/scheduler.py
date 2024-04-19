from apscheduler.schedulers.background import BackgroundScheduler
from models.models import Webserver
from services.schedulerServices import SchedulerService
from threading import Lock
import atexit
import logging
from scheduler.threadpoolManager import ThreadPoolManager



class Scheduler:
    _instance = None
    _lock = Lock()  # Lock for thread safety

    def __init__(self, app):
        self.scheduler = BackgroundScheduler()
        self.app = app
        self.thread_pool_manager = ThreadPoolManager(app,max_workers=10)
        self.define_jobs()

    @classmethod
    def get_scheduler(cls, app):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(app)
        return cls._instance

    def define_jobs(self):
        with self.app.app_context():
            self.scheduler.add_job(
                func=self.health_task, 
                trigger='interval', 
                seconds=45
            )
            
            # Adding a job to delete old request histories every Sunday at midnight
            self.scheduler.add_job(
                func=self.delete_old_request_histories, 
                trigger='cron', 
                day_of_week='sun', 
                hour=0, 
                minute=0
            )

    
    def health_task(self):
        
        logging.info("STARTED a routine health checks.")
        
        try:
            with self.app.app_context():
                webservers = Webserver.query.all()
                self.thread_pool_manager.execute_tasks(SchedulerService.check_webserver_health, webservers)
            
            logging.info("FINISHED the routine health checks.")

        except Exception as e:
            # Log the exception with an error level log.
            logging.error(f"An error occurred during the routine health checks: {str(e)}")

    
    def delete_old_request_histories():
        logging.info("STARTED a routine weekly delete.")
        
        SchedulerService.delete_old_request_histories()
        
        logging.info("FINISHED the routine weekly delete.")
        

    def start(self):
        atexit.register(self.shutdown)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()