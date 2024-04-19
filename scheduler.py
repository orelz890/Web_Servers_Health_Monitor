from apscheduler.schedulers.background import BackgroundScheduler
from models import Webserver
from schedulerServices import SchedulerService
from threading import Lock
import atexit
import logging
from threadpoolManager import ThreadPoolManager


""" ================= Not finished ==============
    Make a thread pool/ select to enhance performance
    ================= Not finished ==============
"""

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
                func=self.task, 
                trigger='interval', 
                seconds=45
            )

    def task(self):
        
        logging.info("STARTED a routine health checks.")
        
        with self.app.app_context():
            webservers = Webserver.query.all()
            
            self.thread_pool_manager.execute_tasks(SchedulerService.check_webserver_health, webservers)
            
            # for webserver in webservers:
            #     if webserver and webserver.id:
            #         SchedulerService.check_webserver_health(webserver.id)
        logging.info("FINISHED the routine health checks.")

    def start(self):
        atexit.register(self.shutdown)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()