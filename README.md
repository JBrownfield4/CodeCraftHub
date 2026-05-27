CodeCraftHub - Simple Flask REST API for Learning Courses
CodeCraftHub is a beginner-friendly REST API project built with Python and Flask. It lets developers track courses they want to learn, storing course data in a single JSON file (courses.json) without any database. The API supports full CRUD operations and includes basic validation and helpful error messages to teach REST basics.

1) Project overview and description
A lightweight REST API to manage learning courses.
Data stored in a JSON file named
courses.json
(auto-created if missing).
Each course includes:
id: auto-generated integer starting from 1
name: required string
description: required string
target_date: required string in format YYYY-MM-DD
status: required string, one of "Not Started", "In Progress", "Completed"
created_at: auto-generated timestamp (UTC)
Endpoints use the /api/courses route:
POST /api/courses: create a new course
GET /api/courses: get all courses
GET /api/courses/{id}: get a specific course
PUT /api/courses: update a course (include id in the body)
DELETE /api/courses: delete a course (include id in the body)
No authentication or user management; focused on teaching REST API basics.
2) Features
Create, read, update, and delete courses (CRUD)
Auto-incremented id starting from 1
Data persisted in a single JSON file: courses.json
Input validation:
Required fields
Target date format (YYYY-MM-DD)
Status must be one of: Not Started, In Progress, Completed
Created_at timestamp for each course
Simple, beginner-friendly error messages for common mistakes
Automatic creation of courses.json if it doesn't exist
3) Installation instructions (step-by-step)
Prerequisites

Python 3.8+ (recommended) and pip
A command-line shell (Terminal, PowerShell, etc.)
Get the project

If you have the repo folder already, navigate into it.
If you’re starting fresh, you can copy the project files into a folder named CodeCraftHub.
Set up a virtual environment (recommended)

Linux/macOS:
python3 -m venv venv
source venv/bin/activate
Windows:
python -m venv venv
venv\Scripts\activate
Install dependencies

If a requirements.txt is provided:
pip install -r requirements.txt
Otherwise, install Flask directly:
pip install Flask
Verify files

You should have app.py (your Flask app) and a file named courses.json in the project root. The app will create courses.json automatically if it doesn’t exist.
Optional: test data

You can start with no data; the app will create an empty courses.json on first run.
4) How to run the application
Ensure you are in the project root (where app.py is located).
Activate your virtual environment if you created one.
Run the Flask app:
python app.py
The server starts on http://localhost:5000 by default.
You’re ready to send API requests to http://localhost:5000/api/courses and related routes.
Notes:

The code uses the following routes:
POST /api/courses
GET /api/courses
GET /api/courses/{id}
PUT /api/courses
DELETE /api/courses
All data is stored in courses.json at the project root.
5) API endpoints documentation with examples
Base URL: http://localhost:5000

Create a new course
POST /api/courses

