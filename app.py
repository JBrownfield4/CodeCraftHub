"""
CodeCraftHub - Simple Flask REST API for managing learning courses
Requirements satisfied:
- CRUD operations for courses
- Data stored in a JSON file: courses.json
- Endpoints:
  - POST /api/courses        -> Add a new course
  - GET /api/courses         -> Get all courses
  - GET /api/courses/<id>    -> Get a specific course by id
  - PUT /api/courses         -> Update a course (requires id in body)
  - DELETE /api/courses      -> Delete a course (requires id in body)
- Each course fields: id (auto), name, description, target_date (YYYY-MM-DD),
  status ("Not Started", "In Progress", "Completed"), created_at (timestamp)
- Auto-creates courses.json if it doesn't exist
- Includes robust error handling and beginner-friendly comments
"""

import json
import os
from datetime import datetime
from typing import List, Optional, Dict

from flask import Flask, request, jsonify

app = Flask(__name__)

# File where courses are stored
DATA_FILE = os.path.join(os.path.dirname(__file__), 'courses.json')
# Allowed status values
ALLOWED_STATUSES = {"Not Started", "In Progress", "Completed"}


def ensure_data_file():
    """
    Ensure the data directory and JSON file exist.
    If the file doesn't exist, create it with an empty list.
    """
    dir_path = os.path.dirname(DATA_FILE)
    os.makedirs(dir_path, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
        except Exception as e:
            # In case the environment is read-only, raise during startup
            raise RuntimeError(f"Failed to create data file: {e}")


def load_courses() -> List[Dict]:
    """
    Read and return the list of courses from the JSON file.
    If the file is empty or not valid JSON, return an empty list.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            # If the JSON root is not a list, treat as invalid
            return []
    except FileNotFoundError:
        # If the file somehow doesn't exist yet, treat as empty
        return []
    except json.JSONDecodeError:
        # Malformed JSON; treat as empty but log the issue
        return []
    except Exception as e:
        # Reraise to be handled by a caller for a proper 500 error
        raise e


def save_courses(courses: List[Dict]):
    """
    Persist the list of courses back to the JSON file.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(courses, f, indent=2)
    except Exception as e:
        # Propagate the exception to be handled by the caller
        raise e


def next_id(courses: List[Dict]) -> int:
    """
    Compute the next auto-incremented id for a new course.
    """
    max_id = max((c.get('id', 0) for c in courses), default=0)
    return max_id + 1


def find_course(courses: List[Dict], course_id: int) -> Optional[Dict]:
    """
    Find and return a course by id, or None if not found.
    """
    for c in courses:
        if c.get('id') == course_id:
            return c
    return None


def is_valid_date(date_str: str) -> bool:
    """
    Validate that the date string is in YYYY-MM-DD format.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# Initialize data file on startup
ensure_data_file()


# Route: GET all courses
@app.route('/api/courses', methods=['GET'])
@app.route('/api/courses/', methods=['GET'])
def get_all_courses():
    """
    Retrieve all courses stored in the JSON file.
    """
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read data file."}), 500

    return jsonify(courses), 200


# Route: GET a specific course by id
@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id: int):
    """
    Retrieve a single course by its id.
    """
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read data file."}), 500

    course = find_course(courses, course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course), 200


# Route: POST create a new course
@app.route('/api/courses', methods=['POST'])
@app.route('/api/courses/', methods=['POST'])
def create_course():
    """
    Create a new course with required fields.
    Expected JSON body:
    {
        "name": "...",
        "description": "...",
        "target_date": "YYYY-MM-DD",
        "status": "Not Started" | "In Progress" | "Completed"
    }
    """
    try:
        payload = request.get_json(force=True) or {}
    except Exception:
        return jsonify({"error": "Invalid JSON payload."}), 400

    # Validate required fields
    required_fields = ["name", "description", "target_date", "status"]
    missing = [f for f in required_fields if not payload.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    name = payload["name"]
    description = payload["description"]
    target_date = payload["target_date"]
    status = payload["status"]

    if status not in ALLOWED_STATUSES:
        return jsonify({"error": f"Invalid status. Allowed: {', '.join(ALLOWED_STATUSES)}"}), 400

    if not is_valid_date(target_date):
        return jsonify({"error": "target_date must be in YYYY-MM-DD format"}), 400

    # Load existing data
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read data file."}), 500

    new_id = next_id(courses)
    created_at = datetime.utcnow().isoformat() + "Z"

    new_course = {
        "id": new_id,
        "name": name,
        "description": description,
        "target_date": target_date,
        "status": status,
        "created_at": created_at
    }

    courses.append(new_course)

    try:
        save_courses(courses)
    except Exception:
        return jsonify({"error": "Failed to write to data file."}), 500

    return jsonify(new_course), 201


# Route: PUT update a course (id must be provided in body)
@app.route('/api/courses', methods=['PUT'])
@app.route('/api/courses/', methods=['PUT'])
def update_course():
    """
    Update an existing course by id.
    Required body fields:
    {
        "id": <int>,
        "name": "...",
        "description": "...",
        "target_date": "YYYY-MM-DD",
        "status": "Not Started" | "In Progress" | "Completed"
    }
    """
    try:
        payload = request.get_json(force=True) or {}
    except Exception:
        return jsonify({"error": "Invalid JSON payload."}), 400

    if "id" not in payload:
        return jsonify({"error": "Missing field: id"}), 400

    course_id = payload["id"]

    # Validate required fields present for update
    required_fields = ["name", "description", "target_date", "status"]
    missing = [f for f in required_fields if not payload.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    if payload["status"] not in ALLOWED_STATUSES:
        return jsonify({"error": f"Invalid status. Allowed: {', '.join(ALLOWED_STATUSES)}"}), 400

    if not is_valid_date(payload["target_date"]):
        return jsonify({"error": "target_date must be in YYYY-MM-DD format"}), 400

    # Load existing data
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read data file."}), 500

    course = find_course(courses, course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Update fields (preserve created_at)
    course["name"] = payload["name"]
    course["description"] = payload["description"]
    course["target_date"] = payload["target_date"]
    course["status"] = payload["status"]

    try:
        save_courses(courses)
    except Exception:
        return jsonify({"error": "Failed to write to data file."}), 500

    return jsonify(course), 200


# Route: DELETE delete a course by id (id must be provided in body)
@app.route('/api/courses', methods=['DELETE'])
@app.route('/api/courses/', methods=['DELETE'])
def delete_course():
    """
    Delete a course by providing its id in the request body:
    {
        "id": <int>
    }
    """
    try:
        payload = request.get_json(force=True) or {}
    except Exception:
        return jsonify({"error": "Invalid JSON payload."}), 400

    if "id" not in payload:
        return jsonify({"error": "Missing field: id"}), 400

    course_id = payload["id"]

    # Load existing data
    try:
        courses = load_courses()
    except Exception:
        return jsonify({"error": "Failed to read data file."}), 500

    course = find_course(courses, course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Remove the course
    try:
        courses = [c for c in courses if c.get('id') != course_id]
        save_courses(courses)
    except Exception:
        return jsonify({"error": "Failed to write to data file."}), 500

    return jsonify({"message": "Course deleted", "id": course_id}), 200


if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, port=5000)
