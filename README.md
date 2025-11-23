## Late Show API — Flask Code Challenge

### Overview
This project is a backend RESTful API for managing a Late Night TV show, built with Flask, SQLAlchemy, and Flask-RESTful. It supports managing episodes, guests, and their appearances, with full data validation and proper database relationships.

#### What I Achieved
- Set up a Flask application using the MVC pattern
- Created models for Episode, Guest, and Appearance with correct relationships and validations
- Implemented RESTful API endpoints for listing, creating, and deleting resources
- Added error handling and validation for all endpoints
- Wrote and passed unit and integration tests for both models and API endpoints

### How to Test the API

#### 1. Run the Application
```bash
cd server
python app.py
# The API will be available at http://localhost:5555
```

#### 2. Test Endpoints with Postman
Use these example URLs in Postman (replace `<id>` with an actual ID):

- **List all episodes:**
	- `GET http://localhost:5555/episodes`
- **Get episode with appearances:**
	- `GET http://localhost:5555/episodes/<id>`
- **Delete an episode:**
	- `DELETE http://localhost:5555/episodes/<id>`
- **List all guests:**
	- `GET http://localhost:5555/guests`
- **Create a new appearance:**
	- `POST http://localhost:5555/appearances`
		- Body (JSON):
			```json
			{
				"rating": 5,
				"episode_id": 1,
				"guest_id": 2
			}
			```

Check responses and error handling as described in the challenge instructions.

#### 3. Run All Tests
```bash
pytest -x
# All tests should pass. This runs both model and API endpoint tests.
```

#### 4. (Optional) Seed the Database
```bash
python server/seed.py
# Populates the database with sample data for manual testing.
```

---
**Tech Stack:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-RESTful, SQLAlchemy-serializer, pytest

**Author:** Elijah Kamanga
