from apscheduler.schedulers.background import BackgroundScheduler
from models import Webserver
from schedulerServices import SchedulerService
from threading import Lock
import atexit


class Scheduler:
    _instance = None
    _lock = Lock()  # Lock for thread safety

    def __init__(self, app):
        self.scheduler = BackgroundScheduler()
        self.app = app
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
                seconds=30
            )

    def task(self):
        with self.app.app_context():
            webservers = Webserver.query.all()
            for webserver in webservers:
                if webserver and webserver.id:
                    SchedulerService.check_webserver_health(webserver.id)

    def start(self):
        atexit.register(self.shutdown)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()