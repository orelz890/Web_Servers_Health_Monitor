

"""
    TODO - complete monitor, learn more about celery.
"""

from celery import Celery, group
from services import WebserverService
from models import Webserver
import config

app = Celery('tasks', broker=config.Config.CELERY_BROKER_URL)
app.conf.update(result_backend=config.Config.CELERY_RESULT_BACKEND)

"""
    Configurations:
    
    app.conf.task_routes - This means that when executing the monitor_all_webservers Celery task, it will be placed in the 'monitoring' queue for processing by Celery workers subscribed to that queue.
    
    app.conf.beat_schedule - Defines a Celery periodic task to run every 30 seconds
"""
app.conf.task_routes = {'tasks.monitor_all_webservers': {'queue': 'monitoring'}}

app.conf.beat_schedule = {
    'health_check': {
        'task': 'tasks.monitor_all_webservers',
        'schedule': 30.0,  # Run every 30 seconds
    },
}


@app.task
def monitor_webserver(webserver_id):
    WebserverService.check_webserver_health(webserver_id)


@app.task
def monitor_all_webservers():
    webserver_ids = [webserver.id for webserver in Webserver.query.all()]
    
    # Create a group of tasks to monitor each web server in parallel.
    task_group = group(monitor_webserver.s(webserver_id) for webserver_id in webserver_ids)
    
    task_group.apply_async()


if __name__ == '__main__':
    app.start()