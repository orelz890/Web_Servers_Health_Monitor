from apscheduler.schedulers.background import BackgroundScheduler
from models import Webserver
from services import WebserverService

class Scheduler:
    def __init__(self, app):
        self.scheduler = BackgroundScheduler()
        self.app = app
        self.define_jobs()

    def task(self):
        with self.app.app_context():
            webservers = Webserver.query.all()
            for webserver in webservers:
                WebserverService.check_webserver_health(webserver.id)
    
    def define_jobs(self):  
        with self.app.app_context():
            self.scheduler.add_job(
                func=lambda: self.task(), 
                trigger='interval', 
                seconds=30
            )

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()