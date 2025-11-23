from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db from models and initialize with app
from server.models import db, Episode
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Import models after db is initialized
from server import models


# Basic route to test server
@app.route('/')
def home():
    return {'message': 'Welcome to the Late Show API'}


# GET /episodes endpoint: Returns a list of all episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    # Query all episodes from the database
    episodes = Episode.query.all()
    # Build a list of episode dicts for JSON response
    episodes_list = [
        {"id": ep.id, "date": ep.date, "number": ep.number}
        for ep in episodes
    ]
    # Return the list as JSON with status 200
    return jsonify(episodes_list), 200


# Returns a single episode with its appearances and guest details
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    # Query the episode by ID
    episode = Episode.query.get(id)
    if not episode:
        # If not found, return 404 with error message
        return jsonify({"error": "Episode not found"}), 404

    # Build a list of appearances with nested guest info
    appearances = [
        {
            "id": ap.id,
            "rating": ap.rating,
            "guest_id": ap.guest_id,
            "episode_id": ap.episode_id,
            "guest": {
                "id": ap.guest.id,
                "name": ap.guest.name,
                "occupation": ap.guest.occupation
            }
        }
        for ap in episode.appearances
    ]

    # Return the episode with nested appearances as JSON
    return jsonify({
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": appearances
    }), 200


# DELETE:Deletes an episode and its appearances
@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    # Query the episode by ID
    episode = Episode.query.get(id)
    if not episode:
        # If not found, return 404 with error message
        return jsonify({"error": "Episode not found"}), 404

    # Delete the episode
    from server.models import db  #db import
    db.session.delete(episode)
    db.session.commit()

    # Return 204 No Content to indicate successful deletion
    return '', 204


# GET /guests endpoint: Returns a list of all guests
@app.route('/guests', methods=['GET'])
def get_guests():
    # Import the Guest model
    from server.models import Guest

    # Query all guests from the database
    guests = Guest.query.all()

    # Build a list of guest dictionaries for the JSON response
    guests_list = [
        {"id": g.id, "name": g.name, "occupation": g.occupation}
        for g in guests
    ]

    # Return the list as JSON with status 200
    return jsonify(guests_list), 200

if __name__ == '__main__':
    # Run the app on port 5555
    app.run(port=5555, debug=True)