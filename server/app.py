from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database (DB will be in project root)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db from models and initialize with app
from server.models import db
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Import models after db is initialized (required for migrations to detect models)
from server import models


# Basic route to test server
@app.route('/')
def home():
    return {'message': 'Welcome to the Late Show API'}


if __name__ == '__main__':
    # Run the app on port 5555
    app.run(port=5555, debug=True)