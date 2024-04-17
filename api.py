# Connection test

from flask import Flask, jsonify, request
import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

from sqlalchemy import text  # Import text from sqlalchemy

@app.route('/')
def test_db_connection():
    try:
        # Explicitly declare the SQL expression as a text object
        result = db.session.execute(text('SELECT 1'))
        # Fetch the first row to confirm the query executed successfully
        row = result.fetchone()
        if row and row[0] == 1:
            return 'Database connection successful!'
        else:
            return 'Database connection failed!'
    except Exception as e:
        return f'Error connecting to database: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)