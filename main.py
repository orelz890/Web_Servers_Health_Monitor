from app.app import FlaskAppSingleton
from models.models import db
from scheduler.scheduler import Scheduler

app = FlaskAppSingleton.get_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        scheduler = Scheduler.get_scheduler(app)
        scheduler.start()
    app.run(debug=True, use_reloader=False)
