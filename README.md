# Trivia-RESTful-API
This project is a game where users can test their knowledge answering trivia questions. 
The task for the project was to create an API and test suite for implementing the follow functionality:

<ul>
<li>Display questions - both way - all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.</li>
<li>Delete questions.</li>
<li>Add questions and require that they include question and answer text.</li>
<li>Search for questions based on a text query string.</li>
<li>Play the quiz game, randomizing either all questions or within a specific category.</li>
</ul>

In addition a unit testing was implemented with unittest python package and tests for every endpoint has been written.

# About the Stack
It is designed with some key functional areas:

# Backend
The ./backend directory contains a partially completed Flask and SQLAlchemy server. 
All API endpoints defined in '__init__.py' file inside folder 'flaskr' 
Models for database tables stored in 'models.py' along with for DB and SQLAlchemy connection setup.
Please, pay attention - there are no functionality for migration implemented, juct simple "db.create.all()".
If you need migration - feel free to add it

# Frontend
The ./frontend directory contains a complete React frontend to consume the data from the Flask server. 
We didn't touch anything over there except endpoints urls - just to make them the same as on the server.

If you do something - pay special attention to what data the frontend is expecting from each API response to help guide how you format your API.

View the README.md within ./frontend for more details.