Required JSON body: { "name": "Intro to Flask", "description": "Learn the basics of Flask and build a simple API.", "target_date": "YYYY-MM-DD", "status": "Not Started" // one of: Not Started, In Progress, Completed }

Example curl: curl -s -X POST http://localhost:5000/api/courses
-H "Content-Type: application/json"
-d '{"name":"Intro to Flask","description":"Learn the basics of Flask and build a simple API.","target_date":"2026-07-01","status":"Not Started"}'

Successful response (HTTP 201) example: { "id": 1, "name": "Intro to Flask", "description": "Learn the basics of Flask and build a simple API.", "target_date": "2026-07-01", "status": "Not Started", "created_at": "2026-05-27T12:34:56.789Z" }

Get all courses
GET /api/courses

Example curl: curl -s -X GET http://localhost:5000/api/courses

Successful response (HTTP 200): an array of course objects.

Get a specific course by id
GET /api/courses/{id}

Example curl (replace {id} with a real id, e.g., 1): curl -s -X GET http://localhost:5000/api/courses/1

Successful response (HTTP 200): the course object with that id.

If not found (e.g., id 99999), response: { "error": "Course not found" }

Update a course (PUT)
PUT /api/courses

Required JSON body (include id and all fields): { "id": 1, "name": "Intro to Flask - Updated", "description": "Updated description", "target_date": "YYYY-MM-DD", "status": "In Progress" // one of: Not Started, In Progress, Completed }

Example curl: curl -s -X PUT http://localhost:5000/api/courses
-H "Content-Type: application/json"
-d '{"id":1,"name":"Intro to Flask - Updated","description":"Updated description","target_date":"2026-07-15","status":"In Progress"}'

Successful response (HTTP 200): the updated course object.

Delete a course
DELETE /api/courses

Required JSON body: { "id": 1 }

Example curl: curl -s -X DELETE http://localhost:5000/api/courses
-H "Content-Type: application/json"
-d '{"id":1}'

Successful response (HTTP 200): { "message": "Course deleted", "id": 1 }

Notes:

For convenience, you can replace the id values with any existing course id.
The API validates status values and the target_date format, and returns helpful error messages when something is invalid.
6) Testing instructions
Start the server:

python app.py
Basic flow (manual, copy-paste friendly):

Create a new course curl -s -X POST http://localhost:5000/api/courses
-H "Content-Type: application/json"
-d '{"name":"Intro to Flask","description":"Learn the basics of Flask and build a simple API.","target_date":"2026-07-01","status":"Not Started"}'
Get all courses curl -s -X GET http://localhost:5000/api/courses
Get a specific course (replace 1 with the actual id) curl -s -X GET http://localhost:5000/api/courses/1
Update a course (include id) curl -s -X PUT http://localhost:5000/api/courses
-H "Content-Type: application/json"
-d '{"id":1,"name":"Intro to Flask - Updated","description":"Updated description","target_date":"2026-07-15","status":"In Progress"}'
Delete a course curl -s -X DELETE http://localhost:5000/api/courses
-H "Content-Type: application/json"
-d '{"id":1}'
Additional tips

If you have jq installed, you can extract the id from the POST response and reuse it for subsequent GET/PUT/DELETE requests.
You can reset data by deleting the courses.json file and restarting the server; a new one will be created automatically.
7) Troubleshooting common issues
Server won’t start or port is in use
Ensure no other process is listening on port 5000.
You can run on a different port by editing app.py (change port in app.run) or setting an environment variable if your setup supports it.
Permission denied writing to courses.json
Ensure the project folder is writable.
Run the server with appropriate permissions or adjust the file path.
Invalid JSON payload
Ensure the request Content-Type is application/json and the JSON is valid (balanced braces, quotes, etc.).
Missing required fields (400 response)
Check the payload fields: name, description, target_date, status (and for PUT, id as well).
Invalid date format
target_date must be exactly YYYY-MM-DD (e.g., 2026-07-01). Use leading zeros where needed.
Invalid status value
Status must be one of: Not Started, In Progress, Completed
Corrupted courses.json
If the JSON file is corrupted, the API may fail to read. Delete or fix the file contents; the app will recreate a valid empty array on the next operation.
8) Project structure explanation
app.py
The main Flask application implementing the REST API.
Routes:
POST /api/courses
GET /api/courses
GET /api/courses/<id>
PUT /api/courses
DELETE /api/courses
Helper functions:
load_courses(): read data from courses.json
save_courses(data): write data to courses.json
next_id(courses): compute next auto-incremented id
find_course(courses, id): locate a course by id
is_valid_date(date_str): validate YYYY-MM-DD format
Automatically creates courses.json if missing.
courses.json
The data store for all courses. It starts as an empty array [] and grows as you add courses.
Location: project root (same directory as app.py)
requirements.txt (optional)
If you use one, it may include:
Flask
You can install with: pip install -r requirements.txt
If you’d like, I can tailor this README further with additional examples, screenshots, or a quick getting-started video walkthrough.
