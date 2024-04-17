pip install Flask SQLAlchemy Flask-SQLAlchemy pymysql APScheduler cryptography

<!-- for testing -->
pip install requests
pip install celery


## How to run:

Celery:
* Navigate to the monitor file location in terminal and enter:
''' bash
  celery -A monitor worker --loglevel=info
''' bash